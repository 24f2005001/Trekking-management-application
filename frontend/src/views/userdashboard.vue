<template>
  <div class="container-fluid bg-dark text-white min-vh-100">
    <div class="row">
      <nav class="col-md-3 col-lg-2 d-md-block sidebar px-0 position-fixed start-0 top-0 bottom-0 collapse" id="sidebarMenu">
        <div class="p-3 border-bottom border-secondary-subtle">
          <span class="fs-5 heading-font fw-bold text-mint d-flex align-items-center gap-2">
            <i class="ti ti-mountain"></i> Trekker Panel
          </span>
        </div>

        <div class="pt-3">
          <h6 class="px-3 text-uppercase text-mint opacity-50 small font-monospace" style="font-size: 0.7rem; letter-spacing: 0.1em;">Explore</h6>
          <ul class="nav flex-column mb-3">
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'dashboard' }" @click.prevent="currentTab = 'dashboard'">
                <i class="ti ti-layout-dashboard"></i> Dashboard
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'treks' }" @click.prevent="currentTab = 'treks'">
                <i class="ti ti-map-search"></i> Available Treks
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'bookings' }" @click.prevent="currentTab = 'bookings'">
                <i class="ti ti-ticket"></i> My Bookings
              </a>
            </li>
          </ul>

          <h6 class="px-3 text-uppercase text-mint opacity-50 small font-monospace" style="font-size: 0.7rem; letter-spacing: 0.1em;">Account</h6>
          <ul class="nav flex-column mb-4">
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'profile' }" @click.prevent="currentTab = 'profile'">
                <i class="ti ti-user"></i> Profile
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
            {{ pageTitle }}
          </h1>
          <div class="rounded-circle text-dark fw-bold d-flex align-items-center justify-content-center heading-font avatar-glow" style="width: 34px; height: 34px;">
            {{ userInitials }}
          </div>
        </header>

        <div v-if="message" class="alert alert-success py-2">{{ message }}</div>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

        <div v-if="currentTab === 'dashboard'" class="fade-in">
          <div class="py-5 text-center text-secondary">
            <i class="ti ti-mountain fs-1 opacity-20 mb-3"></i>
            <p class="font-monospace">Browse open treks, manage your bookings, and keep your trekking profile updated.</p>
          </div>

          <div class="row g-3">
            <div class="col-md-4">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Available Treks</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ treks.length }}</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Booked Treks</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ activeBookings.length }}</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Completed Treks</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ completedBookings.length }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'treks'" class="fade-in">
          <div class="card bg-dark-panel text-white mb-3">
            <div class="card-header bg-transparent border-secondary-subtle py-3">
              <h5 class="card-title mb-0 heading-font text-mint fs-6">Search & Filter Treks</h5>
            </div>
            <div class="card-body">
              <form class="row g-3" @submit.prevent="fetchTreks">
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Search</label>
                  <input type="text" v-model="filters.search" class="form-control bg-transparent text-white border-secondary" placeholder="Name or location">
                </div>
                <div class="col-md-3">
                  <label class="form-label small text-mint font-monospace">Difficulty</label>
                  <select v-model="filters.difficulty" class="form-select bg-dark text-white border-secondary">
                    <option value="">All</option>
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label small text-mint font-monospace">Max Duration</label>
                  <input type="number" min="1" v-model="filters.duration" class="form-control bg-transparent text-white border-secondary" placeholder="Days">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                  <button type="submit" class="btn btn-sm btn-teal text-white border-0 w-100" style="background-color:#0a9396;">Apply</button>
                </div>
              </form>
            </div>
          </div>

          <div class="card bg-dark-panel text-white">
            <div class="table-responsive">
              <table class="table table-dark-custom align-middle mb-0">
                <thead>
                  <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size:0.7rem;">
                    <th>Trek</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <th>Slots</th>
                    <th>Dates</th>
                    <th>Price</th>
                    <th class="text-end">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="trek in treks" :key="trek.id">
                    <td class="fw-medium text-white">{{ trek.title }}</td>
                    <td>{{ trek.location }}</td>
                    <td>
                      <span class="badge font-monospace" :class="getDifficultyClass(trek.difficulty)">
                        {{ trek.difficulty }}
                      </span>
                    </td>
                    <td>{{ trek.duration_days }} Days</td>
                    <td>{{ trek.available_slots }}</td>
                    <td style="font-size:0.75rem;">
                      <div>{{ trek.start_date }}</div>
                      <div v-if="trek.end_date">to {{ trek.end_date }}</div>
                    </td>
                    <td>₹{{ trek.price }}</td>
                    <td class="text-end">
                      <button class="btn btn-sm btn-outline-success" :disabled="isAlreadyBooked(trek.id) || trek.available_slots <= 0" @click="bookTrek(trek.id)">
                        {{ isAlreadyBooked(trek.id) ? 'Booked' : 'Book' }}
                      </button>
                    </td>
                  </tr>
                  <tr v-if="treks.length === 0">
                    <td colspan="8" class="text-center py-4 text-secondary">No open treks match your search.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'bookings'" class="fade-in">
          <div class="card bg-dark-panel text-white">
            <div class="card-header bg-transparent border-secondary-subtle py-3 d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0 heading-font text-mint fs-6">Booking Status & Trekking History</h5>
              <button class="btn btn-sm btn-outline-success" @click="exportBookings" :disabled="bookings.length === 0">
                <i class="ti ti-download"></i> Export CSV
              </button>
            </div>
            <div class="table-responsive">
              <table class="table table-dark-custom align-middle mb-0">
                <thead>
                  <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size:0.7rem;">
                    <th>Booking</th>
                    <th>Trek</th>
                    <th>Location</th>
                    <th>Booking Date</th>
                    <th>Start Date</th>
                    <th>Status</th>
                    <th class="text-end">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="booking in bookings" :key="booking.booking_id">
                    <td class="font-monospace text-secondary">#BKG-{{ booking.booking_id }}</td>
                    <td class="fw-medium text-white">{{ booking.trek_name }}</td>
                    <td>{{ booking.location }}</td>
                    <td>{{ booking.booking_date }}</td>
                    <td>{{ booking.start_date }}</td>
                    <td>
                      <span class="badge font-monospace" :class="getBookingStatusClass(booking.status)">
                        {{ booking.status }}
                      </span>
                    </td>
                    <td class="text-end">
                      <button v-if="booking.status === 'Booked'" class="btn btn-sm btn-outline-danger" @click="cancelBooking(booking.booking_id)">
                        Cancel
                      </button>
                      <span v-else class="text-secondary small">History</span>
                    </td>
                  </tr>
                  <tr v-if="bookings.length === 0">
                    <td colspan="7" class="text-center py-4 text-secondary">No bookings yet.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'profile'" class="fade-in">
          <div class="card bg-dark-panel text-white">
            <div class="card-header bg-transparent border-secondary-subtle py-3">
              <h5 class="card-title mb-0 heading-font text-mint fs-6">Edit Profile</h5>
            </div>
            <form @submit.prevent="saveProfile">
              <div class="card-body">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label small text-mint font-monospace">Username</label>
                    <input type="text" v-model="profileForm.username" class="form-control bg-transparent text-white border-secondary" required>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label small text-mint font-monospace">Email</label>
                    <input type="email" v-model="profileForm.email" class="form-control bg-transparent text-white border-secondary" disabled>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label small text-mint font-monospace">New Password</label>
                    <input type="password" v-model="profileForm.password" class="form-control bg-transparent text-white border-secondary" placeholder="Leave blank to keep current password">
                  </div>
                </div>
              </div>
              <div class="card-footer bg-transparent border-secondary-subtle text-end">
                <button type="submit" class="btn btn-sm btn-teal text-white border-0 px-3" style="background-color:#0a9396;">Save Profile</button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import API from '../api'

