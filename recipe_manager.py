import json
import os

# Define the file path for data persistence
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")


# --- SECTION 1: File Handling Functions ---

def ensure_data_directory_exists():
    """Create the data directory if it does not already exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_recipes():
    """
    Load recipes from the JSON file into a Python list.
    Returns an empty list if the file doesn't exist or is invalid.
    """
    ensure_data_directory_exists()
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("\n⚠️ Warning: Failed to load existing data. Starting with an empty recipe list.")
        return []


def save_recipes(recipes):
    """Save the list of recipes to the JSON file."""
    ensure_data_directory_exists()
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(recipes, file, indent=4)
        print("\n✅ Recipes saved successfully!")
    except IOError as e:
        print(f"\n❌ Error saving recipes: {e}")


# --- SECTION 2: Core CRUD Functions ---

def add_recipe(recipes):
    """Collect user input to create and append a new recipe dictionary."""
    print("\n--- ➕ Add a New Recipe ---")
    
    title = input("Enter recipe title: ").strip()
    if not title:
        print("❌ Recipe title cannot be empty.")
        return

    # Check for duplicate titles (case-insensitive)
    for recipe in recipes:
        if recipe['title'].lower() == title.lower():
            print("❌ A recipe with this title already exists.")
            return

    category = input("Enter category (e.g., Breakfast, Dinner, Dessert): ").strip() or "General"
    
    print("Enter ingredients separated by commas (e.g., Flour, Sugar, Eggs):")
    ingredients_input = input("> ").strip()
    ingredients = [item.strip() for item in ingredients_input.split(",") if item.strip()]

    print("Enter cooking instructions:")
    instructions = input("> ").strip()

    # Build dictionary data structure
    new_recipe = {
        "title": title,
        "category": category,
        "ingredients": ingredients,
        "instructions": instructions
    }

    recipes.append(new_recipe)
    save_recipes(recipes)
    print(f"🎉 '{title}' was added successfully!")


def view_recipes(recipes):
    """Display all saved recipes formatted for reading."""
    print("\n--- 📖 All Recipes ---")
    if not recipes:
        print("No recipes found. Try adding one!")
        return

    for index, recipe in enumerate(recipes, start=1):
        print(f"\n[{index}] Title: {recipe['title']} (Category: {recipe.get('category', 'N/A')})")
        print(f"    Ingredients: {', '.join(recipe['ingredients'])}")
        print(f"    Instructions: {recipe['instructions']}")
        print("-" * 40)


def search_recipes(recipes):
    """Search for recipes matching a string in the title or ingredients."""
    print("\n--- 🔍 Search Recipes ---")
    if not recipes:
        print("No recipes stored to search through.")
        return

    query = input("Enter search term (title or ingredient): ").strip().lower()
    if not query:
        print("❌ Search term cannot be empty.")
        return

    matches = []
    for recipe in recipes:
        title_match = query in recipe['title'].lower()
        ingredient_match = any(query in ing.lower() for ing in recipe['ingredients'])
        if title_match or ingredient_match:
            matches.append(recipe)

    print(f"\nFound {len(matches)} matching recipe(s):")
    view_recipes(matches)


def edit_recipe(recipes):
    """Edit an existing recipe's details."""
    print("\n--- ✏️ Edit Recipe ---")
    if not recipes:
        print("No recipes available to edit.")
        return

    query = input("Enter the exact title of the recipe to edit: ").strip().lower()
    
    for recipe in recipes:
        if recipe['title'].lower() == query:
            print(f"\nEditing '{recipe['title']}' (Press ENTER to keep current value):")
            
            # Category
            new_category = input(f"New category [{recipe.get('category', 'General')}]: ").strip()
            if new_category:
                recipe['category'] = new_category

            # Ingredients
            current_ing = ", ".join(recipe['ingredients'])
            new_ing = input(f"New ingredients [{current_ing}]: ").strip()
            if new_ing:
                recipe['ingredients'] = [item.strip() for item in new_ing.split(",") if item.strip()]

            # Instructions
            new_inst = input(f"New instructions [{recipe['instructions']}]: ").strip()
            if new_inst:
                recipe['instructions'] = new_inst

            save_recipes(recipes)
            print(f"✅ '{recipe['title']}' updated successfully!")
            return

    print("❌ No matching recipe title found.")


def delete_recipe(recipes):
    """Delete a recipe by title after user confirmation."""
    print("\n--- 🗑️ Delete Recipe ---")
    if not recipes:
        print("No recipes available to delete.")
        return

    query = input("Enter the title of the recipe to delete: ").strip().lower()

    for index, recipe in enumerate(recipes):
        if recipe['title'].lower() == query:
            confirm = input(f"Are you sure you want to delete '{recipe['title']}'? (y/n): ").strip().lower()
            if confirm == 'y':
                deleted = recipes.pop(index)
                save_recipes(recipes)
                print(f"🗑️ Deleted '{deleted['title']}' from storage.")
            else:
                print("Action cancelled.")
            return

    print("❌ No matching recipe found.")


# --- SECTION 3: Main Menu CLI Loop ---

def display_menu():
    """Print the user interface option menu."""
    print("\n==================================")
    print("   🍳 RECIPE MANAGER CLI APP 🍳   ")
    print("==================================")
    print("1. View All Recipes")
    print("2. Add New Recipe")
    print("3. Search Recipes")
    print("4. Edit a Recipe")
    print("5. Delete a Recipe")
    print("6. Exit")
    print("==================================")


def main():
    """Main program control loop."""
    recipes = load_recipes()

    while True:
        display_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            view_recipes(recipes)
        elif choice == '2':
            add_recipe(recipes)
        elif choice == '3':
            search_recipes(recipes)
        elif choice == '4':
            edit_recipe(recipes)
        elif choice == '5':
            delete_recipe(recipes)
        elif choice == '6':
            print("\nGoodbye! Thank you for using Recipe Manager.")
            break
        else:
            print("❌ Invalid selection. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()