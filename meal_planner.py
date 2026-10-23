"""A simple desktop meal planner built with Tkinter and a binary search tree.

Add one meal at a time, browse meals in alphabetical order and get a random
recommendation. The data structure is intentionally written without external
packages so that the recursion and tree logic are easy to study.
"""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk


class TreeNode:
    """One node in a binary search tree of meal names."""

    def __init__(self, meal: str):
        self.meal = meal
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


class BinaryTree:
    """Store meal names alphabetically, ignoring case when comparing."""

    def __init__(self):
        self.root: TreeNode | None = None

    def insert(self, meal: str) -> bool:
        """Add a meal, returning False if the name already exists."""
        if self.root is None:
            self.root = TreeNode(meal)
            return True
        return self._insert_recursive(self.root, meal)

    def _insert_recursive(self, node: TreeNode, meal: str) -> bool:
        comparison = (meal.casefold() > node.meal.casefold()) - (
            meal.casefold() < node.meal.casefold()
        )
        if comparison == 0:
            return False
        if comparison < 0:
            if node.left is None:
                node.left = TreeNode(meal)
                return True
            return self._insert_recursive(node.left, meal)
        if node.right is None:
            node.right = TreeNode(meal)
            return True
        return self._insert_recursive(node.right, meal)

    def get_planned_meals(self) -> list[str]:
        """Return an alphabetically sorted list using in-order recursion."""
        meals: list[str] = []
        self._in_order(self.root, meals)
        return meals

    def _in_order(self, node: TreeNode | None, meals: list[str]) -> None:
        if node is not None:
            self._in_order(node.left, meals)
            meals.append(node.meal)
            self._in_order(node.right, meals)

    def remove(self, meal: str) -> bool:
        """Rebuild the tree without the selected meal (simple for this small app)."""
        remaining = [m for m in self.get_planned_meals() if m.casefold() != meal.casefold()]
        if len(remaining) == len(self.get_planned_meals()):
            return False
        self.root = None
        # Inserting middle values first avoids an unnecessarily deep tree here.
        self._insert_balanced(remaining)
        return True

    def _insert_balanced(self, sorted_meals: list[str]) -> None:
        if not sorted_meals:
            return
        midpoint = len(sorted_meals) // 2
        self.insert(sorted_meals[midpoint])
        self._insert_balanced(sorted_meals[:midpoint])
        self._insert_balanced(sorted_meals[midpoint + 1 :])

    def clear(self) -> None:
        self.root = None


