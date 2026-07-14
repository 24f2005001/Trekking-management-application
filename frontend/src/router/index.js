import { createRouter, createWebHistory } from "vue-router";


import Login from "../views/login.vue";
import Register from "../views/register.vue";
import Dashboard from "../views/dashboard.vue";
import AdminDashboard from '../views/admindashboard.vue';
import UserDashboard from '../views/userdashboard.vue';
import StaffDashboard from '../views/staffdashboard.vue';

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
    component: AdminDashboard,
    meta: { roles: ['admin'] }
  },
  {
    path: '/userdashboard',
    component: UserDashboard,
    meta: { roles: ['trekker', 'user'] }
  },
  {
    path: '/staffdashboard',
    component: StaffDashboard,
    meta: { roles: ['staff'] }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to) => {
  const allowedRoles = to.meta.roles;
  if (!allowedRoles) return true;

  const token = localStorage.getItem('admin_token');
  const role = localStorage.getItem('user_role');

  if (!token || !role) return '/login';
  if (allowedRoles.includes(role)) return true;

  if (role === 'admin') return '/admindashboard';
  if (role === 'staff') return '/staffdashboard';
  return '/userdashboard';
});

export default router;
