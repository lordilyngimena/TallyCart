import tkinter as tk
from tkinter import messagebox, ttk
from cart_logic import FoodCart
from strategies import GuiOutputStrategy


class FoodAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TallyCart")

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        self.colors = {
            "bg_main": "#f4f9f4", "bg_card": "#ffffff",
            "primary": "#27ae60", "primary_dark": "#219150",
            "accent": "#e67e22", "danger": "#c0392b",
            "text_main": "#2c3e50", "header_bg": "#27ae60"
        }
        self.root.configure(bg=self.colors["bg_main"])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self._build_ui()

        output_strategy = GuiOutputStrategy(
            listbox_widget=self.listbox,
            notepad_widget=self.notepad_text,
            subtotal_label=self.lbl_subtotal,
            total_label=self.lbl_total,
            budget_label=self.lbl_budget_status
        )
        self.cart = FoodCart(output_strategy)

        self.categories = ["Fruit", "Vegetable", "Meat", "Dairy", "Pantry", "Beverage"]
        self.combo_category['values'] = self.categories
        self.combo_category.current(0)
        self.root.bind('<Return>', lambda event: self.add_item())

    def _build_ui(self):
        # HEADER
        header_frame = tk.Frame(self.root, bg=self.colors["header_bg"], height=80)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        tk.Label(header_frame, text="TallyCart", font=("Verdana", 20, "bold"),
                 bg=self.colors["header_bg"], fg="#ffffff").pack(pady=20)

        # INPUT SECTION
        input_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        input_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        input_frame = tk.Frame(input_container, bg=self.colors["bg_card"], bd=1, relief="solid")
        input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Row 1
        row1 = tk.Frame(input_frame, bg=self.colors["bg_card"])
        row1.pack(fill="x", padx=15, pady=(15, 10))
        tk.Label(row1, text="Category", bg=self.colors["bg_card"], fg=self.colors["primary"],
                 font=("Arial", 10, "bold")).pack(side="left")
        self.combo_category = ttk.Combobox(row1, state="readonly", width=10, font=("Arial", 10))
        self.combo_category.pack(side="left", padx=10)
        tk.Label(row1, text="Food Name", bg=self.colors["bg_card"], fg=self.colors["primary"],
                 font=("Arial", 10, "bold")).pack(side="left", padx=(10, 5))
        self.entry_name = tk.Entry(row1, font=("Arial", 11), relief="flat", bg="#f9f9f9", highlightthickness=1,
                                   highlightcolor=self.colors["primary"])
        self.entry_name.pack(side="left", fill="x", expand=True, padx=5)

        # Row 2
        row2 = tk.Frame(input_frame, bg=self.colors["bg_card"])
        row2.pack(fill="x", padx=15, pady=(0, 15))
        tk.Label(row2, text="Price", bg=self.colors["bg_card"], fg=self.colors["primary"],
                 font=("Arial", 10, "bold")).pack(side="left")
        self.entry_price = tk.Entry(row2, font=("Arial", 11), width=12, relief="flat", bg="#f9f9f9",
                                    highlightthickness=1, highlightcolor=self.colors["primary"])
        self.entry_price.pack(side="left", padx=10)

        tk.Label(row2, text="Qty", bg=self.colors["bg_card"], fg=self.colors["primary"],
                 font=("Arial", 10, "bold")).pack(side="left")
        self.entry_qty = tk.Entry(row2, font=("Arial", 11), width=8, relief="flat", bg="#f9f9f9", highlightthickness=1,
                                  highlightcolor=self.colors["primary"])
        self.entry_qty.insert(0, "1")
        self.entry_qty.pack(side="left", padx=5)

        btn_add = tk.Button(row2, text="Add", command=self.add_item, bg=self.colors["accent"], fg="white",
                            font=("Arial", 10, "bold"), relief="flat", padx=20, pady=5, cursor="hand2", bd=0)
        btn_add.pack(side="right")

        # CONTENT AREA
        content_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        content_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_columnconfigure(1, weight=1)
        content_container.grid_rowconfigure(0, weight=1)

        # Left: List
        left_card = tk.Frame(content_container, bg=self.colors["bg_card"], bd=1, relief="solid")
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        tk.Label(left_card, text="Your Basket", bg=self.colors["bg_card"], fg=self.colors["text_main"],
                 font=("Verdana", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.listbox = tk.Listbox(left_card, font=("Courier New", 10), bg="#fafafa", fg=self.colors["text_main"], bd=0,
                                  highlightthickness=0)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Right: Notepad
        right_card = tk.Frame(content_container, bg="#fffdf0", bd=1, relief="solid")
        right_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        tk.Label(right_card, text="Receipt Log", bg="#fffdf0", fg=self.colors["text_main"],
                 font=("Verdana", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.notepad_text = tk.Text(right_card, height=10, width=20, bg="#fffdf0", font=("Courier New", 10),
                                    state="disabled", bd=0, relief="flat")
        self.notepad_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # BOTTOM AREA
        bottom_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        bottom_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))

        totals_frame = tk.Frame(bottom_frame, bg=self.colors["bg_main"])
        totals_frame.pack(side="left", padx=10)

        self.lbl_subtotal = tk.Label(totals_frame, text="SUBTOTAL: P0.00", font=("Arial", 12),
                                     bg=self.colors["bg_main"], fg="#7f8c8d")
        self.lbl_subtotal.pack(anchor="w")

        disc_row = tk.Frame(totals_frame, bg=self.colors["bg_main"])
        disc_row.pack(fill="x", pady=2)
        tk.Label(disc_row, text="DISCOUNT:", font=("Arial", 10, "bold"), bg=self.colors["bg_main"],
                 fg=self.colors["text_main"]).pack(side="left")
        self.discount_var = tk.DoubleVar(value=0.0)
        self.entry_discount = tk.Entry(disc_row, textvariable=self.discount_var, width=12, font=("Arial", 10),
                                       justify="right", relief="solid", bd=1)
        self.entry_discount.pack(side="right")
        self.entry_discount.bind("<KeyRelease>", self.on_discount_change)

        # Budget Input
        budget_row = tk.Frame(totals_frame, bg=self.colors["bg_main"])
        budget_row.pack(fill="x", pady=2)
        tk.Label(budget_row, text="BUDGET:", font=("Arial", 10, "bold"), bg=self.colors["bg_main"],
                 fg=self.colors["text_main"]).pack(side="left")
        self.budget_var = tk.DoubleVar(value=0.0)
        self.entry_budget = tk.Entry(budget_row, textvariable=self.budget_var, width=12, font=("Arial", 10),
                                     justify="right", relief="solid", bd=1)
        self.entry_budget.pack(side="right")
        self.entry_budget.bind("<KeyRelease>", self.on_budget_change)

        self.lbl_total = tk.Label(totals_frame, text="TOTAL: P0.00", font=("Verdana", 20, "bold"),
                                  bg=self.colors["bg_main"], fg=self.colors["primary"])
        self.lbl_total.pack(anchor="w")

        self.lbl_budget_status = tk.Label(totals_frame, text="REMAINING BALANCE: P0.00", font=("Verdana", 12, "bold"),
                                          bg=self.colors["bg_main"], fg="blue")
        self.lbl_budget_status.pack(anchor="w", pady=(5, 0))

        # Buttons
        btn_container = tk.Frame(bottom_frame, bg=self.colors["bg_main"])
        btn_container.pack(side="right", padx=10)

        btn_del = tk.Button(btn_container, text="Delete Selected", command=self.delete_selected_item,
                            bg=self.colors["danger"], fg="white",
                            font=("Arial", 10, "bold"), relief="flat", padx=15, pady=8, cursor="hand2", bd=0)
        btn_del.pack(side="right", padx=5)

        btn_sum = tk.Button(btn_container, text="Checkout Summary", command=self.show_summary,
                            bg=self.colors["primary"], fg="white",
                            font=("Arial", 10, "bold"), relief="flat", padx=20, pady=8, cursor="hand2", bd=0)
        btn_sum.pack(side="right", padx=5)

    # --- LOGIC HANDLERS ---

    def add_item(self):
        name = self.entry_name.get().strip()
        price_str = self.entry_price.get().strip()
        qty_str = self.entry_qty.get().strip()
        category = self.combo_category.get()

        if not name or not price_str:
            messagebox.showwarning("Missing Info", "Please enter Food Name and Price.")
            return

        try:
            price = float(price_str)
            if price < 0: raise ValueError
            qty = float(qty_str) if qty_str else 1
            if qty <= 0: raise ValueError

            self.cart.add_item(name, price, category, qty)

            self.entry_name.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
            self.entry_qty.insert(0, "1")
            self.entry_name.focus()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def delete_selected_item(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select an item to delete.")
            return
        index = selection[0]
        self.cart.delete_item(index)

    def on_discount_change(self, event=None):
        try:
            val = float(self.discount_var.get())
            if val < 0: raise ValueError
            self.cart.discount = val
        except ValueError:
            pass

    def on_budget_change(self, event=None):
        try:
            val = float(self.budget_var.get())
            if val < 0: raise ValueError
            self.cart.budget = val
        except ValueError:
            pass

    def show_summary(self):
        items = self.cart.get_all_items()
        if not items:
            messagebox.showwarning("Empty", "Basket is empty.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Receipt")
        popup.geometry("400x500")
        popup.configure(bg=self.colors["bg_main"])

        tk.Frame(popup, bg=self.colors["primary"], height=60).pack(fill="x")
        tk.Label(popup, text="RECEIPT", font=("Verdana", 14, "bold"), bg=self.colors["primary"], fg="white").place(
            relx=0.5, rely=0.5, anchor="center")

        content = tk.Frame(popup, bg=self.colors["bg_main"])
        content.pack(fill="both", expand=True, padx=20, pady=20)

        receipt_card = tk.Frame(content, bg="#ffffff", bd=1, relief="solid")
        receipt_card.pack(fill="both", expand=True)

        inner = tk.Frame(receipt_card, bg="#ffffff", padx=15, pady=15)
        inner.pack(fill="both", expand=True)

        # List Items
        for item in items:
            row = tk.Frame(inner, bg="#ffffff")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{item.name} x{int(item.quantity)}", bg="#ffffff", anchor="w").pack(side="left")
            tk.Label(row, text=f"P{item.price * item.quantity:.2f}", bg="#ffffff", anchor="e").pack(side="right")

        ttk.Separator(inner, orient='horizontal').pack(fill='x', pady=10)

        # Calculations
        subtotal = self.cart.get_total()
        discount = self.cart.discount
        total = subtotal - discount
        budget = self.cart.budget
        balance = budget - total

        # Helper for aligned rows
        def add_row(label, value, font=("Arial", 10), fg="black", pady=0):
            r = tk.Frame(inner, bg="#ffffff")
            r.pack(fill="x", pady=pady)
            tk.Label(r, text=label, bg="#ffffff", font=("Arial", 10)).pack(side="left")
            tk.Label(r, text=value, bg="#ffffff", font=font, fg=fg).pack(side="right")

        # Summary Rows
        add_row("SUBTOTAL:", f"P{subtotal:.2f}", font=("Arial", 10, "bold"))

        disc_str = f"-P{discount:.2f}" if discount > 0 else f"P{discount:.2f}"
        add_row("DISCOUNT:", disc_str, fg=self.colors["danger"], pady=5)

        ttk.Separator(inner, orient='horizontal').pack(fill='x', pady=10)

        add_row("TOTAL:", f"P{total:.2f}", font=("Verdana", 14, "bold"), fg=self.colors["primary"])

        ttk.Separator(inner, orient='horizontal').pack(fill='x', pady=10)

        add_row("BUDGET:", f"P{budget:.2f}")

        bal_color = self.colors["primary"] if balance >= 0 else self.colors["danger"]
        bal_text = f"P{balance:.2f}" if balance >= 0 else f"-P{abs(balance):.2f}"
        add_row("BALANCE:", bal_text, font=("Arial", 12, "bold"), fg=bal_color, pady=5)

        # Close and Clear Logic
        def close_and_clear():
            self.cart.clear_for_new_transaction()
            self.discount_var.set(0.0)
            popup.destroy()

        tk.Button(popup, text="Close", command=close_and_clear, bg="#95a5a6", fg="white", relief="flat").pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FoodAppGUI(root)
    root.mainloop()