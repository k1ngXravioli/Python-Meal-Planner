import tkinter as tk
from tkinter import messagebox
import random


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self, data):
        self.root = TreeNode(data)

    def insert(self, data):
        self._insert_rec(self.root, data)

    def _insert_rec(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_rec(node.left, data)
        else:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_rec(node.right, data)

    def get_planned_meals(self):
        meals = []
        self._in_order_traversal(self.root, meals)
        return meals

    def _in_order_traversal(self, node, meals):
        if node:
            self._in_order_traversal(node.left, meals)
            meals.append(node.data)
            self._in_order_traversal(node.right, meals)


class MealPlanner:
    def __init__(self, master):
        self.master = master
        self.master.title("Meal Planner")
        self.master.geometry("400x400")
        self.master.config(bg="#f7f7f7")

        self.tree = None

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(
            self.master,
            text="Welcome to the Meal Planner!",
            bg="#f7f7f7",
            font=("Arial", 16)
        )
        self.label.pack(pady=10)

        self.meal_entry = tk.Entry(self.master, width=30)
        self.meal_entry.pack(pady=10)

        self.plan_button = tk.Button(
            self.master,
            text="Plan Meal",
            command=self.plan_meal
        )
        self.plan_button.pack(pady=5)

        self.recommend_button = tk.Button(
            self.master,
            text="Get Recommendation",
            command=self.get_recommendation
        )
        self.recommend_button.pack(pady=5)

        self.display_area = tk.Text(
            self.master,
            width=40,
            height=10,
            bg="#ffffff",
            font=("Arial", 12)
        )
        self.display_area.pack(pady=10)

    def plan_meal(self):
        meal = self.meal_entry.get().strip()

        if meal == "":
            messagebox.showerror("Input Error", "Please enter a meal.")
            return

        if self.tree is None:
            self.tree = BinaryTree(meal)
        else:
            self.tree.insert(meal)

        self.meal_entry.delete(0, tk.END)
        self.display_planned_meals()

    def display_planned_meals(self):
        self.display_area.delete("1.0", tk.END)

        if self.tree:
            meals = self.tree.get_planned_meals()
            self.display_area.insert(
                tk.END,
                "Planned Meals:\n\n" + "\n".join(meals)
            )
        else:
            self.display_area.insert(
                tk.END,
                "No meals planned yet."
            )

    def get_recommendation(self):
        if self.tree is None:
            messagebox.showwarning(
                "Recommendation",
                "No meals have been planned yet."
            )
            return

        meals = self.tree.get_planned_meals()
        recommendation = random.choice(meals)

        messagebox.showinfo(
            "Meal Recommendation",
            f"How about: {recommendation}!"
        )


def main():
    root = tk.Tk()
    app = MealPlanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
