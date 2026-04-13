


import sys


class GeminiClient:
    def __init__(self, ):
        self.api_key = sys.env.get("GOOGLE_API_KEY", "")

    async def generate_tasks(self, description: str) -> str:
        # Use Gemini API to generate tasks based on the description
        
        return "job-id-placeholder"