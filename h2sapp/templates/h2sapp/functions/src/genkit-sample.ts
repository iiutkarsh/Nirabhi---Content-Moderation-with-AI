// Import the Genkit core libraries and plugins.
import {genkit, z} from "genkit";
import {vertexAI, gemini15Flash} from "@genkit-ai/vertexai";

// Import Firebase Functions
import {onCallGenkit} from "firebase-functions/v2/https";

// Import Secret Manager
import {defineSecret} from "firebase-functions/params";

// Define API key using Firebase Secrets
const apiKey = defineSecret("GOOGLE_GENAI_API_KEY");

// Initialize AI with Vertex AI plugin
const ai = genkit({
  plugins: [
    vertexAI({location: "us-central1"}),
  ],
});

// Define a flow for menu suggestions
const menuSuggestionFlow = ai.defineFlow(
  {
    name: "menuSuggestionFlow",
    inputSchema: z.string().describe("A restaurant theme").default("seafood"),
    outputSchema: z.string(),
    streamSchema: z.string(),
  },
  async (subject, {sendChunk}) => {
    // Construct a request and send it to the model API.
    const prompt = `Suggest an item for the menu of a 
    ${subject} themed restaurant`;

    const {response, stream} = await ai.generateStream({
      model: gemini15Flash,
      prompt: prompt,
      config: {
        temperature: 1,
      },
    });

    for await (const chunk of stream) {
      sendChunk(chunk.text);
    }

    return (await response).text;
  }
);

// Export Firebase Cloud Function
export const menuSuggestion = onCallGenkit({secrets: [apiKey]},
  menuSuggestionFlow);
