<template>
  <div class="artwork">
    <div class="top">
      <a class="title info">{{ artwork.name }}</a>

      <img alt="Artwork Image" src="../assets/test.jpeg" class="image" />
    </div>

    <div class="description">
      <p v-if="artwork.description && artwork.description[$i18n.locale]" class="desc"> {{ artwork.description[$i18n.locale] }}</p>

      <p class="location">
        <a class="info">{{ $t("Artwork.location") }}:</a> {{ artwork.location.name }}
      </p>

      <p class="author">
        <a class="info">{{ $t("Artwork.author") }}: </a>
        <a v-for="(artist, index) in artwork.artists" :key="index">{{ artist }}<b v-if="index != artwork.artists.length - 1">, </b>
      </a>
      </p>

      <p class="period"> 
        <a class="info">{{ $t("Artwork.period") }}:</a> {{ artwork.creationPeriod.minDate }}<a v-if="artwork.creationPeriod.maxDate">-{{ artwork.creationPeriod.maxDate }}</a>
      </p>

      <a v-if="artwork.wikiLink" :href="artwork.wikiLink" target="_blank">{{ $t("Artwork.wiki") }}</a>
    </div>
  </div>
</template>

<script>
import artworkData_list from '../assets/V0-list.json';

export default {
  name: "ArtWork",
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      artwork: artworkData_list[this.id]
    };
  }
};

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
