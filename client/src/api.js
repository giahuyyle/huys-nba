// For handling API requests

import axios from 'axios';

const BACKEND_URL = process.env.BACKEND_URL;

console.log(BACKEND_URL);

const api = axios.create({
  baseURL: BACKEND_URL,
});

export default api;