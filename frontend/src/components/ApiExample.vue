<template>
  <div>
    <h1>API Example</h1>

    <input type="text" v-model="prUrl" placeholder="Enter PR URL" />
    <button @click="fetchData">Fetch Data</button>

    <div v-if="loading">Loading...</div>

    <div v-if="data">
      <h2>Response:</h2>
      <pre>{{ data }}</pre>
    </div>

    <div v-if="error">
      <p>Error: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // Ensure axios is imported

export default {
  data() {
    return {
      prUrl: '', // Data property for the PR URL
      data: null,
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchData() {
      if (!this.prUrl) {
        this.error = 'Please enter a PR URL';
        return;
      }

      this.loading = true;
      this.data = null;
      this.error = null;

      try {
        const apiUrl = ' http://localhost:8000/'; // Replace with your API URL
        const params = { pr_url: this.prUrl };

        const response = await axios.get(apiUrl, { params });
        this.data = response.data;
      } catch (error) {
        console.error(error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
