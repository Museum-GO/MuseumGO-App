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
?bottomLeftLat=${bottomLeftCoordinates[0]}
&bottomLeftLon=${bottomLeftCoordinates[1]}
&topRightLat=${topRightCoordinates[0]}
&topRightLon=${topRightCoordinates[1]}`
      )
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
