import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../stores/auth'

import HomeView from '../views/public/HomeView.vue'
import LoginView from '../views/auth/LoginView.vue'

import AdminLayout from '../layouts/AdminLayout.vue'

import DashboardView from '../views/admin/DashboardView.vue'
import CompanyView from '../views/admin/CompanyView.vue'
import ServicesView from '../views/admin/ServicesView.vue'
import ContactsView from '../views/admin/ContactsView.vue'
import FaqView from '../views/admin/FaqView.vue'
import LocationsView from '../views/admin/LocationsView.vue'


const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        guestOnly: true,
      },
    },

    {
      path: '/admin',
      component: AdminLayout,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: DashboardView,
        },

        {
          path: 'company',
          name: 'admin-company',
          component: CompanyView,
        },

        {
          path: 'services',
          name: 'admin-services',
          component: ServicesView,
        },

        {
          path: 'contacts',
          name: 'admin-contacts',
          component: ContactsView,
        },

        {
          path: 'faq',
          name: 'admin-faq',
          component: FaqView,
        },

        {
          path: 'locations',
          name: 'admin-locations',
          component: LocationsView,
        },
      ],
    },
  ],
})


router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  await authStore.initialize()

  if (
    to.meta.requiresAuth &&
    !authStore.isAuthenticated
  ) {
    return {
      name: 'login',
    }
  }

  if (
    to.meta.guestOnly &&
    authStore.isAuthenticated
  ) {
    return {
      name: 'admin-dashboard',
    }
  }
})


export default router