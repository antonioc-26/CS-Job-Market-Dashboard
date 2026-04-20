/*
File: router/index.js
Purpose: Configure client-side routing for the Vue application.

Responsibilities:
- Initialize Vue Router with HTML5 history mode
- Define application routes and map them to view components
- Export the configured router instance for use in the app entry point

Notes:
- Currently only a single route (dashboard) is defined.
- Uses Vite's BASE_URL to support proper routing in different deployment environments.
*/

import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  // Use HTML5 history mode for clean URLs (no hash fragments).
  // BASE_URL ensures compatibility with different deployment base paths.
  history: createWebHistory(import.meta.env.BASE_URL),

  // Define application routes.
  routes: [
    {
      path: '/',
      name: 'dashboard',
      // Maps the root path to the main dashboard view.
      component: DashboardView,
      meta: {
        title: 'CS Job Market Dashboard',
      },
    },
  ],
})

router.afterEach((to) => {
  document.title = (to.meta.title as string) || 'CS Job Market Dashboard'
})

export default router