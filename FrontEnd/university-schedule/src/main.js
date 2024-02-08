/**
 * @authors
 *   xrasst00, Sergei Rasstrigin
 *   xmyron00, Yurii Myronov
 *   xklima34, Aliaksei Klimau
 *
 * @file main.js
 * @brief Main app file
 */
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VCalendar from 'v-calendar';
import 'v-calendar/style.css';

// Use plugin with optional defaults


const app = createApp(App)

app.use(router)
app.use(VCalendar, {})

app.mount('#app')
