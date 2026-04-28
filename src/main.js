import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import HomeView from './components/HomeView.vue'
import QuizView from './components/QuizView.vue'
import WrongView from './components/WrongView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/quiz/:category/:type', component: QuizView, props: true },
  { path: '/wrong', component: WrongView }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

createApp(App).use(router).mount('#app')
