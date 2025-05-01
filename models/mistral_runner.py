import requests
import logging

logger = logging.getLogger(__name__)

class MistralRunner:
    def __init__(self, config):
        self.endpoint = config['endpoint']
        self.max_tokens = config['max_tokens']

    def query(self, prompt):
        try:
            # Log the prompt for debugging
            logger.debug(f"Sending prompt to Mistral: {prompt[:500]}...")
            response = requests.post(
                self.endpoint,
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "max_tokens": self.max_tokens,
                    "stream": False
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            answer = result.get("response", "").strip()
            logger.info(f"Received answer: {answer[:100]}...")
            return answer
        except Exception as e:
            logger.error(f"Error querying Mistral: {e}")
            raise