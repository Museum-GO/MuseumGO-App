<template>
  <header id="header">
    <h1>MuseumGo</h1>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </nav>
  </header>
</template>

<script>
export default {
  name: "AppHeader",
};
</script>

<style lang="scss" scoped>
#header {
  display: flex;
  background-color: #42b983;
  height: 6vh;
  align-items: center;
  padding: 0 20px;
  justify-content: space-between;
}
</style>
