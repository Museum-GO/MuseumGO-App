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
    const museum = museums.find((m) => sameCoordinates(m, artwork));

    if (museum) {
      museum.artworks.push(artwork);
    } else {
      museums.push({
        type: "Feature",
        location: artwork.location,
        artworks: [artwork],
      });
    }
  });
  return museums;
};

export const generateRandomArtwork = (targetCoordinates) => {
  const artworks = [
    {
      location: {
        coordinates: [48.860611, 2.337644], // Louvre
      },
    },
    {
      location: {
        coordinates: [48.8526049229, 2.33466199468], // Eugene Delacroix
      },
    },
  ];

  for (let i = 0; i < 10; i++) {
    artworks.push({
      location: {
        coordinates: [
          targetCoordinates[0] + (Math.random() - 0.5) * 0.25,
          targetCoordinates[1] + (Math.random() - 0.5) * 0.25,
        ],
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
        coordinates: randomFeature.geometry.coordinates,
      },
    });
  }

  return artworks;
};
