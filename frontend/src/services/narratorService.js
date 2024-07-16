import axios from 'axios';

export const uploadImage = (imageData) => {
  const formData = new FormData();
  console.log(typeof imageData);
  formData.append('image', imageData);
  return axios.post(API_URL, formData);
};

export const getAnalysis = (id) => {
  return axios.post(`${import.meta.env.VITE_API_URL}${id}/process_image/`);
};