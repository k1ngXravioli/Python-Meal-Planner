# Python Tkinter Meal Planner

A desktop meal planner built in **Python** with **Tkinter**, using a **binary search tree (BST)** and **recursive in-order traversal** to keep meal names in alphabetical order.

## What it does

- Add meals through a graphical interface.
- Insert meal names into a binary search tree using alphabetical comparisons.
- Display the planned meals in sorted order using recursive in-order traversal.
- Display an error message when the meal field is empty.
- Suggest a randomly selected meal from the entries already added.
- Warn when a recommendation is requested before adding any meals.

## Technologies and concepts

**Python 3 · Tkinter · object-oriented programming · binary search trees · recursion · event-driven programming · input validation**

The code separates data structure logic (`TreeNode` and `BinaryTree`) from the graphical application (`MealPlanner`).

## Running the program

Python 3 and Tkinter are required. Tkinter is commonly included with desktop Python installations.

1. Download the `meal_planner.py` file or clone this repository.
2. In a terminal, run:

```bash
python meal_planner.py
```

On some systems, the command is `python3 meal_planner.py`.

3. Type a meal name and select **Plan Meal** to add it, or select **Get Recommendation** for a random suggestion.

## How the binary search tree works

A meal name is stored in a tree node. For each new meal, recursive insertion compares its name against the current node. Names that compare as smaller go left; others go right. An in-order traversal visits the left subtree, the current node and then the right subtree, producing an alphabetically ordered list according to Python's string comparison rules.

For example, inserting `Pasta`, `Curry` and `Salad` produces the ordered list:

```text
Curry
Pasta
Salad
```

## What I learned

Building the project helped me understand how a larger operation can be divided into smaller recursive calls. It also gave me practical experience combining a data structure with a GUI, validating user input, and updating an interface when application state changes.

## Current limitations

- Meals are kept in memory and are lost when the application closes.
- The BST is not self-balancing; sorted input can produce a less efficient tree.
- Duplicate meal names are allowed.
- Sorting is case-sensitive, following Python's default string comparison rules.
- No automated GUI tests or persistence are included in this version.

## Suggested manual checks

| Check | Expected behaviour |
| --- | --- |
| Add Pasta, Curry and Salad | Display Curry, Pasta, Salad |
| Submit an empty meal name | Show an input error dialog |
| Request a recommendation before adding meals | Show a warning |
| Request a recommendation after adding meals | Show one of the stored meals |

These are suggested checks, **not claims that an automated test suite has run**.

## Future improvements

- Add save/load support for meals between sessions.
- Support removing meals and avoiding duplicates.
- Add automated tests for insertion and traversal.
- Consider a balanced tree or simpler list for larger collections.

## Screenshots

A screenshot of the running Tkinter application can be added later in `screenshots/`.

---

This is an original learning project. The code in `meal_planner.py` reflects the implementation supplied for this portfolio, with formatting restored from the copied text.
