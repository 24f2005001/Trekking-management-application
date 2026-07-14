<template>
  <div class="container-fluid bg-dark text-white min-vh-100">
    <div class="row">
      
      <nav class="col-md-3 col-lg-2 d-md-block sidebar px-0 position-fixed start-0 top-0 bottom-0 collapse" id="sidebarMenu">
        <div class="p-3 border-bottom border-secondary-subtle">
          <span class="fs-5 heading-font fw-bold text-mint d-flex align-items-center gap-2">
            <i class="ti ti-mountain"></i> Trek Admin
          </span>
        </div>
        
        <div class="pt-3">
          <h6 class="px-3 text-uppercase text-mint opacity-50 small font-monospace" style="font-size: 0.7rem; letter-spacing: 0.1em;">Overview</h6>
          <ul class="nav flex-column mb-3">
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'dashboard' }" @click.prevent="currentTab = 'dashboard'">
                <i class="ti ti-layout-dashboard"></i> Dashboard
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'analytics' }" @click.prevent="currentTab = 'analytics'">
                <i class="ti ti-chart-bar"></i> Analytics
              </a>
            </li>
          </ul>

          <h6 class="px-3 text-uppercase text-mint opacity-50 small font-monospace" style="font-size: 0.7rem; letter-spacing: 0.1em;">Manage</h6>
          <ul class="nav flex-column mb-3">
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'treks' }" @click.prevent="currentTab = 'treks'">
                <i class="ti ti-map-pin"></i> Treks
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'staff' }" @click.prevent="currentTab = 'staff'">
                <i class="ti ti-users"></i> Staff & Trekkers
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'bookings' }" @click.prevent="currentTab = 'bookings'">
                <i class="ti ti-ticket"></i> Bookings
              </a>
            </li>
          </ul>

          <h6 class="px-3 text-uppercase text-mint opacity-50 small font-monospace" style="font-size: 0.7rem; letter-spacing: 0.1em;">System</h6>
          <ul class="nav flex-column mb-4">
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'reports' }" @click.prevent="currentTab = 'reports'">
                <i class="ti ti-file-report"></i> Reports
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" @click.prevent="logout">
                <i class="ti ti-logout"></i> Logout
              </a>
            </li>
          </ul>
        </div>
      </nav>

      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 pt-3 pb-5">
        
        <header class="d-flex justify-content-between align-items-center pb-3 mb-4 border-bottom border-secondary-subtle">
          <h1 class="h4 heading-font fw-bold mb-0 text-capitalize">
            {{ currentTab === 'staff' ? 'Staff & Trekkers Management' : currentTab }}
          </h1>
          <div class="d-flex align-items-center gap-3">
            <div class="input-group search-input-group px-2 py-1 align-items-center" style="width: 260px;">
              <i class="ti ti-search text-mint opacity-50 me-1"></i>
              <input type="text" v-model="searchQuery" class="form-control text-white" placeholder="Search...">
            </div>
            <div class="rounded-circle text-dark fw-bold d-flex align-items-center justify-content-center heading-font avatar-glow" style="width: 34px; height: 34px;">
              {{ adminInitials }}
            </div>
          </div>
        </header>

        <div v-if="adminMessage" class="alert alert-success py-2">{{ adminMessage }}</div>
        <div v-if="adminError" class="alert alert-danger py-2">{{ adminError }}</div>

        <div v-if="currentTab === 'dashboard' || currentTab === 'analytics'" class="py-5 text-center text-secondary">
          <i class="ti ti-folder-open fs-1 opacity-20 mb-3"></i>
          <p class="font-monospace">Welcome to the Admin Panel. Use the sidebar navigation menu to view active trek data models.</p>
          <div class="row g-3 justify-content-center mt-4">
            <div class="col-md-3">
              <div class="card bg-dark-panel p-3 text-start">
                <h6 class="text-mint opacity-70 small text-uppercase">Total Treks</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ dashboardStats.total_treks }}</p>
              </div>
            </div>
            <div class="col-md-3">
              <div class="card bg-dark-panel p-3 text-start">
                <h6 class="text-mint opacity-70 small text-uppercase">Total Users</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ dashboardStats.total_users }}</p>
              </div>
            </div>
            <div class="col-md-3">
              <div class="card bg-dark-panel p-3 text-start">
                <h6 class="text-mint opacity-70 small text-uppercase">Total Staff</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ dashboardStats.total_staff }}</p>
              </div>
            </div>
            <div class="col-md-3">
              <div class="card bg-dark-panel p-3 text-start">
                <h6 class="text-mint opacity-70 small text-uppercase">Total Bookings</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ dashboardStats.total_bookings }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'treks'" class="fade-in">
          <div class="card bg-dark-panel text-white">
            <div class="card-header bg-transparent border-secondary-subtle d-flex justify-content-between align-items-center py-3">
              <h5 class="card-title mb-0 heading-font text-mint fs-6">Manage Trekking Routes</h5>
              <button @click="openAddModal" class="btn btn-sm btn-teal text-white border-0 bg-gradient font-monospace p-1 px-2" style="background-color: #0a9396; font-size: 0.75rem;">
                <i class="ti ti-plus"></i> Create Route
              </button>
            </div>
            
            <div class="table-responsive">
              <table class="table table-dark-custom align-middle mb-0">
                <thead>
                  <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size: 0.7rem; letter-spacing: 0.05em;">
                    <th>Title</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <th>Slots</th>
                    <th>Price</th>
                    <th>Dates</th>
                    <th>Status</th>
                    <th class="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="trek in filteredTreks" :key="trek.id">
                    <td class="fw-medium text-white">{{ trek.title }}</td>
                    <td>{{ trek.location }}</td>
                    <td>
                      <span :class="['badge small font-monospace', getDifficultyClass(trek.difficulty)]" style="font-size: 0.7rem;">
                        {{ trek.difficulty }}
                      </span>
                    </td>
                    <td>{{ trek.duration_days }} Days</td>
                    <td>{{ trek.available_slots }} / {{ trek.total_slots }}</td>
                    <td>₹{{ trek.price }}</td>
                    <td style="font-size: 0.75rem;">
                      <div>{{ trek.start_date }}</div>
                      <div>to {{ trek.end_date }}</div>
                    </td>
                    <td>
                      <span :class="['badge font-monospace', getStatusClass(trek.status)]" style="font-size: 0.7rem;">
                        {{ trek.status }}
                      </span>
                    </td>
                    <td class="text-end">
                      <div class="btn-group">
                        <button @click="openEditModal(trek)" class="btn btn-sm btn-link text-mint p-1" title="Edit Route"><i class="ti ti-edit"></i></button>
                        <button @click="deleteTrekRoute(trek.id)" class="btn btn-sm btn-link text-danger p-1" title="Remove Route"><i class="ti ti-trash"></i></button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="filteredTreks.length === 0">
                    <td colspan="9" class="text-center py-4 text-secondary">No trekking routes found in database.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'staff'" class="fade-in">
          <div class="d-flex justify-content-between align-items-center mb-3">

            <h5 class="card-title mb-0 heading-font text-mint fs-6">Manage User Accounts</h5>

            <button
              @click="openStaffModal"
              class="btn btn-sm btn-teal text-white border-0 font-monospace"
              style="background-color:#0a9396;font-size:0.75rem;"
            >
              <i class="ti ti-user-plus"></i>
              Add Staff
            </button>

          </div>

          <div class="card bg-dark-panel text-white">

            <div class="table-responsive">
              <table class="table table-dark-custom align-middle mb-0">

                <thead>
                  <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size:0.7rem;">
                    <th>User ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th class="text-end">Actions</th>
                  </tr>
                </thead>

                <tbody>

                  <tr v-for="member in filteredUsers" :key="member.id">
                    <td class="font-monospace text-mint">
                      #USR-{{ member.id }}
                    </td>

                    <td class="fw-medium text-white">
                      {{ member.username }}
                    </td>

                    <td>
                      {{ member.email }}
                    </td>

                    <td>
                      <span class="badge bg-secondary">
                        {{ getRoleLabel(member.role) }}
                      </span>
                    </td>

                    <td>
                      <span
                        class="badge"
                        :class="member.is_active ? 'bg-success' : 'bg-danger'"
                      >
                        {{ member.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </td>

                    <td class="text-end">
                      <button
                        v-if="member.role !== 'admin'"
                        @click="toggleUserStatus(member)"
                        class="btn btn-sm"
                        :class="member.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                        style="font-size:0.75rem;padding:2px 8px;"
                      >
                        {{ member.is_active ? 'Deactivate' : 'Activate' }}
                      </button>
                      <span v-else class="text-secondary small">Protected</span>
                    </td>
                  </tr>

                  <tr v-if="filteredUsers.length === 0">
                    <td colspan="6" class="text-center py-4 text-secondary">
                      No user accounts found.
                    </td>
                  </tr>

                </tbody>

              </table>
            </div>

          </div>
        </div>





        <div v-if="currentTab === 'bookings'" class="fade-in">
          <div class="card bg-dark-panel text-white">
            <div class="card-header bg-transparent border-secondary-subtle py-3">
              <h5 class="card-title mb-0 heading-font text-mint fs-6">Master Ledger Cross-Reference</h5>
            </div>
            <div class="table-responsive">
              <table class="table table-dark-custom align-middle mb-0">
                <thead>
                  <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size: 0.7rem;">
                    <th>ID</th>
                    <th>Trek Target</th>
                    <th>Trekker Profile</th>
                    <th>Transaction Date</th>
                    <th>Reservation Status</th>
                    <th>Financial Audit</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="booking in filteredBookings" :key="booking.booking_id">
                    <td class="font-monospace text-secondary">#BKG-{{ booking.booking_id }}</td>
                    <td class="fw-medium text-white">{{ booking.trek_name }}</td>
                    <td>
                      <div>{{ booking.username }}</div>
                      <small class="text-secondary font-monospace" style="font-size: 0.7rem;">ID: {{ booking.user_id }}</small>
                    </td>
                    <td>{{ booking.booking_date }}</td>
                    <td>
                      <span class="badge font-monospace" :class="getBookingStatusClass(booking.status)">
                        {{ booking.status }}
                      </span>
                    </td>
                    <td>
                      <span class="badge bg-opacity-10" :class="booking.payment_status === 'Paid' ? 'bg-success text-success' : 'bg-warning text-warning'">
                        {{ booking.payment_status || 'Unverified' }}
                      </span>
                    </td>
                  </tr>
                  <tr v-if="filteredBookings.length === 0">
                    <td colspan="6" class="text-center py-4 text-secondary">No transaction bookings structural metadata records logged.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'reports'" class="fade-in">
          <div class="d-flex justify-content-end gap-2 mb-3">
            <button class="btn btn-sm btn-outline-success" @click="triggerMonthlyReport">
              <i class="ti ti-mail"></i> Email Monthly Report
            </button>
            <button class="btn btn-sm btn-outline-info" @click="triggerDailyReminders">
              <i class="ti ti-bell"></i> Send Reminders
            </button>
          </div>

          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Treks Conducted</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ reportData.completed_treks || 0 }}</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Users Participated</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ reportData.participating_users || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="row g-3">
            <div class="col-lg-6">
              <div class="card bg-dark-panel text-white">
                <div class="card-header bg-transparent border-secondary-subtle py-3">
                  <h5 class="card-title mb-0 heading-font text-mint fs-6">Popular Treks</h5>
                </div>
                <div class="table-responsive">
                  <table class="table table-dark-custom align-middle mb-0">
                    <thead>
                      <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size:0.7rem;">
                        <th>Trek</th>
                        <th>Location</th>
                        <th class="text-end">Bookings</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="trek in reportData.popular_treks" :key="trek.id">
                        <td class="fw-medium text-white">{{ trek.title }}</td>
                        <td>{{ trek.location }}</td>
                        <td class="text-end">{{ trek.booking_count }}</td>
                      </tr>
                      <tr v-if="!reportData.popular_treks?.length">
                        <td colspan="3" class="text-center py-4 text-secondary">No report data yet.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <div class="col-lg-6">
              <div class="card bg-dark-panel text-white">
                <div class="card-header bg-transparent border-secondary-subtle py-3">
                  <h5 class="card-title mb-0 heading-font text-mint fs-6">Status Summary</h5>
                </div>
                <div class="table-responsive">
                  <table class="table table-dark-custom align-middle mb-0">
                    <thead>
                      <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size:0.7rem;">
                        <th>Type</th>
                        <th>Status</th>
                        <th class="text-end">Count</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="row in reportStatusRows" :key="`${row.type}-${row.status}`">
                        <td>{{ row.type }}</td>
                        <td>{{ row.status }}</td>
                        <td class="text-end">{{ row.count }}</td>
                      </tr>
                      <tr v-if="reportStatusRows.length === 0">
                        <td colspan="3" class="text-center py-4 text-secondary">No status data yet.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>



      </main>
    </div>

    <div v-if="showModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.7);" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark border-secondary-subtle text-white">
          <div class="modal-header border-secondary-subtle">
            <h5 class="modal-title heading-font text-mint">{{ isEditMode ? 'Update Trek Route' : 'Create New Trek Route' }}</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
          </div>
          <form @submit.prevent="saveTrekRoute">
            <div class="modal-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label small text-mint font-monospace">Trek Title</label>
                  <input type="text" v-model="form.title" class="form-control bg-transparent text-white border-secondary" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label small text-mint font-monospace">Location</label>
                  <input type="text" v-model="form.location" class="form-control bg-transparent text-white border-secondary" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Difficulty</label>
                  <select v-model="form.difficulty" class="form-select bg-dark text-white border-secondary">
                    <option value="Easy">Easy</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Duration (Days)</label>
                  <input type="number" v-model="form.duration_days" class="form-control bg-transparent text-white border-secondary" min="1" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Price (₹)</label>
                  <input type="number" step="0.01" v-model="form.price" class="form-control bg-transparent text-white border-secondary" min="0" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label small text-mint font-monospace">Start Date</label>
                  <input type="date" v-model="form.start_date" class="form-control bg-transparent text-white border-secondary" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label small text-mint font-monospace">End Date</label>
                  <input type="date" v-model="form.end_date" class="form-control bg-transparent text-white border-secondary" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Total Slots</label>
                  <input type="number" v-model="form.total_slots" class="form-control bg-transparent text-white border-secondary" min="1" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Assigned Staff</label>
                  <select v-model="form.staff_id" class="form-select bg-dark text-white border-secondary">
                    <option :value="null">Unassigned</option>
                    <option v-for="staff in activeStaffUsers" :key="staff.id" :value="staff.id">
                      {{ staff.username }} (#{{ staff.id }})
                    </option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Status</label>
                  <select v-model="form.status" class="form-select bg-dark text-white border-secondary">
                    <option value="pending">Pending</option>
                    <option value="open">Open</option>
                    <option value="closed">Closed</option>
                    <option value="started">Started</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="modal-footer border-secondary-subtle">
              <button type="button" class="btn btn-sm btn-outline-secondary text-white" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-sm btn-teal text-white border-0 px-3" style="background-color: #0a9396;">Save Route</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showStaffModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.7);" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark border-secondary-subtle text-white">
          <div class="modal-header border-secondary-subtle">
            <h5 class="modal-title heading-font text-mint">Add Trek Staff</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeStaffModal"></button>
          </div>
          <form @submit.prevent="saveStaffAccount">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label small text-mint font-monospace">Username</label>
                <input type="text" v-model="staffForm.username" class="form-control bg-transparent text-white border-secondary" required>
              </div>
              <div class="mb-3">
                <label class="form-label small text-mint font-monospace">Email</label>
                <input type="email" v-model="staffForm.email" class="form-control bg-transparent text-white border-secondary" required>
              </div>
              <div class="mb-0">
                <label class="form-label small text-mint font-monospace">Password</label>
                <input type="password" v-model="staffForm.password" class="form-control bg-transparent text-white border-secondary" required>
              </div>
            </div>
            <div class="modal-footer border-secondary-subtle">
              <button type="button" class="btn btn-sm btn-outline-secondary text-white" @click="closeStaffModal">Cancel</button>
              <button type="submit" class="btn btn-sm btn-teal text-white border-0 px-3" style="background-color: #0a9396;">Create Staff</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/admin'
const API_ROOT_URL = 'http://127.0.0.1:5000/api'


const currentTab = ref('dashboard')
const searchQuery = ref('')
const adminInitials = ref('A')
const adminMessage = ref('')
const adminError = ref('')

                                
const treks = ref([])

// Form layout states
const users = ref([])                  // Unified users table; staff are users with role = 'staff'
const bookings = ref([])               // All bookings (Admin view)
const stats = ref(null)                // Dashboard statistics (treks, users, staff, bookings)
const reportData = ref({
  completed_treks: 0,
  participating_users: 0,
  popular_treks: [],
  booking_status_counts: [],
  trek_status_counts: []
})
const showModal = ref(false)
const showStaffModal = ref(false)
const isEditMode = ref(false)
const targetEditId = ref(null)
const form = ref({
  title: '',
  location: '',
  difficulty: 'Easy',
  duration_days: 1,
  total_slots: 30,
  price: 0.0,
  start_date: '',
  end_date: '',
  staff_id: null,
  status: 'pending'
})
const staffForm = ref({
  username: '',
  email: '',
  password: ''
})


const getAuthConfig = () => {
  const token = localStorage.getItem('admin_token')
  if (!token) {
    alert('Session missing or expired. Access denied.')
    window.location.href = '/login' 
    return null
  }
  return {
    headers: { Authorization: `Bearer ${token}` }
  }
}

const clearAdminAlerts = () => {
  adminMessage.value = ''
  adminError.value = ''
}


const fetchTreksData = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.get(`${API_BASE_URL}/treks`, config)
    treks.value = res.data
  } catch (error) {
    console.error('Error hydrating trek data array:', error)
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      alert('Unauthorized access. Please login with structural administrative privileges.')
      window.location.href = '/login'
    }
  }
}

