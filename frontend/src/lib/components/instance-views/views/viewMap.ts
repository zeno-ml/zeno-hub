import type { ComponentType } from 'svelte';
import ImageSegmentationOptions from './options/ImageSegmentationOptions.svelte';
import AudioTranscription from './views/AudioTranscription.svelte';
import Chatbot from './views/Chatbot.svelte';
import Codegen from './views/Codegen.svelte';
import ImageClassification from './views/ImageClassification.svelte';
import ImageSegmentation from './views/ImageSegmentation.svelte';
import OpenAiChat from './views/OpenAIChat.svelte';
import TextClassification from './views/TextClassification.svelte';

// MUST update /backend/zeno_backend/routers/sdk.py when adding new views
export const viewMap: Record<string, ComponentType> = {
	'audio-transcription': AudioTranscription,
	chatbot: Chatbot,
	'code-generation': Codegen,
	'image-classification': ImageClassification,
	'image-segmentation': ImageSegmentation,
	'openai-chat': OpenAiChat,
	'text-classification': TextClassification
};

export const optionsMap: Record<string, ComponentType> = {
	'image-segmentation': ImageSegmentationOptions
};
