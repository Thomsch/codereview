import { createApp } from 'vue'
import App from './App.vue'
import { inject } from '@vercel/analytics';
import { injectSpeedInsights } from '@vercel/speed-insights';

inject();
injectSpeedInsights();

createApp(App).mount('#app')
