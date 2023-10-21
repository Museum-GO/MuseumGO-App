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
export default {};
</script>

<style lang="scss" scoped>
#header {
  display: flex;
  margin-bottom: 20px;
  background-color: #42b983;
  height: 50px;
  align-items: center;
  padding: 0 20px;
  justify-content: space-between;
}
</style>
