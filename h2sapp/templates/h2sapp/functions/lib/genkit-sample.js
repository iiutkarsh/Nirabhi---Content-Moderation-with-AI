"use strict";
var __asyncValues = (this && this.__asyncValues) || function (o) {
    if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
    var m = o[Symbol.asyncIterator], i;
    return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () { return this; }, i);
    function verb(n) { i[n] = o[n] && function (v) { return new Promise(function (resolve, reject) { v = o[n](v), settle(resolve, reject, v.done, v.value); }); }; }
    function settle(resolve, reject, d, v) { Promise.resolve(v).then(function(v) { resolve({ value: v, done: d }); }, reject); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.menuSuggestion = void 0;
// Import the Genkit core libraries and plugins.
const genkit_1 = require("genkit");
const vertexai_1 = require("@genkit-ai/vertexai");
// Import Firebase Functions
const https_1 = require("firebase-functions/v2/https");
// Import Secret Manager
const params_1 = require("firebase-functions/params");
// Define API key using Firebase Secrets
const apiKey = (0, params_1.defineSecret)("GOOGLE_GENAI_API_KEY");
// Initialize AI with Vertex AI plugin
const ai = (0, genkit_1.genkit)({
    plugins: [
        (0, vertexai_1.vertexAI)({ location: "us-central1" }),
    ],
});
// Define a flow for menu suggestions
const menuSuggestionFlow = ai.defineFlow({
    name: "menuSuggestionFlow",
    inputSchema: genkit_1.z.string().describe("A restaurant theme").default("seafood"),
    outputSchema: genkit_1.z.string(),
    streamSchema: genkit_1.z.string(),
}, async (subject, { sendChunk }) => {
    var _a, e_1, _b, _c;
    // Construct a request and send it to the model API.
    const prompt = `Suggest an item for the menu of a 
    ${subject} themed restaurant`;
    const { response, stream } = await ai.generateStream({
        model: vertexai_1.gemini15Flash,
        prompt: prompt,
        config: {
            temperature: 1,
        },
    });
    try {
        for (var _d = true, stream_1 = __asyncValues(stream), stream_1_1; stream_1_1 = await stream_1.next(), _a = stream_1_1.done, !_a;) {
            _c = stream_1_1.value;
            _d = false;
            try {
                const chunk = _c;
                sendChunk(chunk.text);
            }
            finally {
                _d = true;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (!_d && !_a && (_b = stream_1.return)) await _b.call(stream_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return (await response).text;
});
// Export Firebase Cloud Function
exports.menuSuggestion = (0, https_1.onCallGenkit)({ secrets: [apiKey] }, menuSuggestionFlow);
//# sourceMappingURL=genkit-sample.js.map