<template>
  <div class="artwork">
    <div class="top">
      <a class="title info">{{ artwork.name }}</a>
      <!-- <img alt="Artwork Image" :src="artwork.image" class="image" /> -->
      <img alt="Artwork Image" src="../assets/test.jpeg" class="image" />
    </div>

    <div class="description">
      <p v-if="artwork.description[$i18n.locale]" class="desc"> {{ artwork.description[$i18n.locale] }}</p>

      <p class="location">
        <a class="info">{{ $t("Artwork.location") }}:</a> {{ artwork.location.name }}
      </p>

      <p class="author">
        <a class="info">{{ $t("Artwork.author") }}: </a>
        <a v-for="artist in artwork.artists" :key="artist"> {{ artist }}, </a>
      </p>

      <p class="period"> 
        <a class="info">{{ $t("Artwork.period") }}:</a> {{ artwork.creationPeriod.minDate }}<a v-if="artwork.creationPeriod.maxDate">-{{ artwork.creationPeriod.maxDate }}</a>
      </p>

      <a v-if="artwork.wikiLink" :href="artwork.wikiLink" target="_blank">{{ $t("Artwork.wiki") }}</a>
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
  height: 100%;
  margin-left: 15%;
  margin-right: 15%;
  background-color: white;
  padding: 2%;
}

.info {
  font-weight: bold;
}

.description {
  align-items: right;
}

.top {
  display: flex;
  flex-direction: column;
  justify-content: center;


  .title{
    align-items: left;
  }

  .image {
    height: 100%;
    width: 100%;
    align-items: center;
  }
}
</style>
