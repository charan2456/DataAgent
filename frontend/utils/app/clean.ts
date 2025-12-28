import { Conversation } from '@/types/chat';
import { AgentID, Agents } from '@/types/agent';

import { DEFAULT_SYSTEM_PROMPT, DEFAULT_TEMPERATURE } from './const';

export const cleanSelectedConversation = (conversation: Conversation) => {
  let updatedConversation = conversation;

  if (!updatedConversation.agent) {
    updatedConversation = {
      ...updatedConversation,
      agent: updatedConversation.agent || Agents[AgentID.DATA_AGENT],
    };
  }

  if (!updatedConversation.prompt) {
    updatedConversation = {
      ...updatedConversation,
      prompt: updatedConversation.prompt || DEFAULT_SYSTEM_PROMPT,
    };
  }

  if (!updatedConversation.temperature) {
    updatedConversation = {
      ...updatedConversation,
      temperature: updatedConversation.temperature || DEFAULT_TEMPERATURE,
    };
  }

  if (!updatedConversation.folderId) {
    updatedConversation = {
      ...updatedConversation,
      folderId: updatedConversation.folderId || null,
    };
  }

  if (!updatedConversation.messages) {
    updatedConversation = {
      ...updatedConversation,
      messages: updatedConversation.messages || [],
    };
  }

  return updatedConversation;
};
