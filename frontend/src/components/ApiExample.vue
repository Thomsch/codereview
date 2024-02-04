<template>
  <div>
    <h1>Code Review Assistant</h1>
    <p>Paste the URL of your GitHub pull request to receive feedback.</p>
    <!-- Input field for the PR URL -->
    <input v-model="prUrl" placeholder="Enter Pull Request URL" />
    <button @click="fetchData">Review pull request</button>

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
      prUrl: '', // Add a data property for PR URL
      llm_output: '',
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      this.llm_output = ''; // Reset feedback data

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

        // Use the prUrl data property instead of the hardcoded URL
        const stream = await chain.stream({pr_url: this.prUrl});

        let isFirstChunk = true;

        for await (const chunk of stream) {
          console.log(chunk);

          if (isFirstChunk) {
            // Assuming the first chunk is always the wrapper object
            isFirstChunk = false;
            console.log("Run ID:", chunk);
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
