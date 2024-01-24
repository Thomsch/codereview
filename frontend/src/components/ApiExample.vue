<template>
  <div>
    <h1>API Example</h1>
    <button @click="fetchData">Fetch Joke</button>

    <div v-if="loading">Loading...</div>

    <div v-if="joke">
      <h2>Joke:</h2>
      <p>{{ joke }}</p>
    </div>

    <div v-if="error">
      <p>Error: {{ error }}</p>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      joke: '',
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      this.joke = ''; // Reset joke data

      try {
        // Import the RemoteRunnable inside the method to ensure it's only loaded when needed
        const { RemoteRunnable } = await import('langchain/runnables/remote');

        const chain = new RemoteRunnable({
          url: `http://localhost:8000/feedback/`,
          // timeout: 1,
          // headers: {
          //   'Content-Type': 'application/json',
          // },
        });

        const stream = await chain.stream({ pr_url: "https://github.com/PyGithub/PyGithub/pull/664"});

        for await (const chunk of stream) {
          console.log(chunk);
          this.joke += chunk;
        }

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