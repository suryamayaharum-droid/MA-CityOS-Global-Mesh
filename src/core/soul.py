import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env")

class CitySoul:
    """O Coração e Alma da MA-CityOS. Conexão unificada via OpenRouter."""
    
    def __init__(self, model="google/gemini-2.0-flash-001"):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        self.model = model

    def think(self, prompt, system_instruction="Você é a Alma da MA-CityOS."):
        response = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://macityos.org", # Site opcional para OpenRouter
                "X-Title": "MA-CityOS",
            },
            model=self.model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    soul = CitySoul()
    print("✨ Alma da Cidade (Almathea) conectada ao fluxo holográfico.")
