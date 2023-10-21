<template>
  <div id="testCompo">
    <p>{{ $t("hello") }}</p>
    <p>{{ variable }}</p>

    <input type="number" v-model="newVariable" />
    <button @click="setVariable">Change</button>
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

  // The following hooks won't be very useful in most cases.
  beforeUpdate() {
    // Called when the component is about to update.
    console.log("beforeUpdate");
  },

  updated() {
    // Called after a data change causes the virtual DOM to be re-rendered and patched.
    console.log("updated");
  },

  beforeUnmount() {
    // Called when the component is about to be unmounted.
  },

  unmounted() {
    // Called when the component has been removed from the DOM.
  },
});
</script>

<style lang="scss" scoped>
// Scoped styles
#testCompo {
  color: red;

  #message {
    color: green;
    .error {
      color: red;
    }
  }
}
</style>
