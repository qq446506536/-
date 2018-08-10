import Vue from 'vue'
import Router from 'vue-router'

import Luffy from '@/components/Luffy'



Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Luffy',
      component: Luffy
    }
  ]
})
