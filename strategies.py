import tkinter as tk
from interfaces import IOutputStrategy


class GuiOutputStrategy(IOutputStrategy):
    def __init__(self, listbox_widget, notepad_widget, subtotal_label, total_label, budget_label):
        self.listbox = listbox_widget
        self.notepad = notepad_widget
        self.lbl_subtotal = subtotal_label
        self.lbl_total = total_label
        self.lbl_budget = budget_label

    def clear_view(self):
        self.listbox.delete(0, "end")
        self.notepad.config(state="normal")
        self.notepad.delete(1.0, "end")
        self.notepad.config(state="disabled")

    def display_item(self, item_string):
        self.listbox.insert("end", item_string)

    def log_message(self, message):
        self.notepad.config(state="normal")
        self.notepad.insert("end", message + "\n")
        self.notepad.config(state="disabled")

    def update_totals(self, subtotal, discount, total, budget, balance):
        self.lbl_subtotal.config(text=f"SUBTOTAL: P{subtotal:.2f}")
        self.lbl_total.config(text=f"TOTAL: P{total:.2f}")

        if balance >= 0:
            self.lbl_budget.config(text=f"REMAINING BALANCE: P{balance:.2f}", fg="green")
        else:
            self.lbl_budget.config(text=f"OVER BUDGET: P{abs(balance):.2f}", fg="red")