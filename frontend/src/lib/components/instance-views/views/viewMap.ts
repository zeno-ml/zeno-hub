import type { ComponentType } from 'svelte';
import AudioTranscription from './views/AudioTranscription.svelte';
import Chatbot from './views/Chatbot.svelte';
import Codegen from './views/Codegen.svelte';
import ImageClassification from './views/ImageClassification.svelte';
import OpenAiChat from './views/OpenAIChat.svelte';
import OpenAiChatMarkdown from './views/OpenAIChatMarkdown.svelte';
import RAG from './views/RAG.svelte';
import SpaceSeparatedValues from './views/SpaceSeparatedValues.svelte';
import TextClassification from './views/TextClassification.svelte';

// MUST update /backend/zeno_backend/routers/sdk.py when adding new views
export const viewMap: Record<string, ComponentType> = {
	'audio-transcription': AudioTranscription,
	chatbot: Chatbot,
	'code-generation': Codegen,
	'image-classification': ImageClassification,
	'openai-chat': OpenAiChat,
	'openai-chat-markdown': OpenAiChatMarkdown,
	rag: RAG,
	'space-separated-values': SpaceSeparatedValues,
	'text-classification': TextClassification
};

export const optionsMap: Record<string, ComponentType> = {};