const router = useRouter()

const currentTab = ref('dashboard')
const treks = ref([])
const bookings = ref([])
const message = ref('')
const error = ref('')
const filters = ref({
  search: '',
  difficulty: '',
  duration: ''
})
const profileForm = ref({
  username: '',
  email: '',
  password: ''
})

const getAuthConfig = () => {
  const token = localStorage.getItem('admin_token')
  if (!token) {
    router.push('/login')
    return null
  }
  return {
    headers: { Authorization: `Bearer ${token}` }
  }
}

const pageTitle = computed(() => {
  if (currentTab.value === 'treks') return 'Available Treks'
  if (currentTab.value === 'bookings') return 'My Bookings'
  if (currentTab.value === 'profile') return 'Profile'
  return 'Dashboard'
})

const userInitials = computed(() => {
  return profileForm.value.username ? profileForm.value.username.slice(0, 1).toUpperCase() : 'U'
})

const activeBookings = computed(() => bookings.value.filter(booking => booking.status === 'Booked'))
const completedBookings = computed(() => bookings.value.filter(booking => booking.status === 'Completed'))

const clearAlerts = () => {
  message.value = ''
  error.value = ''
}

const fetchProfile = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await API.get('/user/profile', config)
    profileForm.value = {
      username: res.data.username,
      email: res.data.email,
      password: ''
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load profile.'
  }
}

