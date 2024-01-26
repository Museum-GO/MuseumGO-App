import axios from "axios";

const apiClient = axios.create({
  baseURL: "/",
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  getWorks() {
    return apiClient
      .get("/works")
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  getWorksInRect(bottomLeftCoordinates, topRightCoordinates) {
    return apiClient
      .get(
        `/worksInRectangle
?bottomLeftLat=${bottomLeftCoordinates[1]}
&bottomLeftLon=${bottomLeftCoordinates[0]}
&topRightLat=${topRightCoordinates[1]}
&topRightLon=${topRightCoordinates[0]}`
      )
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