const fetchStatsData = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.get(`${API_BASE_URL}/stats`, config)
    stats.value = res.data
  } catch (error) {
    console.error('Error fetching admin stats:', error)
  }
}

const fetchUsersData = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.get(`${API_BASE_URL}/users`, config)
    users.value = res.data
  } catch (error) {
    console.error('Error fetching user accounts:', error)
  }
}

const fetchBookingsData = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.get(`${API_BASE_URL}/bookings`, config)
    bookings.value = res.data
  } catch (error) {
    console.error('Error fetching booking records:', error)
  }
}

const fetchReportsData = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.get(`${API_BASE_URL}/reports`, config)
    reportData.value = res.data
  } catch (error) {
    console.error('Error fetching admin reports:', error)
  }
}

const refreshAdminData = async () => {
  await Promise.all([
    fetchTreksData(),
    fetchStatsData(),
    fetchUsersData(),
    fetchBookingsData(),
    fetchReportsData()
  ])
}

// Lifecycle Initialization Hook
onMounted(() => {
  refreshAdminData()
})


const filteredTreks = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  if (!query) return treks.value
  return treks.value.filter(t => 
    t.title.toLowerCase().includes(query) ||
    t.location.toLowerCase().includes(query)
  )
})

const filteredUsers = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  const visibleUsers = users.value.filter(user => user.role !== 'admin')

  if (!query) return visibleUsers

  return visibleUsers.filter(user =>
    user.username.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query) ||
    user.role.toLowerCase().includes(query)
  )
})

