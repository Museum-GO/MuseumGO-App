<template>
  <div class="Artwork">
    <img alt="Vue logo" src="../assets/logo.png" />
    <ArtWork msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
import ArtWork from "@/components/Artwork.vue";

export default {
  components: {
    ArtWork,
  } 
};
</script>

<style lang="scss" scoped>
.home {
  display: flex;
  flex-direction: column;

  img {
    width: 200px;
    height: auto;
    margin: 0 auto;
  }
}
</style>
