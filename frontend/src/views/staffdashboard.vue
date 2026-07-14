<template>
  <div class="container-fluid bg-dark text-white min-vh-100">
    <div class="row">
      <nav class="col-md-3 col-lg-2 d-md-block sidebar px-0 position-fixed start-0 top-0 bottom-0 collapse" id="sidebarMenu">
        <div class="p-3 border-bottom border-secondary-subtle">
          <span class="fs-5 heading-font fw-bold text-mint d-flex align-items-center gap-2">
            <i class="ti ti-mountain"></i> Staff Panel
          </span>
        </div>

        <div class="pt-3">
          <h6 class="px-3 text-uppercase text-mint opacity-50 small font-monospace" style="font-size: 0.7rem; letter-spacing: 0.1em;">Treks</h6>
          <ul class="nav flex-column mb-3">
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'dashboard' }" @click.prevent="currentTab = 'dashboard'">
                <i class="ti ti-layout-dashboard"></i> Dashboard
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'treks' }" @click.prevent="currentTab = 'treks'">
                <i class="ti ti-map-pin"></i> Assigned Treks
              </a>
            </li>
            <li>
              <a href="#" class="nav-link-custom" :class="{ active: currentTab === 'participants' }" @click.prevent="currentTab = 'participants'">
                <i class="ti ti-users"></i> Participants
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
          <h1 class="h4 heading-font fw-bold mb-0 text-capitalize">{{ pageTitle }}</h1>
          <div class="rounded-circle text-dark fw-bold d-flex align-items-center justify-content-center heading-font avatar-glow" style="width: 34px; height: 34px;">S</div>
        </header>

        <div v-if="message" class="alert alert-success py-2">{{ message }}</div>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

        <div v-if="currentTab === 'dashboard'" class="fade-in">
          <div class="py-5 text-center text-secondary">
            <i class="ti ti-clipboard-list fs-1 opacity-20 mb-3"></i>
            <p class="font-monospace">Manage assigned treks, update slot availability, and review participant lists.</p>
          </div>

          <div class="row g-3">
            <div class="col-md-4">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Assigned Treks</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ treks.length }}</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Registered Users</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ registeredTotal }}</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-dark-panel p-3">
                <h6 class="text-mint opacity-70 small text-uppercase">Completed Treks</h6>
                <p class="fs-3 fw-bold mb-0 text-white">{{ completedTreks }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'treks'" class="fade-in">
          <div class="card bg-dark-panel text-white">
            <div class="card-header bg-transparent border-secondary-subtle py-3">
              <h5 class="card-title mb-0 heading-font text-mint fs-6">Assigned Trek Management</h5>
            </div>
            <div class="table-responsive">
              <table class="table table-dark-custom align-middle mb-0">
                <thead>
                  <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size:0.7rem;">
                    <th>Trek</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Slots</th>
                    <th>Registered</th>
                    <th>Dates</th>
                    <th>Status</th>
                    <th class="text-end">Update</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="trek in treks" :key="trek.id">
                    <td class="fw-medium text-white">{{ trek.title }}</td>
                    <td>{{ trek.location }}</td>
                    <td>{{ trek.difficulty }}</td>
                    <td style="width:120px;">
                      <input type="number" min="0" :max="trek.total_slots" v-model.number="trek.available_slots" class="form-control form-control-sm bg-transparent text-white border-secondary">
                    </td>
                    <td>{{ trek.registered_users_count }}</td>
                    <td style="font-size:0.75rem;">
                      <div>{{ trek.start_date }}</div>
                      <div>to {{ trek.end_date }}</div>
                    </td>
                    <td style="width:150px;">
                      <select v-model="trek.status" class="form-select form-select-sm bg-dark text-white border-secondary">
                        <option value="pending">Pending</option>
                        <option value="open">Open</option>
                        <option value="closed">Closed</option>
                        <option value="started">Started</option>
                        <option value="completed">Completed</option>
                      </select>
                    </td>
                    <td class="text-end">
                      <button class="btn btn-sm btn-outline-success" @click="updateTrek(trek)">Save</button>
                    </td>
                  </tr>
                  <tr v-if="treks.length === 0">
                    <td colspan="8" class="text-center py-4 text-secondary">No treks assigned yet.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'participants'" class="fade-in">
          <div class="card bg-dark-panel text-white mb-3">
            <div class="card-body">
              <label class="form-label small text-mint font-monospace">Select Trek</label>
              <select v-model="selectedTrekId" class="form-select bg-dark text-white border-secondary" @change="fetchParticipants">
                <option value="">Choose assigned trek</option>
                <option v-for="trek in treks" :key="trek.id" :value="trek.id">
                  {{ trek.title }} - {{ trek.location }}
                </option>
              </select>
            </div>
          </div>

          <div class="card bg-dark-panel text-white">
            <div class="card-header bg-transparent border-secondary-subtle py-3">
              <h5 class="card-title mb-0 heading-font text-mint fs-6">Participant List</h5>
            </div>
            <div class="table-responsive">
              <table class="table table-dark-custom align-middle mb-0">
                <thead>
                  <tr class="text-uppercase text-mint font-monospace opacity-50" style="font-size:0.7rem;">
                    <th>Booking</th>
                    <th>User ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Booking Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="participant in participants" :key="participant.booking_id">
                    <td class="font-monospace text-secondary">#BKG-{{ participant.booking_id }}</td>
                    <td>#USR-{{ participant.user_id }}</td>
                    <td class="fw-medium text-white">{{ participant.username }}</td>
                    <td>{{ participant.email }}</td>
                    <td>{{ participant.booking_date }}</td>
                    <td>
                      <span class="badge bg-success">{{ participant.booking_status }}</span>
                    </td>
                  </tr>
                  <tr v-if="participants.length === 0">
                    <td colspan="6" class="text-center py-4 text-secondary">No participants to show.</td>
                  </tr>
                </tbody>
              </table>
            </div>
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
const participants = ref([])
const selectedTrekId = ref('')
const message = ref('')
const error = ref('')

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
  if (currentTab.value === 'treks') return 'Assigned Treks'
  if (currentTab.value === 'participants') return 'Participants'
  return 'Dashboard'
})

const registeredTotal = computed(() => treks.value.reduce((sum, trek) => sum + (trek.registered_users_count || 0), 0))
const completedTreks = computed(() => treks.value.filter(trek => trek.status === 'completed').length)

const clearAlerts = () => {
  message.value = ''
  error.value = ''
}

const fetchTreks = async () => {
  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await API.get('/staff/treks', config)
    treks.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load assigned treks.'
  }
}

const updateTrek = async (trek) => {
  clearAlerts()
  const config = getAuthConfig()
  if (!config) return

  try {
    await API.patch(`/staff/treks/${trek.id}`, {
      available_slots: trek.available_slots,
      status: trek.status
    }, config)
    message.value = 'Trek updated successfully.'
    await fetchTreks()
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to update trek.'
  }
}

const fetchParticipants = async () => {
  clearAlerts()
  participants.value = []
  if (!selectedTrekId.value) return

  const config = getAuthConfig()
  if (!config) return

  try {
    const res = await API.get(`/staff/treks/${selectedTrekId.value}/participants`, config)
    participants.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load participants.'
  }
}

const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('user_role')
  router.push('/login')
}

onMounted(() => {
  fetchTreks()
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
