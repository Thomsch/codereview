<template>
  <div>
    <h1>API Example</h1>
    <button @click="fetchData">Fetch Data</button>

    <div v-if="loading">Loading...</div>

    <div v-if="data">
      <h2>Data from API:</h2>
      <pre>{{ data }}</pre>
    </div>

    <div v-if="error">
      <p>Error: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      data: null,
      loading: false,
      error: null,
    };
  },
  methods: {
    fetchData() {
      this.loading = true;
      this.error = null;

      axios
        .get("http://127.0.0.1:5000/") // Replace with your API endpoint
        .then((response) => {
          console.log(response)
          this.data = response.data
          this.loading = false;
        })
        .catch((error) => {
          console.log(error)
          this.error = error.message;
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>