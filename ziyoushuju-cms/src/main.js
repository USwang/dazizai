import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from '@/router'
import auth from './utils/auth'
import http from './utils/http'

const app = createApp(App)
app.config.globalProperties.$auth = auth;
app.config.globalProperties.$http = http;
app.use(ElementPlus)
app.use(router)
app.mount('#app')
