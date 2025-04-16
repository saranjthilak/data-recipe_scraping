import argparse
import csv
import os
import time
from bs4 import BeautifulSoup
import requests


def parse_recipe(article):
    """
    Parse a recipe article and extract name, difficulty, and prep_time.
    Returns a dict with these key-value pairs.
    """
    # Extract name from the recipe-name class
    name_element = article.find('p', class_='recipe-name')
    name = name_element.text.strip() if name_element else "Unknown"

    # Extract difficulty from the recipe-difficulty class
    difficulty_element = article.find('span', class_='recipe-difficulty')
    difficulty = difficulty_element.text.strip() if difficulty_element else "Unknown"

    # Extract prep time from the recipe-cooktime class
    prep_time_element = article.find('span', class_='recipe-cooktime')
    prep_time = prep_time_element.text.strip() if prep_time_element else "Unknown"

    return {
        'name': name,
        'difficulty': difficulty,
        'prep_time': prep_time
    }

def parse(html):
    """
    Parse the HTML content to extract all recipes.
    Returns a list of recipe dicts.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Find all recipe articles
    recipe_articles = soup.find_all('div', class_='recipe')

    # Parse each recipe
    recipes = []
    for article in recipe_articles:
        recipe_data = parse_recipe(article)
        recipes.append(recipe_data)

    return recipes

def write_csv(ingredient, recipes):
    """
    Write recipes to a CSV file named {ingredient}.csv in the recipes directory.
    """
    # Ensure the recipes directory exists
    os.makedirs('recipes', exist_ok=True)

    # Create the file path
    file_path = os.path.join('recipes', f"{ingredient}.csv")

    # Write to CSV
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        if recipes:
            fieldnames = recipes[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for recipe in recipes:
                writer.writerow(recipe)

def scrape_from_file(ingredient):
    """
    Load HTML from a local file for offline testing.
    """
    with open(f"pages/{ingredient}.html", "r", encoding='utf-8') as file:
        return file.read()

def scrape_from_internet(ingredient, start=0):
    """
    Fetch HTML content for a given ingredient from the website.
    The start parameter is for pagination (each page has 12 recipes).
    """
    url = f"https://recipes.lewagon.com/?search[query]={ingredient}"

    # Add start parameter for pagination if it's not the first page
    if start > 0:
        url += f"&start={start}"

    # Send request and get response
    response = requests.get(url)

    # Add a small delay to be respectful to the server
    time.sleep(1)

    return response.text

def main():
    """
    Main function to orchestrate the scraping process.
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Scrape recipes for a given ingredient')
    parser.add_argument('ingredient', type=str, help='Ingredient to search for')
    args = parser.parse_args()

    ingredient = args.ingredient
    all_recipes = []

    # Scrape three pages (36 recipes if available)
    for page in range(3):
        start = page * 12  # Each page has 12 recipes

        # Get HTML content
        html = scrape_from_internet(ingredient, start)

        # Parse recipes from this page
        page_recipes = parse(html)

        # If no recipes were found on this page, break the loop
        if not page_recipes:
            break

        # Add recipes from this page to the complete list
        all_recipes.extend(page_recipes)

        print(f"Scraped page {page+1}: found {len(page_recipes)} recipes")

    # Write all recipes to CSV
    write_csv(ingredient, all_recipes)

    print(f"Total: {len(all_recipes)} recipes saved to recipes/{ingredient}.csv")

if __name__ == "__main__":
    main()
