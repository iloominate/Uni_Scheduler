/**
 * @authors
 *   xrasst00, Sergei Rasstrigin
 *   xmyron00, Yurii Myronov
 *   xklima34, Aliaksei Klimau
 *
 * @file index.js
 * @brief Vue JS Router
 */
import { createRouter, createWebHistory } from 'vue-router'
import Home from "@/views/HomeView.vue";
import Authorization from "@/views/Authorization.vue";
import StudentView from "@/views/StudentView.vue";
import Scheduler from "@/views/Scheduler.vue";
import StudentSubjects from "@/views/StudentSubjects.vue";
import GuarantorView from "@/views/GuarantorView.vue";
import GuarantorInstructors from "@/views/GuarantorInstructors.vue";
import GuarantorActivities from "@/views/GuarantorActivities.vue";
import StudentActivities from "@/views/StudentActivities.vue";
import Admin from "@/views/Admin.vue";
import InstructorView from "@/views/InstructorView.vue";
import InstructorActivities from "@/views/InstructorActivities.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/authorization',
      component: Authorization,
    },
    {
      path: '/student',
      component: StudentView,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Student') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/scheduler',
      component: Scheduler,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Scheduler' && status !== 'Admin') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/student/subjects',
      component: StudentSubjects,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Student') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/student/activities',
      component: StudentActivities,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Student') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/guarantor',
      component: GuarantorView,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Guarantor' && status !== 'Admin') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/guarantor/instructors',
      component: GuarantorInstructors,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Guarantor' && status !== 'Admin') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/guarantor/activities',
      component: GuarantorActivities,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Guarantor' && status !== 'Admin') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/admin',
      component: Admin,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Admin') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/instructor',
      component: InstructorView,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Instructor' && status !== 'Guarantor' && status !== 'Admin') {
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/instructor/activities',
      component: InstructorActivities,
      beforeEnter: (to, from, next) => {
        const status = JSON.parse(localStorage.getItem('user')).permission.description
        if (status !== 'Instructor' && status !== 'Guarantor' && status !== 'Admin') {
          next('/');
        } else {
          next();
        }
      }
    },

  ]
})

export default router
