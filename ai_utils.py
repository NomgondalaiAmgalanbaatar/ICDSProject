import os
import json
import requests
import base64
import io
from dotenv import load_dotenv
load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
try:
    from hume import HumeBatchClient, HumeStreamClient
    from hume.models.config import LanguageConfig
except ImportError:
    HumeBatchClient = None

class AIHandler:
    def __init__(self):
        # PLACEHOLDERS: User must set these or add them to OS Environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY") 
        self.hume_api_key = os.getenv("HUME_API_KEY")

        self.openai_client = None
        if OpenAI and self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Hume setup (simplified for demo, typically requires async for stream)
        self.hume_client = None
        # Note: Hume integration often requires more complex async setup or batch processing.
        # For this synchronous GUI, we might use simple API requests if SDK is complex.

    def get_chat_response(self, history, user_message, username=None):
        """
        Get a standardized response from OpenAI Chatbot with user context.
        """
        if not self.openai_client:
            return "Error: OpenAI API Key not found or library missing."

        messages = [{"role": "system", "content": "You are a helpful chat assistant participating in a group chat."}]
        
        # Add chat history for context (last few messages)
        if history:
            context_messages = history[-10:]  # Last 10 messages for context
            context_text = "\n".join(context_messages)
            messages.append({"role": "system", "content": f"Recent chat history:\n{context_text}"})
        
        # Add user context if provided
        if username:
            messages.append({"role": "system", "content": f"The user asking this question is: {username}"})
        
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"

    def extract_keywords(self, text):
        """
        Extract keywords from text using OpenAI.
        """
        if not self.openai_client:
            return "Error: OpenAI API Key not found."

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract 5 main keywords from the following text, separated by commas."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"

    def get_summary(self, text):
        """
        Summarize text using OpenAI.
        """
        if not self.openai_client:
            return "Error: OpenAI API Key not found."

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize the following chat conversation briefly."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment using Hume AI (Mock/Placeholder for now as Hume requires specific setup).
        If Hume is not configured, fall back to basic OpenAI sentiment or mock.
        """
        # Fallback to OpenAI if Hume is complex to set up synchronously in Tkinter
        if self.openai_client:
             try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Analyze the sentiment of this text. Return primarily an Emoji representing the emotion (e.g., 😊, 😠, 😢, 😐) followed by a one-word label."},
                        {"role": "user", "content": text}
                    ]
                )
                return response.choices[0].message.content
             except:
                 pass
        
        return "😐 Neutral (AI N/A)"

    def generate_image(self, prompt):
        """
        Generate image using DALL-E 3 and return base64 encoded data.
        Falls back to DALL-E 2 if DALL-E 3 is not available.
        """
        if not self.openai_client:
            return "Error: OpenAI API Key not found."
        
        try:
            # Try DALL-E 3 first (better quality)
            try:
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                    quality="standard"  # or "hd" for higher quality
                )
            except Exception as e:
                # Fallback to DALL-E 2 if DALL-E 3 fails
                print(f"DALL-E 3 failed, falling back to DALL-E 2: {e}")
                response = self.openai_client.images.generate(
                    model="dall-e-2",
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
            
            # Get the image URL
            image_url = response.data[0].url
            
            # Download the image
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code == 200:
                # Convert to base64 for broadcasting
                image_bytes = img_response.content
                base64_str = base64.b64encode(image_bytes).decode('utf-8')
                return base64_str
            else:
                return f"Error: Failed to download image (status {img_response.status_code})"
            
        except Exception as e:
            return f"Image Gen Error: {str(e)}"
