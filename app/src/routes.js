import Summary from './views/Summary.vue'
import Detailed from './views/Detailed.vue'
import NotFound from './views/NotFound.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export let routes = [
  { path: '/', component: Summary },
  { path: '/detailed', component: Detailed },
  { path: '/:path(.*)', component: NotFound },
]
