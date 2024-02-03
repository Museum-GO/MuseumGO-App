<template>
  <div class="Artwork">
    <ArtWork :id="this.id_artwork" />
  </div>
</template>

<script>
import ArtWork from "@/components/Artwork.vue";

export default {
  components: {
    ArtWork,
  },
  created() {
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
