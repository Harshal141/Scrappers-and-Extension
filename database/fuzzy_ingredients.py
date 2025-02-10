import psycopg2
import os
import json
from thefuzz import fuzz

# Connect to the database
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    dbname='content',
    user='postgres',
    password=os.getenv('DB_PASS')
)
cur = conn.cursor()

# Fetch all ingredient details
cur.execute("SELECT id, name, image, level, parent_id FROM ingredient")
ingredients = cur.fetchall()

# Define similarity threshold
SIMILARITY_THRESHOLD = 90  # Adjust as needed

# Convert list to a dictionary format
ingredient_dict = {row[1]: {"id": row[0], "name": row[1], "image": row[2], "level": row[3], "parent_id": row[4]} for row in ingredients}

# Function to group similar names along with their details
def group_similar_ingredients(ingredients, threshold=SIMILARITY_THRESHOLD):
    groups = []
    seen = set()

    ingredient_names = list(ingredient_dict.keys())

    for name in ingredient_names:
        if name in seen:
            continue
        group = [other for other in ingredient_names if fuzz.ratio(name, other) >= threshold]
        if len(group) > 1:
            groups.append([ingredient_dict[item] for item in group])
            seen.update(group)

    return groups

# Get groups of similar ingredients
similar_groups = group_similar_ingredients(ingredients)

# Save the results as JSON
output_file = "./database/similar_ingredients.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(similar_groups, f, indent=4, ensure_ascii=False)

print(f"Similar ingredient groups saved to {output_file}")

# Close the connection
cur.close()
conn.close()
