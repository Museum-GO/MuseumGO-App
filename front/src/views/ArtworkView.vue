<template>
  <div class="Artwork">
    <ArtWork :id="this.id_artwork"/>
  </div>
</template>

<script>
  import ArtWork from "@/components/Artwork.vue";

  import artworkData_list from '../assets/V0-list.json';

  export default {
    components: {
      ArtWork,
    },
    data() {
      return {
        artwork_list: artworkData_list
      };
    },created() {
    this.id_artwork = this.$route.params.id_artwork;
  },
};
</script>

<style lang="scss" scoped>
.Artwork {
  display: flex;
  flex-direction: column;
}
</style>
