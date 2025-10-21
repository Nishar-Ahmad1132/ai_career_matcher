import axios from "axios";

const BASE_URL = "http://127.0.0.1:8080"; // Your FastAPI backend

export const matchResume = async (file, top_k = 5) => {
  const formData = new FormData();
  formData.append("resume", file);

  const response = await axios.post(
    `${BASE_URL}/resume/match_resume?top_k=${top_k}`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};
