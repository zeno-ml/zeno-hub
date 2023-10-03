import type { ComponentType } from 'svelte';
import AudioTranscription from './views/AudioTranscription.svelte';
import Chatbot from './views/Chatbot.svelte';
import Codegen from './views/Codegen.svelte';
import ImageClassification from './views/ImageClassification.svelte';
import OpenAiChat from './views/OpenAIChat.svelte';
import OpenAiChatMarkdown from './views/OpenAIChatMarkdown.svelte';
import SpaceSeparatedValues from './views/SpaceSeparatedValues.svelte';
import TextClassification from './views/TextClassification.svelte';

// MUST update /backend/zeno_backend/routers/sdk.py when adding new views
export const viewMap: Record<string, ComponentType> = {
	'audio-transcription': AudioTranscription,
	'code-generation': Codegen,
	'image-classification': ImageClassification,
	'openai-chat-markdown': OpenAiChatMarkdown,
	'openai-chat': OpenAiChat,
	'space-separated-values': SpaceSeparatedValues,
	'text-classification': TextClassification,
	chatbot: Chatbot
};

export const optionsMap: Record<string, ComponentType> = {};