const filteredBookings = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  if (!query) return bookings.value

  return bookings.value.filter(booking =>
    String(booking.booking_id).includes(query) ||
    booking.trek_name.toLowerCase().includes(query) ||
    booking.username.toLowerCase().includes(query) ||
    booking.status.toLowerCase().includes(query)
  )
})

const dashboardStats = computed(() => {
  const staffCount = users.value.filter(user => user.role === 'staff').length
  const trekkerCount = users.value.filter(user => user.role === 'trekker' || user.role === 'user').length

  return {
    total_treks: stats.value?.total_treks ?? treks.value.length,
    total_users: trekkerCount || stats.value?.total_users || 0,
    total_staff: staffCount || stats.value?.total_staff || 0,
    total_bookings: stats.value?.total_bookings ?? bookings.value.length
  }
})

const activeStaffUsers = computed(() => {
  return users.value.filter(user => user.role === 'staff' && user.is_active)
})

const reportStatusRows = computed(() => {
  const trekRows = (reportData.value.trek_status_counts || []).map(row => ({
    type: 'Trek',
    status: row.status,
    count: row.count
  }))
  const bookingRows = (reportData.value.booking_status_counts || []).map(row => ({
    type: 'Booking',
    status: row.status,
    count: row.count
  }))
  return [...trekRows, ...bookingRows]
})


