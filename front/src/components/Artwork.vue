<template>
  <div class="artwork">
    <img :src="artwork.image" alt="Artwork Image" class="image" />
    <div class="details">
      <h2 class="title">{{ artwork.name }}</h2>
      <p class="author">Auteur(s): {{ artwork.authors.join(', ') }}</p>
      <p class="location">Localisation: {{ artwork.location }}</p>
      <p class="description">{{ artwork.description }}</p>
      <a :href="artwork.wikipedia" target="_blank">Plus d'informations sur Wikipédia</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ArtWork",
  data() {
    return {
      artwork: {
        image: 'chemin/vers/image.jpg',
        name: 'Nom de l\'œuvre',
        authors: ['Auteur 1', 'Auteur 2'],
        location: 'Ville ou musée',
        description: 'Description de l\'œuvre',
        wikipedia: 'lien_vers_wikipedia'
      }
    };
  }
}
</script>

<style lang="scss" scoped>
  .artwork {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .image {
    width: 200px;
    height: auto;
    margin-right: 20px;
  }

  .details {
    .title {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 10px;
    }

    .author,
    .location,
    .description {
      margin-bottom: 10px;
    }

    a {
      display: block;
      color: blue;
      text-decoration: underline;

      &:hover {
        color: darkblue;
      }
    }
  }
</style>