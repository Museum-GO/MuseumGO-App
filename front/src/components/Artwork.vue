<template>
  <div class="artwork">
    <!-- <img alt="Artwork Image" :src="artwork.image" class="image" /> -->
    <h1>{{ id_artwork }}</h1>

    <div class="top">
      <h2 class="title">{{ artwork.name }}</h2>
      <img alt="Artwork Image" :src="artwork.image" class="image" />
    </div>
    {{ artwork.image }}

    <div class="description">
      <p class="description">{{ artwork.description }}</p>

      <p class="location">
        <a class="info">{{ $t("Artwork.location") }}:</a> {{ artwork.location }}
      </p>

      <p class="author">
        <a class="info">{{ $t("Artwork.author") }}:</a>
        {{ artwork.authors.join(", ") }}
      </p>

      <p class="period">
        <a class="info">{{ $t("Artwork.period") }}:</a> {{ artwork.year }}
      </p>

      <a :href="artwork.wikipedia" target="_blank">{{ $t("Artwork.wiki") }}</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ArtWork",
  data() {
    return {
      artwork: {
        image: "../assets/logo.png",
        name: "Nom de l'œuvre",
        authors: ["Auteur 1", "Auteur 2"],
        location: "Ville ou musée",
        description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit.",
        year: "1999",
        wikipedia: "https://en.wikipedia.org/wiki/Vue.js#History",
      },
    };
  },created() {
    this.id_artwork = this.$route.params.id_artwork;
  }
};
</script>
<style lang="scss" scoped>
.artwork {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 30%;
  margin-right: 30%;
}

.info {
  font-weight: bold;
}

.description {
  align-items: right;
}

.image {
  height: 50%;
  width: 50%;
}

.top {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
