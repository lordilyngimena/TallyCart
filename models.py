class FoodItem:
    """Represents a specific food item."""
    def __init__(self, name, price, category, quantity=1):
        self._name = name
        self._price = 0.0
        self._category = category
        self._quantity = 1
        self.price = price
        self.quantity = quantity

    @property
    def name(self): return self._name

    @property
    def price(self): return self._price

    @price.setter
    def price(self, value):
        if value < 0: raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def category(self): return self._category

    @property
    def quantity(self): return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0: raise ValueError("Quantity must be positive.")
        self._quantity = value

    def __str__(self):
        return f"[{self._category}] {self._name} x{int(self._quantity)} ({self._price:.2f})"

    def get_notepad_format(self):
        return f"{self._name}, {self._price}, {self._category}, {self._quantity}"