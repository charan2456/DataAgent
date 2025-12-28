import { OPENAI_API_TYPE } from '../utils/app/const';

export interface Agent {
  id: string;
  name: string;
  maxLength: number;
  tokenLimit: number;
  llm: LLM | undefined;
}

export interface LLM {
  id: string;
  name: string;
}

export enum AgentID {
  DATA_AGENT = 'data-agent',
}

export const fallbackModelID = AgentID.DATA_AGENT;

export const Agents: Record<AgentID, Agent> = {
  [AgentID.DATA_AGENT]: {
    id: AgentID.DATA_AGENT,
    name: 'Data Agent',
    maxLength: 12000,
    tokenLimit: 4000,
    llm: undefined,
  },
};

export const AgentList = Object.values(Agents);
