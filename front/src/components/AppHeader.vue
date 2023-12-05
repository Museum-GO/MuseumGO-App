<template>
  <header id="header">

    <div class="app-name" > <a href="#main"> MuseumGo</a> </div>
        
        <div class="search-bar">
            <input type="text" placeholder="Recherche">
        </div>

        <div class="language-link"> <a href="?fr">FR</a> | <a href="?eng">ENG</a> </div>
  </header>
</template>

<script>
export default {
  name: "AppHeader",
};
</script>

<style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
        }

        #header {
            background-color: #ffffff;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .app-name {
            font-size: 24px;
            font-weight: bold;
        }

        .app-name a{
          color: #333333;
          text-decoration: none;
        }

        .search-bar {
            margin-left: 20px;
        }

        .language-link {
            color: #333333;
            font-weight: bold;
            margin-right: 20px;
        }

        .language-link a{
          color: #333333;
          text-decoration: none;
        }
    </style>