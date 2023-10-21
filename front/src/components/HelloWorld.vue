<template>
  <div id="testCompo">
    <p>{{ $t("hello") }}</p>
    <p>{{ variable }}</p>

    <!-- Variable change form -->
    <div id="form">
      <input type="number" v-model="newVariable" />
      <button @click="setVariable">{{ $t("setVariable") }}</button>
    </div>

    <!-- Variable change message -->
    <div id="message">
      <p v-if="isVariableCorrect">{{ $t("variableCorrect") }}</p>
      <p v-else class="error">{{ $t("variableIncorrect") }}</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "HelloWorld",
  i18n: {
    // Local translations
    messages: {
      en: {
        hello: "Hello from component!",
        setVariable: "Set Variable from component!",
        variableCorrect: "The variable is correct from component!",
        variableIncorrect: "The variable is incorrect from component!",
      },
      // ... other languages can be defined here
    },
  },
  data() {
    return {
      variable: 10,
      newVariable: 20,
    };
  },
  created() {
    // Called when the component is created.
  },
  mounted() {
    // Called when the component has been mounted in the DOM.
  },
  methods: {
    // Any methods you want to use in your component.
    setVariable() {
      this.variable = parseInt(this.newVariable);
    },
  },
  computed: {
    // Any computed properties you want to use in your component.
    isVariableCorrect() {
      return this.variable >= 0;
    },
  },
  watch: {
    // Any watchers you want to use in your component.
    variable(newValue, oldValue) {
      console.log(`Variable changed from ${oldValue} to ${newValue}`);
    },
  },

  // Their is many other options you can use in your component.
  // Learn more on hooks: https://vuejs.org/guide/essentials/lifecycle.html
});
</script>

<style lang="scss" scoped>
// Scoped styles
#testCompo {
  padding: 10px;
  margin: 10px;
  border: 1px solid black;
  border-radius: 5px;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  #message {
    color: green;
    .error {
      color: red;
    }
  }
}
</style>
