// Utility file for the map view

const sameCoordinates = (a, b) => {
  // Returns true if a and b are the same coordinates
  return (
    a.location.coordinates[0] === b.location.coordinates[0] &&
    a.location.coordinates[1] === b.location.coordinates[1]
  );
};

export const constructMuseumsFromArtworks = (artworks) => {
  // Converts artworks into museums
  // Museums are artworks with the same location

  const museums = [];
  artworks.forEach((artwork) => {
    if (!artwork.location || !artwork.location.coordinates || !artwork._id)
      return;

    // Get the museum with the same coordinates
    const museum = museums.find((m) => sameCoordinates(m, artwork));

    if (museum) {
      museum.nbArtworks += 1;
      museum.name = artwork.location.name || "Museum";
    } else {
      museums.push({
        id: artwork._id,
        location: artwork.location,
        nbArtworks: 1,
        imageUrl: artwork.image,
        name: artwork.name,
      });
    }
  });
  return museums;
};

export const generateRandomArtwork = (targetCoordinates) => {
  const artworks = [];
  const nbArtworks = Math.floor(Math.random() * 20) + 1;

  for (let i = 0; i < nbArtworks; i++) {
    artworks.push({
      _id: i,
      name: "Artwork " + i,
      image: "https://picsum.photos/200/300",
      location: {
        coordinates: [
          targetCoordinates[0] + (Math.random() - 0.5) * 0.25,
          targetCoordinates[1] + (Math.random() - 0.5) * 0.25,
        ],
        name: "Place " + i,
      },
    });
  }

  // Add few more artworks that have the same coordinates as some other artworks
  const nbMuseums = 5;

  for (let i = 0; i < nbMuseums; i++) {
    const randomIndex = Math.floor(Math.random() * artworks.length);
    const randomFeature = artworks[randomIndex];
    artworks.push({
      location: {
        coordinates: randomFeature.location.coordinates,
      },
    });
  }

  return artworks;
};