const openAddModal = () => {
  isEditMode.value = false
  form.value = { 
    title: '', 
    location: '', 
    difficulty: 'Easy', 
    duration_days: 1, 
    total_slots: 30, 
    price: 0.0,
    start_date: '',
    end_date: '',
    staff_id: null,
    status: 'pending' 
  }
  showModal.value = true
}

const openEditModal = (trek) => {
  isEditMode.value = true
  targetEditId.value = trek.id
  form.value = { ...trek }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const openStaffModal = () => {
  staffForm.value = {
    username: '',
    email: '',
    password: ''
  }
  showStaffModal.value = true
}

const closeStaffModal = () => {
  showStaffModal.value = false
}

const saveTrekRoute = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    if (isEditMode.value) {
      await axios.put(`${API_BASE_URL}/treks/${targetEditId.value}`, form.value, config)
    } else {
      await axios.post(`${API_BASE_URL}/treks`, form.value, config)
    }
    closeModal()
    await refreshAdminData()
  } catch (error) {
    alert(error.response?.data?.message || 'Error compiling backend transaction data for layout update.')
  }
}

const saveStaffAccount = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    await axios.post(`${API_BASE_URL}/staff`, staffForm.value, config)
    closeStaffModal()
    await refreshAdminData()
  } catch (error) {
    alert(error.response?.data?.message || 'Error creating staff account.')
  }
}

