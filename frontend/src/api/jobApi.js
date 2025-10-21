import axios from "axios";

const BASE_URL = "http://127.0.0.1:8080"; // Backend URL

export const searchJobs = async (query, top_k = 10) => {
  const response = await axios.get(`${BASE_URL}/jobs/search_jobs`, {
    params: { query, top_k },
  });
  return response.data;
};
