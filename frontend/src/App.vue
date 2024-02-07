<template>
<!--  <img alt="Vue logo" src="./assets/logo.png">-->
<!--  <HelloWorld msg="Welcome to Your Vue.js App"/>-->
  <ApiExample/>
</template>

<script lang="ts">
import ApiExample from "./components/CodeReview.vue";
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App',
  components: {
    ApiExample
  },
  mounted() {
    document.title = "Code Review Assistant";
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>