const deleteTrekRoute = async (id) => {
  const config = getAuthConfig()
  if (!config) return

  if (confirm('Are you absolutely sure you want to completely remove this route entry from the ledger?')) {
    try {
      await axios.delete(`${API_BASE_URL}/treks/${id}`, config)
      await refreshAdminData()
    } catch (error) {
      alert('Error updating server context index record.')
    }
  }
}

const toggleUserStatus = async (user) => {
  const config = getAuthConfig()
  if (!config) return

  try {
    await axios.patch(`${API_BASE_URL}/users/${user.id}/status`, {
      is_active: !user.is_active
    }, config)
    await refreshAdminData()
  } catch (error) {
    alert(error.response?.data?.message || 'Error updating user account status.')
  }
}

const pollJob = async (taskId, successMessage) => {
  if (!taskId) return
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.get(`${API_ROOT_URL}/jobs/${taskId}`, config)
    if (!res.data.ready) {
      setTimeout(() => pollJob(taskId, successMessage), 2000)
      return
    }

    if (res.data.state === 'SUCCESS') {
      adminMessage.value = successMessage
    } else {
      adminError.value = res.data.error || 'Background job failed.'
    }
  } catch (error) {
    adminError.value = error.response?.data?.message || 'Unable to check job status.'
  }
}

