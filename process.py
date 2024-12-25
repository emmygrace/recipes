import re
import os


# Convert single recipe function
def convert_recipe_format(recipe_text):
    recipe_text = re.sub(r'^## (.*)', r'# \1', recipe_text, flags=re.MULTILINE)
    recipe_text = re.sub(r'^### (Ingredients.*)', r'## \1', recipe_text, flags=re.MULTILINE)
    recipe_text = re.sub(r'^### (Directions.*)', r'## \1', recipe_text, flags=re.MULTILINE)
    recipe_text = re.sub(r'^### (Notes.*)', r'## \1', recipe_text, flags=re.MULTILINE)

    def clean_directions(match):
        steps = re.findall(r'\d+\. \*\*(.*?)\*\*:\n   - (.*?)\n', match.group())
        return '\n'.join([f"{i + 1}. {step[1]}" for i, step in enumerate(steps)])

    recipe_text = re.sub(r'## Directions.*?(?=## Notes|$)', clean_directions, recipe_text, flags=re.S)

    metadata = (
        "Recipe Book: *Pastas*\n"
        "Tags: **pasta**, **daam**, **vegetarian**\n"
        "Servings: **4**\n"
        "Active Time: **20 minutes**\n"
        "Total Time: **30 minutes**\n"
    )
    recipe_text = re.sub(r'# (.*)', rf'# \1\n\n{metadata}', recipe_text, count=1)

    return recipe_text


# Process files recursively
def process_recipes_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_directory, f"updated_{file}")

                with open(input_path, 'r', encoding='utf-8') as f:
                    recipe_text = f.read()

                updated_recipe = convert_recipe_format(recipe_text)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(updated_recipe)


# Example usage
input_directory = './'
output_directory = './updated_recipes'
process_recipes_in_directory(input_directory, output_directory)
