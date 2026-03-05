# 🌌 Generative AI & LangChain Lab

This directory is dedicated to exploring and implementing state-of-the-art Generative AI models using the **LangChain** framework. It serves as a sandbox for testing various Large Language Models (LLMs) and embedding techniques.

## 📂 Structure

- **`ChatModels/`**: Implementation of chat interfaces with multiple providers.
  - `googleModels/`: Integration with Gemini Pro / Flash.
  - `mistralModel/`: Integration with Mistral AI.
  - `openai/`: Integration with GPT-3.5 and GPT-4.
  - `Huggingface/`: Utilizing open-source models via Inference API or local transformers.
- **`EmbeddingModels/`**: Tools for generating vector representations of text.
  - `openaiEmbeddingmodels/`: Using `text-embedding-3-small` or `text-embedding-ada-002`.
  - `huggingfaceEmbeddingmodels/`: Using open-source embeddings (e.g., BGE, E5).

## 🛠️ Setup

1. **Virtual Environment**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. **Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=...
   GROQ_API_KEY=...
   MISTRAL_API_KEY=...
   HUGGINGFACEHUB_API_TOKEN=...
   ```

## 🧪 Experiments

Currently focused on:

- **Unified Prompting**: Developing prompts that work across different model architectures.
- **RAG Pre-processing**: Testing different embedding models for optimal retrieval performance.
- **LangChain Expression Language (LCEL)**: Building efficient chains for complex logic.

---

_Part of the [Master AI Repository](../README.md)._
