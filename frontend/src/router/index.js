import { createRouter, createWebHistory } from "vue-router";


import Login from "../views/login.vue";
import Register from "../views/register.vue";
import Dashboard from "../views/dashboard.vue";
import AdminDashboard from '../views/admindashboard.vue';

const routes = [
  {
    path: '/',
    redirect: '/dashboard' 
  },
  { 
    path: '/login', 
    component: Login 
  },
  { 
    path: '/dashboard', 
    component: Dashboard 
  },
  { 
    path: '/register', 
    component: Register 
  },
  { 
    path: '/admindashboard', 
    component: AdminDashboard 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;