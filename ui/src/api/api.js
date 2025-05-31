import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:80'; // Port FastAPI

export const getPrediction = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_URL}/predict`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};