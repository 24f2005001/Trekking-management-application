<template>
  <div class="split-container min-vh-100 w-100 d-flex flex-column flex-md-row">
    
    <div class="visual-side d-none d-md-flex flex-column justify-content-between p-5">
      <a class="brand-logo text-decoration-none fs-3 fw-bold text-white tracking-wide" href="#" @click.prevent="$router.push('/dashboard')">
        🏔️ Trekking App
      </a>
      
      <div class="visual-footer text-white text-shadow">
        <h3 class="fw-bold mb-2">The mountains are calling.</h3>
        <p class="opacity-75 fw-light mb-0">Join thousands of trekkers planning their next peak adventure.</p>
      </div>
    </div>

    <div class="form-side d-flex justify-content-center align-items-center p-4 p-md-5">
      
      <div class="glass-card p-4 p-sm-5 rounded-4 shadow-lg">
        
        <div class="d-md-none text-center mb-4">
          <span class="fs-4 fw-bold text-white tracking-wide">🏔️ Trekking App</span>
        </div>

        <div class="text-center mb-4">
          <h2 class="fw-semibold text-white text-shadow mb-2">Welcome Back</h2>
          <p class="fs-6 text-white text-shadow opacity-90 fw-light">
            Log in to plan your next trek
          </p>
        </div>

        <form @submit.prevent="login" class="d-flex flex-column gap-3">
          
          <div class="form-group text-start">
            <label for="email" class="form-label text-white text-shadow fw-medium mb-1">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="form-control custom-input"
              placeholder="you@example.com"
              required
            />
          </div>

          <div class="form-group text-start">
            <label for="password" class="form-label text-white text-shadow fw-medium mb-1">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="form-control custom-input"
              placeholder="••••••••"
              required
            />
          </div>

          <div v-if="error" class="alert alert-danger py-2 my-2 text-center small rounded-3">
            {{ error }}
          </div>

          <button 
            type="submit" 
            class="btn custom-btn w-100 py-3 rounded-3 fw-semibold text-uppercase tracking-wider mt-2 d-flex justify-content-center align-items-center gap-2" 
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
            {{ loading ? "Logging in..." : "Login" }}
          </button>

        </form>

        <div class="text-center mt-4">
          <router-link to="/register" class="text-decoration-none text-white text-shadow opacity-90 small">
            Don't have an account? <span class="text-white fw-bold text-decoration-underline">Register</span>
          </router-link>
        </div>

      </div>

    </div>

  </div>
</template>

<script>
import API from "../api";

export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      error: ""
    };
  },
  methods: {
    async login() {
      this.error = "";
      this.loading = true;
      try {
        const response = await API.post("/login", {
          email: this.email,
          password: this.password
        });
        const token = response.data.access_token;
        const userRole = response.data.role;

        if (token) {
          localStorage.setItem('admin_token', token);
          localStorage.setItem('user_role', userRole);
        }

        if (userRole === 'admin') {
          this.$router.push("/admindashboard");
        } else if (userRole === 'staff') {
          this.$router.push("/staffdashboard");
        } else {
          this.$router.push("/userdashboard");
        }
      } catch (err) {
        this.error = err.response?.data?.message || "Invalid email or password";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>

.split-container {
  overflow-x: hidden;
}


.visual-side {
  flex: 1;
  background: 
    linear-gradient(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.45)), 
    url('https://images.unsplash.com/photo-1501785888041-af3ef285b470');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}


.form-side {
  flex: 1;
  
  background: linear-gradient(
    135deg, 
    #1d2a2b 0%,    
    #14191a 100%   
  );
  position: relative;
}
.form-side::before {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: rgba(208, 171, 171, 0.05); 
  border-radius: 50%;
  filter: blur(80px);
  top: 20%;
  left: 20%;
  pointer-events: none;
}


.glass-card {
  max-width: 440px; 
  width: 100%; 
  background: rgba(208, 171, 171, 0.07); 
  backdrop-filter: blur(8px); 
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(188, 160, 160, 0.15);
}


.custom-input {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  border-radius: 8px;
  padding: 12px;
}
.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}
.custom-input:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(188, 160, 160, 0.4);
  color: white;
  box-shadow: none;
}


.custom-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.2s ease;
}
.custom-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
}
.custom-btn:active {
  transform: scale(0.98);
}


.text-shadow {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}
.opacity-90 {
  opacity: 0.9;
}
.tracking-wide {
  letter-spacing: 0.5px;
}
.tracking-wider {
  letter-spacing: 1px;
}
</style>
