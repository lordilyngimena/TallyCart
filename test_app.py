import pytest
from unittest.mock import MagicMock
import tkinter as tk

# Import your classes
from models import FoodItem
from interfaces import IOutputStrategy
from cart_logic import FoodCart
from strategies import GuiOutputStrategy
from main import FoodAppGUI


# 1. Test for models.py
def test_models_py():
    item = FoodItem("Apple", 1.50, "Fruit", 2)
    assert item.name == "Apple"
    assert item.price == 1.50
    assert item.quantity == 2
    # Check that negative price raises an error
    with pytest.raises(ValueError):
        FoodItem("BadApple", -1.0, "Fruit")


# 2. Test for interfaces.py
def test_interfaces_py():
    # Check that we can create a valid implementation of the interface
    class MockStrategy(IOutputStrategy):
        def clear_view(self): pass

        def display_item(self, item_string): pass

        def log_message(self, message): pass

        def update_totals(self, subtotal, discount, total, budget, balance): pass

    strategy = MockStrategy()
    assert isinstance(strategy, IOutputStrategy)


# 3. Test for cart_logic.py
def test_cart_logic_py():
    # Use a mock strategy so we don't need the real GUI
    mock_strategy = MagicMock(spec=IOutputStrategy)
    cart = FoodCart(mock_strategy)

    cart.add_item("Bread", 2.0, "Pantry", 3)  # Total = 6.0
    cart.discount = 1.0
    cart.budget = 10.0

    assert len(cart.get_all_items()) == 1
    assert cart.get_total() == 6.0

    # Check if the cart correctly calculated the balance (10 budget - 5 total = 5 balance)
    # (Subtotal 6 - Discount 1 = Total 5)
    mock_strategy.update_totals.assert_called_with(6.0, 1.0, 5.0, 10.0, 5.0)


# 4. Test for strategies.py
def test_strategies_py():
    # Create fake tkinter widgets
    mock_listbox = MagicMock()
    mock_notepad = MagicMock()
    mock_lbl_sub = MagicMock()
    mock_lbl_total = MagicMock()
    mock_lbl_budget = MagicMock()

    strategy = GuiOutputStrategy(mock_listbox, mock_notepad, mock_lbl_sub, mock_lbl_total, mock_lbl_budget)

    # Test the update_totals method logic for positive balance
    strategy.update_totals(10.0, 2.0, 8.0, 15.0, 7.0)
    mock_lbl_budget.config.assert_called_with(text="REMAINING BALANCE: P7.00", fg="green")


# 5. Test for main.py
def test_main_py():
    # Create a hidden Tkinter window to test the GUI initialization
    root = tk.Tk()
    root.withdraw()  # Hides the empty window from popping up during the test

    app = FoodAppGUI(root)

    # Verify the GUI successfully created the Cart and has categories
    assert app.cart is not None
    assert "Fruit" in app.categories

    # Clean up the Tkinter window
    root.destroy()