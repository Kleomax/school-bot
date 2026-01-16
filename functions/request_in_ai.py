import aiohttp

from config import system_prompt

async def request_ai(api_key: str, prompt: str) -> dict | bool:
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "deepseek-ai/DeepSeek-R1-0528",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            status_code = response.status

            json_data = await response.json()

    if status_code == 200:
        return json_data
    else:
        return False