const triggerMonthlyReport = async () => {
  clearAdminAlerts()
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.post(`${API_BASE_URL}/jobs/monthly-report`, {}, config)
    adminMessage.value = res.data.message
    pollJob(res.data.task_id, 'Monthly report emailed to admin.')
  } catch (error) {
    adminError.value = error.response?.data?.message || 'Unable to queue monthly report.'
  }
}

const triggerDailyReminders = async () => {
  clearAdminAlerts()
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await axios.post(`${API_BASE_URL}/jobs/daily-reminders`, {}, config)
    adminMessage.value = res.data.message
    pollJob(res.data.task_id, 'Daily reminders sent.')
  } catch (error) {
    adminError.value = error.response?.data?.message || 'Unable to queue daily reminders.'
  }
}

const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('user_role')
  window.location.href = '/login'
}


const getDifficultyClass = (diff) => {
  if (diff === 'Hard') return 'bg-danger bg-opacity-15 text-danger'
  if (diff === 'Easy') return 'bg-success bg-opacity-15 text-mint'
  return 'bg-warning bg-opacity-40 text-dark'
}

const getStatusClass = (status) => {
  switch(status) {
    case 'open': return 'bg-success'
    case 'closed': return 'bg-danger'
    case 'completed': return 'bg-info text-dark'
    default: return 'bg-secondary' // pending
  }
}

