import { API_CHAT, API_RECOMMEND } from './const';
import { Agent } from '@/types/agent';

export const getEndpoint = (agent: Agent) => {
  return API_CHAT;
};

export const getRecommendationEndpoint = () => {
  return API_RECOMMEND;
};

const exportObjects = {
  getEndpoint,
  getRecommendationEndpoint,
};

export default exportObjects;