const fetchTreks = async () => {
  clearAlerts()

  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.difficulty) params.difficulty = filters.value.difficulty
    if (filters.value.duration) params.duration = filters.value.duration

    const res = await API.get('/treks/search', { params })
    treks.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load available treks.'
  }
}

const fetchBookings = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await API.get('/user/bookings', config)
    bookings.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load booking history.'
  }
}

const refreshDashboard = async () => {
  await Promise.all([
    fetchProfile(),
    fetchTreks(),
    fetchBookings()
  ])
}

const bookTrek = async (trekId) => {
  clearAlerts()
  const config = getAuthConfig()
  if (!config) return

  try {
    await API.post('/bookings', { trek_id: trekId }, config)
    message.value = 'Trek booked successfully.'
    await refreshDashboard()
    currentTab.value = 'bookings'
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to book this trek.'
  }
}

const cancelBooking = async (bookingId) => {
  clearAlerts()
  const config = getAuthConfig()
  if (!config) return

  try {
    await API.patch(`/bookings/${bookingId}/cancel`, {}, config)
    message.value = 'Booking cancelled successfully.'
    await refreshDashboard()
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to cancel this booking.'
  }
}

const exportBookings = async () => {
  clearAlerts()
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await API.post('/user/bookings/export', {}, config)
    message.value = res.data.message || 'Export job queued. You will receive the CSV by email.'
    pollJob(res.data.task_id, 'CSV export completed. Please check your email.')
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to export booking history.'
  }
}

const pollJob = async (taskId, successMessage) => {
  if (!taskId) return
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await API.get(`/jobs/${taskId}`, config)
    if (!res.data.ready) {
      setTimeout(() => pollJob(taskId, successMessage), 2000)
      return
    }

    if (res.data.state === 'SUCCESS') {
      message.value = successMessage
    } else {
      error.value = res.data.error || 'Background job failed.'
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to check export status.'
  }
}

const saveProfile = async () => {
  clearAlerts()
  const config = getAuthConfig()
  if (!config) return

  const payload = {
    username: profileForm.value.username
  }

  if (profileForm.value.password.trim()) {
    payload.password = profileForm.value.password
  }

  try {
    await API.put('/user/profile', payload, config)
    message.value = 'Profile updated successfully.'
    await fetchProfile()
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to update profile.'
  }
}

const isAlreadyBooked = (trekId) => {
  return bookings.value.some(booking => booking.trek_id === trekId && booking.status === 'Booked')
}

const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('user_role')
  router.push('/login')
}

const getDifficultyClass = (diff) => {
  if (diff === 'Hard') return 'bg-danger bg-opacity-15 text-danger'
  if (diff === 'Easy') return 'bg-success bg-opacity-15 text-mint'
  return 'bg-warning bg-opacity-40 text-dark'
}

const getBookingStatusClass = (status) => {
  switch(status) {
    case 'Booked': return 'bg-success'
    case 'Cancelled': return 'bg-danger'
    case 'Completed': return 'bg-info text-dark'
    default: return 'bg-secondary'
  }
}

onMounted(() => {
  refreshDashboard()
})
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
