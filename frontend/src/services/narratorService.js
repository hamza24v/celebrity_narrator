import axios from 'axios';

export const uploadImage = (imageData) => {
  const formData = new FormData();
  formData.append('image', imageData);
  return axios.post(import.meta.env.VITE_API_URL, formData)
    .then(response => {
      console.log("Upload Response:", response); 
      return response;
    })
    .catch(error => {
      console.error("Upload Error:", error); 
    });
};

export const getAnalysis = (id) => {
  return axios.post(`${import.meta.env.VITE_API_URL}${id}/process_image/`)
    .then(response => {
      console.log("Analysis Response:", response);
      return response;
    })
    .catch(error => {
      console.error("Analysis Error:", error);
    });
};