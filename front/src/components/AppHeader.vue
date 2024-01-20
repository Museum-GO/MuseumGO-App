<!-- TEMPLATE ---------------------------------------------------------------------------------------------------------------------------------->

<template>
  <header id="header" lang="fr">

    <div class="app-name"> <a href="/">{{$t("Header.app-name") }}</a> </div>

    <div class="search-bar">
      <input type="text" :placeholder='$t("Header.search-bar")'>
    </div>

    <div class="language-link">  
      <select v-model="$i18n.locale">
        <option value="fr">fr</option>
        <option value="en">en</option>
      </select>
</div>
  </header>
</template>

<!-- SCRIPT ---------------------------------------------------------------------------------------------------------------------------------->

<script>
  export default {
    name: "AppHeader",
  };
</script>

<!-- CSS ---------------------------------------------------------------------------------------------------------------------------------->

<style lang="scss" scoped>
  body {
    margin: 0;
    font-family: Arial, sans-serif;
  }

  #header {
    background-color: #333333;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  a {
      color: #d3d3d3;
      text-decoration: none;
      font-weight: bold;
  }

  .app-name {
    font-size: 24px;
  }

  .search-bar {
    margin-left: 20px;
  }

  .language-link {
    margin-right: 20px;
  }
</style>