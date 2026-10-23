"""Tests for the meal planner's binary search tree (no GUI needed)."""

import unittest
from meal_planner import BinaryTree


class MealTreeTests(unittest.TestCase):
    def test_insert_and_sort(self):
        tree = BinaryTree()
        for meal in ("Pizza", "Burger", "Pasta"):
            self.assertTrue(tree.insert(meal))
        self.assertEqual(tree.get_planned_meals(), ["Burger", "Pasta", "Pizza"])

    def test_case_insensitive_comparisons(self):
        tree = BinaryTree()
        for meal in ("ziti", "Apple", "banana"):
            self.assertTrue(tree.insert(meal))
        self.assertEqual(tree.get_planned_meals(), ["Apple", "banana", "ziti"])
        self.assertFalse(tree.insert("BANANA"))
        self.assertEqual(len(tree.get_planned_meals()), 3)

    def test_remove_and_clear(self):
        tree = BinaryTree()
        for meal in ("Pizza", "Burger", "Pasta", "Toast"):
            tree.insert(meal)
        self.assertTrue(tree.remove("BURGER"))
        self.assertEqual(tree.get_planned_meals(), ["Pasta", "Pizza", "Toast"])
        self.assertFalse(tree.remove("Missing"))
        tree.clear()
        self.assertEqual(tree.get_planned_meals(), [])


if __name__ == "__main__":
    unittest.main()
