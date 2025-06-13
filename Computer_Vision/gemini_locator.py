import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env file")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Initialize the multimodal model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def find_element_coordinates(image_path: str, element_name: str) -> str:
    """
    Uses Gemini to locate the coordinates of an element in the given image.
    
    :param image_path: Path to the image file
    :param element_name: Name or description of the UI element
    :return: String description of coordinates
    """
    try:
        img = Image.open(image_path)
        response = model.generate_content([
            img,
            f"Return only the coordinates (x, y, width, height) of the UI element named: '{element_name}'."
        ])
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
