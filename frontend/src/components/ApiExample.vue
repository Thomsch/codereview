<template>
  <div>
    <h1>API Example</h1>
    <button @click="fetchData">Fetch Joke</button>

    <div v-if="loading">Loading...</div>

    <div v-if="llm_output">
      <h2>Feedback:</h2>
      <div v-html="llm_output"></div>
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
      llm_output: '',
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      this.llm_output = ''; // Reset joke data

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

        const stream = await chain.stream({pr_url: "https://github.com/PyGithub/PyGithub/pull/664"});

        let isFirstChunk = true;

        for await (const chunk of stream) {
        console.log(chunk);

        if (isFirstChunk) {
          // Assuming the first chunk is always the wrapper object
          isFirstChunk = false;
          // Process the wrapper object as needed. Example:
          console.log("Run ID:", chunk);
          // Optionally, store the run_id or handle it as needed
        } else {
          // Append HTML content directly
          this.llm_output += chunk;
        }
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
