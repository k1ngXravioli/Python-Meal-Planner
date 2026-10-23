# Python Tkinter Meal Planner

A desktop meal planner I built in **Python with Tkinter**. It uses a **binary search tree (BST)**, recursive insertion and in-order traversal to keep meal names in alphabetical order.

## What it does

- Add meals **one at a time** through a graphical interface.
- Display added meals alphabetically in a separate list.
- Suggest a randomly selected meal from the current list.
- Reject empty entries and duplicate meal names (ignoring capitalisation).
- Remove a selected meal or clear the full list.
- Show clear success/error messages and a count of planned meals.
- Use explicit light text/background colours to improve readability on macOS.

**Note:** Meals are currently stored in memory and are lost when the program closes.

## How to run it on macOS

Open **Terminal**, then paste these commands to download the latest version from GitHub and open the app:

```bash
cd ~/Downloads
curl -fL https://raw.githubusercontent.com/k1ngXravioli/Python-Meal-Planner/main/meal_planner.py -o meal_planner.py
python3 meal_planner.py
```

Use **one meal at a time**: type `Burger`, press **Add meal** (or Return), then repeat with `Pasta` and `Pizza`. The separate *Your planned meals* list should show:

```text
Burger
Pasta
Pizza
```

Click **Suggest a meal** for a recommendation, or select a meal in the list and click **Remove selected**.

**Requirements:** Python 3.10 or newer and Tkinter. If macOS says `No module named '_tkinter'`, use a Python distribution with Tkinter support.

## Technical implementation

**Stack:** Python · Tkinter / ttk · Object-oriented programming · Binary Search Tree · Recursion · Input Validation.

The data model is intentionally separate from the UI:

- `TreeNode` stores one meal name and pointers to left and right nodes.
- `BinaryTree.insert()` recursively inserts items, comparing meal names case-insensitively.
- `BinaryTree.get_planned_meals()` uses an in-order traversal to retrieve sorted meals.
- `BinaryTree.remove()` rebuilds a small tree after deleting an entry.
- `MealPlanner` handles text entry, the listbox, buttons and user feedback.

For example, inserting `Pizza`, `Burger`, then `Pasta` produces `Burger`, `Pasta`, `Pizza`.

## Tests

Three tests verify BST insertion/sorting, case-insensitive duplicate handling, and removing/clearing entries. Run:

```bash
python3 -m unittest -v test_meal_planner.py
```

The model tests and a virtual-display GUI interaction test passed during the latest update. The appearance on macOS still needs a real Mac check.

## What I learned

This project helped me understand how recursion divides a larger operation into smaller calls, how data structures can support GUI features, and why error handling and interface readability matter when testing software.

## Changes made after testing on a Mac

The first version had difficult-to-read text in macOS dark mode, and it was unclear where to type new meals versus where saved meals should appear. The updated version uses explicit text colours, a distinct meal-entry field, a separate list, clearer instructions and improved controls.

## Limitations and future work

- No persistent storage yet.
- The BST is not self-balancing for every insertion order.
- This is a small educational desktop project rather than a deployed web service.
- Automated GUI testing on an actual Mac has not yet been performed.

Ideas for future updates: save and load meals, add a date-based weekly planner, and improve automated GUI tests.

## Screenshot

A screenshot from the running macOS application can be added after testing the updated version.
