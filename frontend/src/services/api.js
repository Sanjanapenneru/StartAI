import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8007",
  headers: { "Content-Type": "application/json" },
});

export const gramaiService = {
  createAssessment: async (data) => {
    const response = await api.post("/api/assessment", data);
    return response.data;
  },
  analyze: async (assessmentId) => {
    const response = await api.post("/api/analyze", {
      assessment_id: assessmentId,
    });
    return response.data;
  },
  financialPlan: async (availableCapital) => {
    const response = await api.post("/api/financial-plan", {
      available_capital: availableCapital,
    });
    return response.data;
  },
  health: async () => {
    const response = await api.get("/api/health");
    return response.data;
  },
};

export default api;