// Utility file for the map view

const sameGeometryCoordinates = (a, b) => {
  // Returns true if a and b are the same coordinates
  return (
    a.geometry.coordinates[0] === b.geometry.coordinates[0] &&
    a.geometry.coordinates[1] === b.geometry.coordinates[1]
  );
};

export const constructMuseumsFromArtworks = (artworks) => {
  // Converts artworks into museums
  // Museums are artworks with the same location

  const museums = [];
  artworks.forEach((artwork) => {
    const museum = museums.find((m) => sameGeometryCoordinates(m, artwork));

    if (museum) {
      museum.artworks.push(artwork);
    } else {
      museums.push({
        type: "Feature",
        geometry: artwork.geometry,
        artworks: [artwork],
      });
    }
  });
  return museums;
};
