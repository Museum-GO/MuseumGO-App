<template>
  <div class="Artwork">
    <ArtWork />
  </div>
</template>

<script>
import ArtWork from "@/components/Artwork.vue";

export default {
  components: {
    ArtWork,
  },
};
</script>

<style lang="scss" scoped>
.Artwork {
  display: flex;
  flex-direction: column;
}
</style>