class MealPlanner:
    BG = "#F3F6FC"
    WHITE = "#FFFFFF"
    INK = "#17243B"
    MUTED = "#64748B"
    ACCENT = "#275DCE"
    ACCENT_DARK = "#214FAF"
    BORDER = "#CCD6E5"
    SUCCESS = "#12694B"
    ERROR = "#B3261E"

    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Meal Planner")
        self.master.geometry("600x630")
        self.master.minsize(490, 520)
        self.master.configure(bg=self.BG)
        self.tree = BinaryTree()
        self._configure_styles()
        self._build_interface()
        self._refresh_list()
        self.entry.focus_set()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.master)
        # macOS Aqua widgets can inherit dark colours, even on a white window.
        # Clam uses the explicit light foreground/background colours below.
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Planner.TEntry", fieldbackground=self.WHITE, foreground=self.INK,
                        background=self.WHITE, bordercolor=self.BORDER, padding=10,
                        insertcolor=self.INK, font=("Arial", 12))
        style.map("Planner.TEntry", fieldbackground=[("disabled", self.BG)],
                  foreground=[("disabled", self.MUTED)])
        style.configure("Primary.TButton", font=("Arial", 11, "bold"),
                        background=self.ACCENT, foreground=self.WHITE, borderwidth=0,
                        padding=(14, 11))
        style.map("Primary.TButton", background=[("active", self.ACCENT_DARK),
                                                   ("disabled", self.BORDER)],
                  foreground=[("disabled", self.MUTED), ("active", self.WHITE)])
        style.configure("Secondary.TButton", font=("Arial", 10, "bold"),
                        background=self.WHITE, foreground=self.INK, borderwidth=1,
                        bordercolor=self.BORDER, padding=(12, 9))
        style.map("Secondary.TButton", background=[("active", "#E5EAF4"),
                                                     ("disabled", self.BG)],
                  foreground=[("disabled", self.MUTED)])

    def _label(self, parent: tk.Widget, text: str, *, size: int = 11,
               bold: bool = False, color: str | None = None, bg: str | None = None) -> tk.Label:
        return tk.Label(parent, text=text, font=("Arial", size, "bold" if bold else "normal"),
                        foreground=color or self.INK, background=bg or self.BG,
                        anchor="w", justify="left")

    def _build_interface(self) -> None:
        layout = tk.Frame(self.master, background=self.BG, padx=27, pady=22)
        layout.pack(fill="both", expand=True)

        self._label(layout, "Meal Planner", size=23, bold=True).pack(anchor="w")
        self._label(layout, "Add meals one at a time, then choose a recommendation.",
                    color=self.MUTED).pack(anchor="w", pady=(3, 24))

        self._label(layout, "Meal name", bold=True).pack(anchor="w", pady=(0, 7))
        add_row = tk.Frame(layout, background=self.BG)
        add_row.pack(fill="x")
        self.entry = ttk.Entry(add_row, style="Planner.TEntry", font=("Arial", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=3, padx=(0, 9))
        self.entry.bind("<Return>", lambda event: self.add_meal())
        self.add_button = ttk.Button(add_row, text="+ Add meal", style="Primary.TButton",
                                     command=self.add_meal)
        self.add_button.pack(side="right")
        self._label(layout, "Example: type Burger, click Add meal, then type Pasta.",
                    color=self.MUTED, size=10).pack(anchor="w", pady=(8, 22))

        list_header = tk.Frame(layout, background=self.BG)
        list_header.pack(fill="x", pady=(0, 9))
        self._label(list_header, "Your planned meals", size=14, bold=True).pack(side="left")
        self.count_label = self._label(list_header, "0 meals", color=self.MUTED, size=10)
        self.count_label.pack(side="right")

        list_frame = tk.Frame(layout, background=self.WHITE, highlightbackground=self.BORDER,
                              highlightthickness=1)
        list_frame.pack(fill="both", expand=True)
        self.meal_list = tk.Listbox(list_frame, font=("Arial", 12),
                                   bg=self.WHITE, fg=self.INK, selectbackground=self.ACCENT,
                                   selectforeground=self.WHITE, activestyle="none",
                                   relief="flat", borderwidth=0, highlightthickness=0,
                                   exportselection=False)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.meal_list.yview)
        self.meal_list.configure(yscrollcommand=scrollbar.set)
        self.meal_list.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 4))

        actions = tk.Frame(layout, background=self.BG)
        actions.pack(fill="x", pady=(15, 0))
        self.recommend_button = ttk.Button(actions, text="Suggest a meal",
                                            style="Primary.TButton", command=self.recommend_meal)
        self.recommend_button.pack(side="left", padx=(0, 9))
        self.remove_button = ttk.Button(actions, text="Remove selected",
                                         style="Secondary.TButton", command=self.remove_selected)
        self.remove_button.pack(side="left", padx=(0, 9))
        self.clear_button = ttk.Button(actions, text="Clear all",
                                        style="Secondary.TButton", command=self.clear_meals)
        self.clear_button.pack(side="left")

        self.status = self._label(layout, "Enter your first meal to get started.",
                                  size=10, color=self.MUTED)
        self.status.pack(anchor="w", fill="x", pady=(16, 0))
        self.meal_list.bind("<<ListboxSelect>>", lambda event: self._sync_buttons())

    def _set_status(self, message: str, color: str | None = None) -> None:
        self.status.configure(text=message, foreground=color or self.MUTED)

    def _sync_buttons(self) -> None:
        meals_exist = bool(self.tree.get_planned_meals())
        self.recommend_button.configure(state="normal" if meals_exist else "disabled")
        self.clear_button.configure(state="normal" if meals_exist else "disabled")
        self.remove_button.configure(state="normal" if self.meal_list.curselection() else "disabled")

    def _refresh_list(self) -> None:
        meals = self.tree.get_planned_meals()
        self.meal_list.delete(0, tk.END)
        for name in meals:
            self.meal_list.insert(tk.END, f"  {name}")
        self.count_label.configure(text=f"{len(meals)} meal{'s' if len(meals) != 1 else ''}")
        self._sync_buttons()

    def add_meal(self) -> None:
        name = self.entry.get().strip()
        if not name:
            self._set_status("Please type a meal name first.", self.ERROR)
            self.entry.focus_set()
            return
        if not self.tree.insert(name):
            self._set_status(f"{name} is already on your list.", self.ERROR)
            self.entry.selection_range(0, tk.END)
            self.entry.focus_set()
            return
        self.entry.delete(0, tk.END)
        self._refresh_list()
        self._set_status(f"Added {name} successfully.", self.SUCCESS)
        self.entry.focus_set()

    def recommend_meal(self) -> None:
        meals = self.tree.get_planned_meals()
        if not meals:
            self._set_status("Add a meal before requesting a suggestion.", self.ERROR)
            return
        choice = random.choice(meals)
        self._set_status(f"Today's suggestion: {choice}", self.SUCCESS)

    def remove_selected(self) -> None:
        selection = self.meal_list.curselection()
        if not selection:
            self._set_status("Select a meal in the list before removing it.", self.ERROR)
            return
        name = self.tree.get_planned_meals()[selection[0]]
        self.tree.remove(name)
        self._refresh_list()
        self._set_status(f"Removed {name}.", self.SUCCESS)

    def clear_meals(self) -> None:
        self.tree.clear()
        self._refresh_list()
        self._set_status("Your meal list is empty.")


def main() -> None:
    root = tk.Tk()
    MealPlanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
