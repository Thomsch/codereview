<template>
  <div class="container">
    <h1>Code Review Assistant</h1>
    <p>Paste the URL of your GitHub pull request to receive feedback.</p>
    <div class="input-group">
      <input v-model="prUrl" placeholder="Enter pull request URL" class="input-field" @input="updateValidation" @keyup.enter="onEnterKeyPress"/>
      <div v-if="validation" class="validation">{{ validation }}</div>
      <button @click="fetchData" class="submit-btn" :disabled="!isValidUrl(prUrl)">Review pull request</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-if="llm_output" class="feedback">
      <div v-html="llm_output"></div>
    </div>

    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  data() {
    return {
      prUrl: '' as string,
      llm_output: '' as string,
      loading: false as boolean,
      error: null as string | null,
      validation: '' as string,
    };
  },
  methods: {
    updateValidation() {
      if (this.validation.length > 0) {
        this.validation = '';
      }
    },
    onEnterKeyPress() {
      if (!this.isValidUrl(this.prUrl)) {
        this.validation = "Invalid URL. Please enter a valid URL.";
      } else {
        this.fetchData();
      }
    },
    isValidUrl(url: string): boolean {
      const urlPattern = /^(https?:\/\/)?([^\s:@]+:[^\s:@]*@)?(([0-9]{1,3}\.){3}[0-9]{1,3}|([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})?(:[0-9]{1,5})?(\/\S*)?$/;
      return urlPattern.test(url);
    },

    async fetchData() {


      if (this.prUrl.length === 0) {
        this.validation = "Please enter a pull request URL. For example, https://github.com/psf/black/pull/4218";
        return;
      }

      if (!this.isValidUrl(this.prUrl)) {
        this.validation = "Invalid URL. Please enter a valid URL.";
        return;
      }

      this.loading = true;
      this.error = null // type: string | null
      this.llm_output = ''; // Reset feedback data

      try {
        // Import the RemoteRunnable inside the method to ensure it's only loaded when needed
        const {RemoteRunnable} = await import('langchain/runnables/remote');

        const chain = new RemoteRunnable({
          url: process.env.VUE_APP_BACKEND + `feedback/`,
          // timeout: 1,
          // headers: {
          //   'Content-Type': 'application/json',
          // },
        });

        // Use the prUrl data property instead of the hardcoded URL
        const stream = await chain.stream({pr_url: this.prUrl});
        let isFirstChunk = true;

        for await (const chunk of stream) {
          this.loading = false;
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
      } catch (err: unknown) {
        if (err instanceof Error) {
          this.error = err.message;
          if (err.message.includes("fetch")) {
            this.error = "Assistant unavailable. Please try again later.";
          }
          console.log({err})
        } else {
          // If it's not an Error object, you might want to handle it differently
          this.error = "An unknown error occurred";
        }
        console.log("Error:", err);

      } finally {
        this.loading = false;
      }
    },
  },
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: auto;
  max-width: 600px; /* Adjust the width as needed */
  padding: 20px;
}

.input-group {
  width: 100%;
  margin-bottom: 20px;
}

.input-field, .submit-btn {
  width: 100%;
  padding: 10px;
  margin: 5px 0; /* Add margin to top and bottom */
  box-sizing: border-box; /* Ensures padding does not affect the width */
}

.submit-btn {
  padding: 10px 20px; /* Adjust padding as needed */
  background-color: #4CAF50; /* A green background for the submit button */
  color: white;
  border: none;
  cursor: pointer;
  margin-top: 10px; /* Space between input field and button */
  display: inline-block; /* Makes the button fit its content */
  margin-left: auto; /* Aligns the button to the right */
  margin-right: auto; /* Aligns the button to the center */
  border-radius: 5px; /* Adds rounded corners for a softer look */
}

.submit-btn:hover {
  background-color: #45a049; /* Darker shade of green for hover effect */
}

.submit-btn:disabled {
  background-color: #cccccc; /* Light gray background when button is disabled */
  cursor: not-allowed; /* Change cursor to indicate that the button is disabled */
}

.loading, .error, .validation {
  font-size: smaller;
}

.loading, .feedback, .error, .validation {
  text-align: left;
  width: 100%;
  padding: 10px;
}

.validation {
  color: #e57373;
}

.error {
  color: #e57373; /* Softer shade of red */
  margin-top: 10px;
  border: 1px solid #e57373; /* Optional: adds a subtle border */
  border-radius: 5px; /* Optional: rounds the corners for a softer look */
  background-color: #fff7f6; /* Optional: very light red background for more emphasis */
}
</style>
