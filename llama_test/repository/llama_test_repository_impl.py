from llama_test.repository.llama_test_repository import LlamaTestRepository
# from langchain_community.llms import Ollama
# from langchain import PromptTemplate

from llama_cpp import Llama
from transformers import AutoTokenizer


class LlamaTestRepositoryImpl(LlamaTestRepository):
    __instance = None

    llm = Llama(model_path="/home/eddi/ggml-model-q4_k_m.gguf",
                n_ctx=512,
                n_gpu_layers=-1)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def generateText(self, userSendMessage):
        systemPrompt = "You are a helpful assistant."

        tokenizer = AutoTokenizer.from_pretrained("Saxo/Linkbricks-Horizon-AI-Korean-llama-3.1-sft-dpo-8B")

        messages = [
            {"role": "system", "content": f"{systemPrompt}"},
            {"role": "user", "content": f"{userSendMessage}"}
        ]

        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        generationKwargs = {
            "max_tokens": 512,
            "stop": ["<|eot_id|>"],
            "top_p": 0.9,
            "temperature": 0.6,
            "echo": True
        }

        response = self.llm(prompt, **generationKwargs)
        generatedText = response['choices'][0]['text'][len(prompt):]

        return { "generatedText": generatedText }