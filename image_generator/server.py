from dotenv import load_dotenv
load_dotenv()
import os

import json
from openai import OpenAI
from PIL import Image
import requests


# Set up OpenAI API client
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

input_file = "./image_generator/images.json"

# Output folder for images
output_folder = "generated_images"
os.makedirs(output_folder, exist_ok=True)

# Function to generate a professional image prompt
def create_prompt(packaging_name):
    return f"A high-quality, professional studio image of a {packaging_name}. Well-lit with a clean white background, suitable for e-commerce product listing."

# Load input data
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item in the input data
for item in data:
    packaging_id = item.get("id")
    packaging_name = item.get("packaging_name")
    
    if packaging_name:
        # Generate image prompt
        prompt = create_prompt(packaging_name)
        print(f"Generating image for {packaging_name}...")

        # Call OpenAI API to generate the image
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response["data"][0]["url"]
            
            # Download and save the image
            image_response = requests.get(image_url)
            image_path = os.path.join(output_folder, f"{packaging_id}_{packaging_name}.png")
            
            with open(image_path, "wb") as img_file:
                img_file.write(image_response.content)
            
            print(f"Image saved as {image_path}.")
        except Exception as e:
            print(f"Failed to generate image for {packaging_name}. Error: {e}")
