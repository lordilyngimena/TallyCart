from abc import ABC, abstractmethod

class IOutputStrategy(ABC):
    @abstractmethod
    def clear_view(self): pass

    @abstractmethod
    def display_item(self, item_string): pass

    @abstractmethod
    def log_message(self, message): pass

    @abstractmethod
    def update_totals(self, subtotal, discount, total, budget, balance): pass