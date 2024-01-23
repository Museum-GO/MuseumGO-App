<template>
  <div id="helloWorld">
    <p>{{ $t("HelloWorld.hello") }}</p>
    <p>{{ variable }}</p>

    <!-- Variable change form -->
    <div id="form">
      <input type="number" v-model="newVariable" />
      <button @click="setVariable">{{ $t("HelloWorld.setVariable") }}</button>
    </div>

    <!-- Variable change message -->
    <div id="message">
      <p v-if="isVariableCorrect">{{ $t("HelloWorld.variableCorrect") }}</p>
      <p v-else class="error">{{ $t("HelloWorld.variableIncorrect") }}</p>
    </div>

    <!-- ArtWork display -->
    <div id="works">
      <div class="work" v-for="work in works" :key="work._id">
        <h3>{{ work.name }}</h3>
        <p>{{ work.location.coordinates }}</p>
      </div>
    </div>
    <div class="numWork">
        <p> {{ numWork }}</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "HelloWorld",
  data() {
    return {
      variable: 10,
      newVariable: 20,
      works: [],
      numWork: undefined,
    };
  },
  
  created() {
    // Called when the component is created.
    // Good place to fetch data from API.

    api.getWorks().then((works) => {
      this.works = works;
    });

    api.getNumberWorks().then((NumWorks) => {
      this.numWork = NumWorks;
    });

  },
  mounted() {
    // Called when the component has been mounted in the DOM.
    // Good place to use jQuery or other DOM manipulations (maps, etc.)
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
};
</script>

<style lang="scss" scoped>
// Scoped styles
#helloWorld {
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

  #works {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: flex-start;
    max-width: 100%;
    overflow: auto;
    padding-bottom: 10px;

    .work {
      width: 200px;
      min-width: 200px;
      height: 150px;
      padding: 10px;
      margin: 5px;
      border: 1px solid black;
      border-radius: 5px;
    }
  }
}
</style>
