<template>
  <div class="artwork">
    <!-- <img alt="Artwork Image" :src="artwork.image" class="image" /> -->
    <h1>{{ id_artwork }}</h1>

    <div class="top">
      <h2 class="title">{{ artwork.name }}</h2>
      <img alt="Artwork Image" :src="artwork.image" class="image" />
    </div>

    <div class="description">
      <p class="desc">{{ artwork.description.en }}</p>

      <p class="location">
        <a class="info">{{ $t("Artwork.location") }}:</a> {{ artwork.location.name }}
      </p>

      <p class="author">
        <a class="info">{{ $t("Artwork.author") }}:</a>
        {{ artwork.artists[0]}}
      </p>

      <p class="period">
        <a class="info">{{ $t("Artwork.period") }}:</a> {{ artwork.creationPeriod.minDate }}
      </p>

      <a :href="artwork.wikiLink" target="_blank">{{ $t("Artwork.wiki") }}</a>
    </div>
  </div>
</template>

<script>
import artworkData from '../assets/V0.json';

export default {
  name: "ArtWork",
  data() {
    return {
      artwork: artworkData,
    };
  },
  created() {
    this.id_artwork = this.$route.params.id_artwork;
  },
};
/// TO KEEP BECAUSE IT WILL BE USEFULL WHEN I WILL CALL THE API
//
//
// export default {
//   name: "ArtWork",
//   data() {
//     return {
//       artwork: null, // laisser null pour l'instant
//     };
//   },
//   created() {
//   fetch('../assets/v0.json') // Remplacez le chemin d'accès si besoin
//     .then(response => response.json())
//     .then(data => {
//       this.artwork = data;
//     })
//     .catch(error => {
//       console.error('Erreur lors du chargement des données du JSON:', error);
//     });

//     this.id_artwork = this.$route.params.id_artwork;
// },
// };
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
