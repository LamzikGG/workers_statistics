from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

class LLMService_analyze_json:                 
    def __init__(self):
        api_key = os.getenv("OPEN_API_KEY")
        folder_id = os.getenv("YANDEX_CLOUD_FOLDER")
        self.model = os.getenv("YANDEX_CLOUD_MODEL", "yandexgpt-lite")
        self.client = AsyncOpenAI(
            api_key=api_key,  
            base_url="https://llm.api.cloud.yandex.net/v1",
            default_headers={
                "x-folder-id": folder_id  
            }
        )
        self.folder_id = folder_id

    async def analyze_json_file(self, data: list[dict]) -> str:
        json_str = json.dumps(data, ensure_ascii=False) 
        prompt = (
            "Проверь файлы и сделай выжимку из данных.\n"
            f"Данные: {json_str}"
        )
        
        response = await self.client.chat.completions.create(
            model=f"gpt://{self.folder_id}/{self.model}",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
"""
class ChatingToLLM:
    def __init__(self):
        api_key = os.getenv("open_api_key")
        folder_id = os.getenv("yandex_cloud_folder")
        self.model = os.getenv("yandex_cloud_model", "yandexgpt-lite")
        self.client = AsyncOpenAI(
            api_key=api_key,  
            base_url="https://llm.api.cloud.yandex.net/v1",
            default_headers={
                "x-folder-id": folder_id  
            }
        )
        self.folder_id = folder_id
    def chatting_to_LLM():
        return



async def main():
    test_data = [{"key": "value"}]
    service = LLMService_analyze_json()
    result = await service.analyze_json_file(test_data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
"""