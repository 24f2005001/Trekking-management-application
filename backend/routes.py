from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt,get_jwt_identity
from datetime import date,datetime
from sqlalchemy import func
import tasks


from models import User,Trek,Booking
from db import db
from cache import cache


OPEN_STATUS = "open"
BOOKED_STATUS = "Booked"
COMPLETED_STATUS = "Completed"
TREK_CACHE_KEY = "view//api/treks/search"

def admin_only():
    claims = get_jwt()
    return claims.get("role") == "admin"

def staff_only():
    claims = get_jwt()
    return claims.get("role") in ["admin", "staff"]

def clear_trek_cache():
    try:
        cache.clear()
    except Exception:
        pass

def task_response(task_id):
    result = tasks.celery.AsyncResult(task_id)
    payload = {
        "task_id": task_id,
        "state": result.state,
        "ready": result.ready(),
    }

    if result.successful():
        payload["result"] = result.result
    elif result.failed():
        payload["error"] = str(result.result)

    return payload


def register_routes(app):

    
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        if not email or not username or not password:
            return jsonify({"message": "Missing required fields"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        hashed_pw = generate_password_hash(password)

        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}),201


    
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            
            
            if not user.is_active:
                return jsonify({"message": "Your account has been deactivated."}), 403
            
            
            access_token = create_access_token(
                identity=str(user.id), 
                additional_claims={"role": user.role}
            )
            
            return jsonify({
                "message": "Login success",
                "access_token": access_token,
                "role": user.role
            }), 200

        return jsonify({"message": "Invalid credentials"}), 401
    

    @app.route('/api/admin/stats', methods=['GET'])
    @jwt_required()
    def admin_dashboard_stats():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
        
        total_treks = Trek.query.count()
        total_users = User.query.filter(User.role.in_(["trekker", "user"])).count()
        total_staff = User.query.filter_by(role="staff").count()
        total_bookings = Booking.query.count()
        
        return jsonify({
            "total_treks": total_treks,
            "total_users": total_users,
            "total_staff": total_staff,
            "total_bookings": total_bookings
        }), 200

    @app.route('/api/admin/reports', methods=['GET'])
    @jwt_required()
    def admin_reports():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403

        popular_rows = (
            db.session.query(
                Trek.id,
                Trek.title,
                Trek.location,
                func.count(Booking.id).label("booking_count")
            )
            .outerjoin(Booking, Booking.trek_id == Trek.id)
            .group_by(Trek.id)
            .order_by(func.count(Booking.id).desc())
            .limit(5)
            .all()
        )

        status_rows = (
            db.session.query(Booking.status, func.count(Booking.id))
            .group_by(Booking.status)
            .all()
        )

        trek_status_rows = (
            db.session.query(Trek.status, func.count(Trek.id))
            .group_by(Trek.status)
            .all()
        )

        completed_treks = Trek.query.filter(Trek.status.ilike("completed")).count()
        participating_users = (
            db.session.query(Booking.user_id)
            .filter(Booking.status.in_([BOOKED_STATUS, COMPLETED_STATUS]))
            .distinct()
            .count()
        )

        return jsonify({
            "completed_treks": completed_treks,
            "participating_users": participating_users,
            "popular_treks": [{
                "id": row.id,
                "title": row.title,
                "location": row.location,
                "booking_count": row.booking_count
            } for row in popular_rows],
            "booking_status_counts": [{
                "status": status or "Unknown",
                "count": count
            } for status, count in status_rows],
            "trek_status_counts": [{
                "status": status or "Unknown",
                "count": count
            } for status, count in trek_status_rows]
        }), 200

    @app.route('/api/admin/jobs/daily-reminders', methods=['POST'])
    @jwt_required()
    def admin_trigger_daily_reminders():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403

        task = tasks.celery.send_task("tasks.send_daily_reminders") 
        return jsonify({
            "message": "Daily reminder job queued.",
            "task_id": task.id
        }), 202

    @app.route('/api/admin/jobs/monthly-report', methods=['POST'])
    @jwt_required()
    def admin_trigger_monthly_report():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403

        task = tasks.celery.send_task("tasks.send_monthly_report") 
        return jsonify({
            "message": "Monthly report job queued.",
            "task_id": task.id
        }), 202

    @app.route('/api/jobs/<task_id>', methods=['GET'])
    @jwt_required()
    def get_job_status(task_id):
        return jsonify(task_response(task_id)), 200
    

    @app.route('/api/admin/staff', methods=['POST'])
    @jwt_required()
    def admin_create_staff():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
            
        data = request.get_json() or {}
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        if not email or not username or not password:
            return jsonify({"message": "Missing required staff credentials"}), 400
            
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already registered."}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already registered."}), 400
            
        hashed_pw = generate_password_hash(password)
        staff = User(
            username=username,
            email=email,
            password_hash=hashed_pw,
            role="staff",
            is_active=True
        )
        db.session.add(staff)
        db.session.commit()
        return jsonify({"message": "Trek Staff account created successfully!"}), 201
    
    @app.route('/api/admin/users', methods=['GET'])
    @jwt_required()
    def admin_get_all_users():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
            
        search_query = request.args.get('search', '')
        query = User.query
        
        if search_query:
            query = query.filter(User.username.like(f"%{search_query}%"))
            
        users = query.all()
        return jsonify([{
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active
        } for u in users]), 200
    
    @app.route('/api/admin/users/<int:user_id>/status', methods=['PATCH'])
    @jwt_required()
    def admin_toggle_user_status(user_id):
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
            
        user = User.query.get_or_404(user_id)
        if user.role == "admin":
            return jsonify({"message": "Cannot deactivate an admin account."}), 400
            
        data = request.get_json() or {}
        is_active = data.get('is_active')
        
        if is_active is not None:
            user.is_active = bool(is_active)
            db.session.commit()
            status_str = "activated" if user.is_active else "deactivated/blacklisted"
            return jsonify({"message": f"User status successfully updated to {status_str}."}), 200
            
        return jsonify({"message": "Missing status field 'is_active'"}), 400
    
    @app.route('/api/admin/bookings', methods=['GET'])
    @jwt_required()
    def admin_view_all_bookings():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
            
        bookings = Booking.query.all()
        output = []
        for b in bookings:
            user = User.query.get(b.user_id)
            trek = Trek.query.get(b.trek_id)
            output.append({
                "booking_id": b.id,
                "user_id": b.user_id,
                "username": user.username if user else "Unknown User",
                "trek_id": b.trek_id,
                "trek_name": trek.title if trek else "Deleted Trek",
                "booking_date": b.booking_date.strftime('%Y-%m-%d') if b.booking_date else None,
                "status": b.status,
                "payment_status": b.payment_status
            })
        return jsonify(output), 200
    

    @app.route('/api/admin/treks',methods=['POST'])
    @jwt_required()
    def admin_create_trek():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
        data = request.get_json() or {}

        try:
            start_dt = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
            end_dt = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()

            total_slots = int(data.get('total_slots', 0))
            staff_id = data.get('staff_id') or None

            if staff_id:
                staff_user = User.query.filter_by(id=int(staff_id), role="staff", is_active=True).first()
                if not staff_user:
                    return jsonify({"message": "Assigned staff must be an active staff account."}), 400

            trek = Trek(
                title=data.get('title'),
                location=data.get('location'),
                difficulty=data.get('difficulty'),
                duration_days=int(data.get('duration_days', 1)),
                total_slots=total_slots,
                available_slots=total_slots, 
                status=data.get('status', 'pending').lower(), 
                start_date=start_dt,
                end_date=end_dt,
                price=float(data.get('price', 0.0)),
                staff_id=staff_id
            )
            db.session.add(trek)
            db.session.commit()
            clear_trek_cache()
            return jsonify({"message": "Trek created successfully!", "trek_id": trek.id}), 201
            
        except (ValueError, TypeError) as e:
            return jsonify({"message": f"Invalid data format: {str(e)}"}), 400
        

    @app.route('/api/admin/treks', methods=['GET'])
    @jwt_required()
    def admin_get_all_treks():
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
        
        treks = Trek.query.all()
        output = []
        for t in treks:
            output.append({
                "id": t.id,
                "title": t.title,
                "location": t.location,
                "difficulty": t.difficulty,
                "duration_days": t.duration_days,
                "total_slots": t.total_slots,
                "available_slots": t.available_slots,
                "status": t.status,
                "start_date": t.start_date.strftime('%Y-%m-%d'),
                "end_date": t.end_date.strftime('%Y-%m-%d'),
                "price": t.price,
                "staff_id": t.staff_id
            })
        return jsonify(output), 200


    @app.route('/api/admin/treks/<int:trek_id>', methods=['PUT'])
    @jwt_required()
    def admin_update_trek(trek_id):
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
        trek = Trek.query.get_or_404(trek_id)
        data = request.get_json() or {}

        try:
            if 'title' in data: trek.title = data['title']
            if 'location' in data: trek.location = data['location']
            if 'difficulty' in data: trek.difficulty = data['difficulty']
            if 'duration_days' in data: trek.duration_days = int(data['duration_days'])
            if 'price' in data: trek.price = float(data['price'])
            if 'status' in data: trek.status = data['status'].lower()
            if 'staff_id' in data:
                staff_id = data['staff_id'] or None
                if staff_id:
                    staff_user = User.query.filter_by(id=int(staff_id), role="staff", is_active=True).first()
                    if not staff_user:
                        return jsonify({"message": "Assigned staff must be an active staff account."}), 400
                trek.staff_id = staff_id
            
            if 'total_slots' in data:
                old_total = trek.total_slots
                new_total = int(data['total_slots'])
                
                diff = new_total - old_total
                trek.total_slots = new_total
                trek.available_slots += diff

            if 'start_date' in data:
                trek.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            if 'end_date' in data:
                trek.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

            if trek.status.lower() == "completed":
                Booking.query.filter_by(trek_id=trek.id, status=BOOKED_STATUS).update({"status": COMPLETED_STATUS})

            db.session.commit()
            clear_trek_cache()
            return jsonify({"message": "Trek updated successfully!"}), 200
            
        except (ValueError, TypeError) as e:
            return jsonify({"message": f"Data update error: {str(e)}"}), 400


    @app.route('/api/admin/treks/<int:trek_id>', methods=['DELETE'])
    @jwt_required()
    def admin_delete_trek(trek_id):
        if not admin_only():
            return jsonify({"message": "Administration access required."}), 403
        trek = Trek.query.get_or_404(trek_id)
        if len(trek.bookings) > 0:
            return jsonify({
                "message": "Cannot delete this trek because it has active or past bookings. Please update its status to 'Closed' instead to maintain historical data."
            }), 400
        
        db.session.delete(trek)
        db.session.commit()
        clear_trek_cache()
        return jsonify({"message": "Trek deleted completely."}), 200
    
    #trek staff endpoints

    @app.route('/api/staff/treks', methods=['GET'])
    @jwt_required()
    def staff_assigned_treks():
        if not staff_only():
            return jsonify({"message": "Staff credentials required."}), 403
            
        staff_id = int(get_jwt_identity())
        
        
        if admin_only():
            treks = Trek.query.all()
        else:
            treks = Trek.query.filter_by(staff_id=staff_id).all()
            
        output = []
        for t in treks:
            
            registered_count = Booking.query.filter_by(trek_id=t.id, status=BOOKED_STATUS).count()
            output.append({
                "id": t.id,
                "title": t.title,
                "location": t.location,
                "difficulty": t.difficulty,
                "available_slots": t.available_slots,
                "total_slots": t.total_slots,
                "status": t.status,
                "registered_users_count": registered_count,
                "start_date": t.start_date.strftime('%Y-%m-%d') if t.start_date else None,
                "end_date": t.end_date.strftime('%Y-%m-%d') if t.end_date else None
            })
        return jsonify(output), 200

    @app.route('/api/staff/treks/<int:trek_id>', methods=['PATCH'])
    @jwt_required()
    def staff_update_trek_status(trek_id):
        if not staff_only():
            return jsonify({"message": "Staff credentials required."}), 403
            
        trek = Trek.query.get_or_404(trek_id)
        staff_id = int(get_jwt_identity())
        
        
        if not admin_only() and trek.staff_id != staff_id:
            return jsonify({"message": "Access Denied. You are not assigned to manage this trek."}), 403
            
        data = request.get_json() or {}
        
        if 'status' in data:
            trek.status = data['status'].lower()
        if 'available_slots' in data:
            available_slots = int(data['available_slots'])
            if available_slots < 0 or available_slots > trek.total_slots:
                return jsonify({"message": "Available slots must be between 0 and total slots."}), 400
            trek.available_slots = available_slots

        if trek.status.lower() == "completed":
            Booking.query.filter_by(trek_id=trek.id, status=BOOKED_STATUS).update({"status": COMPLETED_STATUS})
            
        db.session.commit()
        clear_trek_cache()
        return jsonify({"message": "Trek progress updated successfully."}), 200

    @app.route('/api/staff/treks/<int:trek_id>/participants', methods=['GET'])
    @jwt_required()
    def staff_get_participants(trek_id):
        if not staff_only():
            return jsonify({"message": "Staff credentials required."}), 403
            
        trek = Trek.query.get_or_404(trek_id)
        staff_id = int(get_jwt_identity())
        
        if not admin_only() and trek.staff_id != staff_id:
            return jsonify({"message": "Access Denied. You are not assigned to this trek."}), 403
            
        bookings = Booking.query.filter_by(trek_id=trek_id).all()
        participants = []
        for b in bookings:
            u = User.query.get(b.user_id)
            if u:
                participants.append({
                    "booking_id": b.id,
                    "user_id": u.id,
                    "username": u.username,
                    "email": u.email,
                    "booking_status": b.status,
                    "booking_date": b.booking_date.strftime('%Y-%m-%d') if b.booking_date else None
                })
        return jsonify(participants), 200
    
    #user(trekker) endpoints

    @app.route('/api/user/profile', methods=['GET', 'PUT'])
    @jwt_required()
    def user_profile():
        user_id = int(get_jwt_identity())
        user = User.query.get_or_404(user_id)
        
        if request.method == 'GET':
            return jsonify({
                "username": user.username,
                "email": user.email,
                "role": user.role
            }), 200
            
        elif request.method == 'PUT':
            data = request.get_json() or {}
            
            if 'username' in data:
                new_username = data['username'].strip()
                
                # Check if username is taken by ANYONE ELSE
                if new_username.lower() != user.username.lower():
                    existing_user = User.query.filter(func.lower(User.username) == new_username.lower()).first()
                    if existing_user:
                        return jsonify({"message": "Username is already taken."}), 400
                
                user.username = new_username
                
            if 'password' in data and data['password'].strip():
                user.password_hash = generate_password_hash(data['password'])
                
            db.session.commit()
            return jsonify({"message": "Profile updated successfully."}), 200

    @app.route('/api/treks/search', methods=['GET'])
    @cache.cached(timeout=60, query_string=True)
    def user_browse_treks():
        
        query = Trek.query.filter(Trek.status.ilike("open"))
        
        
        search = request.args.get('search')
        difficulty = request.args.get('difficulty')
        location = request.args.get('location')
        max_duration = request.args.get('duration')
        
        if search:
            query = query.filter((Trek.title.like(f"%{search}%")) | (Trek.location.like(f"%{search}%")))
        if difficulty:
            query = query.filter(Trek.difficulty.ilike(difficulty))
        if location:
            query = query.filter(Trek.location.like(f"%{location}%"))
        if max_duration:
            try: 
                duration_val = int(max_duration)
                query = query.filter(Trek.duration_days <= duration_val) 
            except ValueError:
                return jsonify({"message": "Duration must be a valid integer."}), 400
            
        treks = query.all()
        return jsonify([{
            "id": t.id,
            "title": t.title,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration_days": t.duration_days,
            "available_slots": t.available_slots,
            "price": t.price,
            "start_date": t.start_date.strftime('%Y-%m-%d') if t.start_date else None,
            "end_date": t.end_date.strftime('%Y-%m-%d') if t.end_date else None
        } for t in treks]), 200

    @app.route('/api/bookings', methods=['POST'])
    @jwt_required()
    def book_trek():
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        trek_id = data.get('trek_id')
        
        if not trek_id:
            return jsonify({"message": "Trek ID Required"}), 400
            
        trek = Trek.query.get_or_404(trek_id)
        
        
        if trek.status.lower() != OPEN_STATUS:
            return jsonify({"message": "This trek is closed for bookings."}), 400
            
        
        existing_booking = Booking.query.filter_by(user_id=user_id, trek_id=trek_id, status=BOOKED_STATUS).first()
        if existing_booking:
            return jsonify({"message": "You already booked this trek."}), 400
            
        
        if trek.available_slots <= 0:
            return jsonify({"message": "Booking failed. Slots are completely sold out."}), 400
            
        
        trek.available_slots -= 1
        
        new_booking = Booking(
            user_id=user_id,
            trek_id=trek_id,
            booking_date=date.today(),
            status=BOOKED_STATUS
        )
        
        db.session.add(new_booking)
        db.session.commit()
        clear_trek_cache()
        return jsonify({"message": "Trek booked successfully"}), 201

    @app.route('/api/user/bookings', methods=['GET'])
    @jwt_required()
    def user_booking_history():
        user_id = int(get_jwt_identity())
        bookings = Booking.query.filter_by(user_id=user_id).all()
        
        output = []
        for b in bookings:
            trek = Trek.query.get(b.trek_id)
            output.append({
                "booking_id": b.id,
                "trek_id": b.trek_id,
                "trek_name": trek.title if trek else "Unknown Trek",
                "location": trek.location if trek else "N/A",
                "booking_date": b.booking_date.strftime('%Y-%m-%d') if b.booking_date else None,
                "status": b.status,
                "start_date": trek.start_date.strftime('%Y-%m-%d') if (trek and trek.start_date) else None
            })
        return jsonify(output), 200

    @app.route('/api/user/bookings/export', methods=['POST'])
    @jwt_required()
    def export_user_booking_history():
        user_id = int(get_jwt_identity())
        user = User.query.get_or_404(user_id)
        task = tasks.celery.send_task("tasks.export_booking_csv", args=[user.id, user.email])
        return jsonify({
            "message": "Booking history export queued. You will receive the CSV by email.",
            "task_id": task.id
        }), 202

    @app.route('/api/bookings/<int:booking_id>/cancel', methods=['PATCH'])
    @jwt_required()
    def cancel_booking(booking_id):
        user_id = int(get_jwt_identity())
        booking = Booking.query.get_or_404(booking_id)
        
        if booking.user_id != user_id:
            return jsonify({"message": "Unauthorized action."}), 401
            
        if booking.status == "Cancelled":
            return jsonify({"message": "Booking is already cancelled."}), 400
            
        
        trek = Trek.query.with_for_update().get_or_404(booking.trek_id) #locking the db so overbooking is prevented by 2 users 
        if trek.start_date and trek.start_date <= date.today():
            return jsonify({"message": "Cannot cancel a trek that has already started or completed."}), 400
            
        
        trek.available_slots += 1
        booking.status = "Cancelled"
        db.session.commit()
        clear_trek_cache()
        return jsonify({"message": "Reservation cancelled successfully. Slot freed."}), 200
    
