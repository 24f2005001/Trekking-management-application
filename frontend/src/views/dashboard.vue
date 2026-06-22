<template>
  
  <div class="hero-wrapper min-vh-100 w-100 d-flex flex-column position-relative">
    
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-transparent pt-4 px-4 px-md-5 w-100">
      <div class="container-fluid p-0 d-flex justify-content-between align-items-center">
        
       
        <a class="navbar-brand fs-3 fw-bold text-white tracking-wide m-0" href="#" @click.prevent="goTo('/dashboard')">
          🏔️ Trekking App
        </a>

        
        <div class="d-flex gap-3 align-items-center">
          <button class="btn btn-outline-light px-4 rounded-pill fw-medium btn-nav" @click="goTo('/login')">
            Log In
          </button>
          <button class="btn btn-light px-4 rounded-pill fw-semibold shadow-sm btn-nav" @click="goTo('/register')">
            Sign Up
          </button>
        </div>

      </div>
    </nav>

    <div class="flex-grow-1 d-flex justify-content-center align-items-center px-3 pb-5">
      <div class="glass-card text-center text-white p-5 rounded-4 shadow-lg">

        <h1 class="display-4 fw-semibold mb-3 tracking-wide text-white text-shadow">
          Explore the Peaks
        </h1>

        <p class="fs-5 text-white mb-4 fw-light text-shadow opacity-90">
          Find your next adventure
        </p>

        <button class="btn custom-btn w-100 py-3 rounded-3 fw-semibold text-uppercase tracking-wider">
          Get Started
        </button>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "DashboardView",
  methods: {
    goTo(route) {
      this.$router.push(route);
    }
  }
}
</script>

<style scoped>
.hero-wrapper {
  
  background: url('https://images.unsplash.com/photo-1501785888041-af3ef285b470');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.glass-card {
  max-width: 500px; 
  width: 100%; 
  
  background: rgba(208, 171, 171, 0.12); 
  
  backdrop-filter: blur(6px); 
  -webkit-backdrop-filter: blur(6px);
  
  border: 1px solid rgba(188, 160, 160, 0.25);
}


.text-shadow {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}
.custom-heading {
  font-weight: 800; 
}

.opacity-90 {
  opacity: 0.9;
}


.fw-extrabold {
  font-weight: 800;
}
.tracking-wide {
  letter-spacing: 0.5px;
}
.tracking-wider {
  letter-spacing: 1px;
}


.btn-nav {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.btn-nav:hover {
  transform: translateY(-1px);
}

.custom-btn {
  background: rgba(0, 0, 0, 0.6);
  color: white;
  backdrop-filter: blur(10px);
  border: none;
}
.custom-btn:hover {
  background: #39312f8b;
}


</style>