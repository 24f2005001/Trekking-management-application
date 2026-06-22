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
            <li><a href="#" class="nav-link-custom"><i class="ti ti-users"></i> Staff & Trekkers</a></li>
            <li><a href="#" class="nav-link-custom"><i class="ti ti-ticket"></i> Bookings</a></li>
          </ul>

          <h6 class="px-3 text-uppercase text-mint opacity-50 small font-monospace" style="font-size: 0.7rem; letter-spacing: 0.1em;">System</h6>
          <ul class="nav flex-column mb-4">
            <li><a href="#" class="nav-link-custom"><i class="ti ti-file-report"></i> Reports</a></li>
            <li><a href="#" class="nav-link-custom"><i class="ti ti-settings"></i> Settings</a></li>
          </ul>
        </div>
      </nav>

      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 pt-3 pb-5">
        
        <header class="d-flex justify-content-between align-items-center pb-3 mb-4 border-bottom border-secondary-subtle">
          <h1 class="h4 heading-font fw-bold mb-0 text-capitalize">{{ currentTab }}</h1>
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

        <div v-if="currentTab === 'dashboard' || currentTab === 'analytics'" class="py-5 text-center text-secondary">
          <i class="ti ti-folder-open fs-1 opacity-20 mb-3"></i>
          <p class="font-monospace">Welcome to the Admin Panel. Use the sidebar navigation menu to view active trek data models.</p>
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
                    <td>${{ trek.price }}</td>
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
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Duration (Days)</label>
                  <input type="number" v-model="form.duration_days" class="form-control bg-transparent text-white border-secondary" min="1" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Price ($)</label>
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
                  <label class="form-label small text-mint font-monospace">Staff ID</label>
                  <input type="number" v-model="form.staff_id" class="form-control bg-transparent text-white border-secondary">
                </div>
                <div class="col-md-4">
                  <label class="form-label small text-mint font-monospace">Status</label>
                  <select v-model="form.status" class="form-select bg-dark text-white border-secondary">
                    <option value="pending">Pending</option>
                    <option value="open">Open</option>
                    <option value="closed">Closed</option>
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

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/admin'

// Global Layout States
const currentTab = ref('dashboard')
const searchQuery = ref('')
const adminInitials = ref('A')

// Reactive Storage for Data Models
const treks = ref([])

// Form Layout States
const showModal = ref(false)
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

// Secure dynamic header setup for requests
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

// HTTP GET Request: Fetch routes from database
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

// Lifecycle Initialization Hook
onMounted(() => {
  fetchTreksData()
})

// Client Side Search Filter
const filteredTreks = computed(() => {
  if (!searchQuery.value) return treks.value
  return treks.value.filter(t => 
    t.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    t.location.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// CRUD Actions: Create, Edit, and Delete operational calls
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
    await fetchTreksData()
  } catch (error) {
    alert(error.response?.data?.message || 'Error compiling backend transaction data for layout update.')
  }
}

const deleteTrekRoute = async (id) => {
  const config = getAuthConfig()
  if (!config) return

  if (confirm('Are you absolutely sure you want to completely remove this route entry from the ledger?')) {
    try {
      await axios.delete(`${API_BASE_URL}/treks/${id}`, config)
      await fetchTreksData()
    } catch (error) {
      alert('Error updating server context index record.')
    }
  }
}

// Visual layout badge utilities mapping context
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