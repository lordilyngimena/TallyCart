from models import FoodItem
from interfaces import IOutputStrategy

class FoodCart:
    def __init__(self, output_strategy: IOutputStrategy):
        self._items = []
        self._discount = 0.0
        self._budget = 0.0
        self.output_strategy = output_strategy

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if value < 0: raise ValueError("Discount cannot be negative")
        self._discount = value
        self._render_totals()

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        if value < 0: raise ValueError("Budget cannot be negative")
        self._budget = value
        self._render_totals()

    def add_item(self, name, price, category, quantity):
        try:
            new_item = FoodItem(name, price, category, quantity)
            self._items.append(new_item)
            self._render_all()
        except ValueError as e:
            raise e

    def delete_item(self, index):
        if 0 <= index < len(self._items):
            self._items.pop(index)
            self._render_all()

    def get_total(self):
        return sum(item.price * item.quantity for item in self._items)

    def get_all_items(self):
        return list(self._items)

    def _calculate_grand_total(self):
        subtotal = self.get_total()
        total = subtotal - self._discount
        return max(0, total), subtotal

    def _render_all(self):
        self.output_strategy.clear_view()
        for item in self._items:
            self.output_strategy.display_item(str(item))
            self.output_strategy.log_message(item.get_notepad_format())
        self._render_totals()

    def _render_totals(self):
        total, subtotal = self._calculate_grand_total()
        balance = self._budget - total
        self.output_strategy.update_totals(subtotal, self._discount, total, self._budget, balance)

    def clear_for_new_transaction(self):
        self._items = []
        self._discount = 0.0
        self._render_all()