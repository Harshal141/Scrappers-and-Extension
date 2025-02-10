import os
import json
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# Database connection
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    dbname='content',
    user='postgres',
    password=os.getenv('DB_PASS')
)
cur = conn.cursor()

# Fetch images for product ID 9783
product_id = 9783
cur.execute("SELECT images FROM product WHERE id = %s", (product_id,))
product = cur.fetchone()

if not product or not product[0]:
    print(f"No images found for product ID {product_id}")
else:
    image_urls = product[0]  # Assuming images are stored as a JSON array

    def describe_image(image_url):
        """
        Uses OpenAI Vision API to generate a detailed description of the image.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error processing {image_url}: {e}")
            return "Error"

    # Get descriptions for each image
    image_descriptions = [(img, describe_image(img)) for img in image_urls]

    # Prepare ranking prompt
    ranking_prompt = "Here are several product images with their descriptions. Rank them from most visually appealing and relevant to least:\n\n"
    for idx, (img, desc) in enumerate(image_descriptions):
        ranking_prompt += f"{idx + 1}. Image: {img}\nDescription: {desc}\n\n"

    ranking_prompt += (
        "Return the rankings as a JSON array with the most relevant image first, like this:\n"
        "[\"image_url_1\", \"image_url_2\", \"image_url_3\"]"
    )

    # Get ranking order from GPT-4o-mini
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": ranking_prompt}],
        )
        ai_result = response.choices[0].message.content.strip()

        # Parse AI's response into a valid JSON list
        new_image_order = json.loads(ai_result)

        # Print old and new order
        print(f"\n🔹 Old Order for Product {product_id}:")
        print(json.dumps(image_urls, indent=4))

        print(f"\n✅ New Reordered Order for Product {product_id}:")
        print(json.dumps(new_image_order, indent=4))

    except Exception as e:
        print(f"Error ranking images: {e}")

# Close the connection
cur.close()
conn.close()