const getBookingStatusClass = (status) => {
  switch(status) {
    case 'Booked': return 'bg-success'
    case 'Cancelled': return 'bg-danger'
    case 'Completed': return 'bg-info text-dark'
    default: return 'bg-secondary'
  }
}

const getRoleLabel = (role) => {
  if (role === 'staff') return 'Trek Staff'
  if (role === 'trekker' || role === 'user') return 'Trekker'
  return role
}
</script>

<style scoped>
.heading-font {
  font-family: 'Syne', sans-serif;
}
.bg-dark-panel {
  background: rgba(255, 255, 255, 0.04) !important;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(148, 210, 189, 0.12) !important;
}
.sidebar {
  background: rgba(10, 24, 36, 0.95);
  border-right: 1px solid rgba(148, 210, 189, 0.12);
  min-height: 100vh;
}
.text-mint { color: #94d2bd !important; }
.text-teal { color: #0a9396 !important; }
.nav-link-custom {
  color: rgba(200, 228, 220, 0.6);
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  font-size: 0.85rem;
  border-left: 2px solid transparent;
  transition: all 0.2s;
}
.nav-link-custom:hover, .nav-link-custom.active {
  color: #94d2bd;
  background: rgba(10, 147, 150, 0.15);
  border-left-color: #0a9396;
}
.table-dark-custom {
  --bs-table-bg: transparent;
  --bs-table-color: rgba(200, 228, 220, 0.8);
  --bs-table-border-color: rgba(148, 210, 189, 0.08);
  font-size: 0.85rem;
}
.search-input-group {
  background: rgba(148, 210, 189, 0.07);
  border: 1px solid rgba(148, 210, 189, 0.15);
  border-radius: 8px;
}
.search-input-group input {
  background: transparent;
  border: none;
  color: #e8f5f0;
}
.search-input-group input:focus {
  background: transparent;
  box-shadow: none;
  color: #e8f5f0;
}
.avatar-glow {
  background: linear-gradient(135deg, #0a9396, #94d2bd);
}
.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
