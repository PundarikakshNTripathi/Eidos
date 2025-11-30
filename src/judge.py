from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Judge:
    def __init__(self):
        if not GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Reasoning will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = "gemini-2.0-flash-exp" # Using Flash for speed/cost, switch to Pro if available/needed

    async def reason(self, source_code: str, tool_output: str, prompt: str) -> str:
        """
        The 'Reasoning' loop: Analyzes tool output in context of source code.
        """
        if not self.client:
            return "Error: GEMINI_API_KEY not configured."

        full_prompt = f"""
        You are Eidos, a Senior Systems Engineer.
        
        **Context:**
        I ran a system tool on the following source code.
        
        **Source Code:**
        ```{source_code}```
        
        **Tool Output:**
        ```{tool_output}```
        
        **Task:**
        {prompt}
        
        **Output Format:**
        Provide a concise, high-level engineering insight. Do not just repeat the tool output.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2, # Low temperature for analytical tasks
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return f"Error during reasoning: {str(e)}"

# Singleton instance
judge = Judge()
