import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import datetime

GALLERY_FILE = "gallery.json"

def load_gallery():
    if not os.path.exists(GALLERY_FILE):
        return []

    try:
        with open(GALLERY_FILE, "r") as f:
            if os.path.getsize(GALLERY_FILE) == 0:
                return []

            return json.load(f)

    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error reading gallery file")
        return []

def save_gallery(gallery):
    with open(GALLERY_FILE, "w") as f:
        json.dump(gallery, f, indent=4)

class GalleryApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Art Gallery Manager")
        self.root.geometry("1000x650")

        title = tk.Label(
            root,
            text="Art Gallery Manager",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Artwork Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(input_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=10)

        tk.Label(input_frame, text="Artist").grid(row=0, column=2)
        self.artist_entry = tk.Entry(input_frame, width=25)
        self.artist_entry.grid(row=0, column=3, padx=10)

        tk.Label(input_frame, text="Created Year").grid(row=1, column=0)
        self.year_entry = tk.Entry(input_frame, width=25)
        self.year_entry.grid(row=1, column=1, padx=10)

        tk.Label(input_frame, text="Price").grid(row=1, column=2)
        self.price_entry = tk.Entry(input_frame, width=25)
        self.price_entry.grid(row=1, column=3, padx=10)

        tk.Label(input_frame, text="Status").grid(row=2, column=0)

        self.status_var = tk.StringVar()
        self.status_var.set("Available")

        status_menu = ttk.Combobox(
            input_frame,
            textvariable=self.status_var,
            values=["Available", "Sold"],
            state="readonly",
            width=22
        )
        status_menu.grid(row=2, column=1, pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Artwork",
            width=18,
            command=self.add_artwork
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Delete Artwork",
            width=18,
            command=self.delete_artwork
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Sell Artwork",
            width=18,
            command=self.sell_artwork
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Search Artwork",
            width=18,
            command=self.search_artwork
        ).grid(row=0, column=3, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Update Price",
            width=18,
            command=self.update_price
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Show Statistics",
            width=18,
            command=self.show_statistics
        ).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Refresh Gallery",
            width=18,
            command=self.display_artworks
        ).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Clear Inputs",
            width=18,
            command=self.clear_inputs
        ).grid(row=1, column=3, padx=5, pady=5)

        search_frame = tk.Frame(root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Title:").pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=10)

        columns = (
            "Title",
            "Artist",
            "Year",
            "Price",
            "Status",
            "Sold Date"
        )

        self.tree = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.display_artworks()

    def display_artworks(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        gallery = load_gallery()

        for art in gallery:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    art["Title"],
                    art["Artist"],
                    art["Created Year"],
                    art["Price"],
                    art["Sold Status"],
                    art["Sold Date"]
                )
            )

    def add_artwork(self):

        gallery = load_gallery()

        title = self.title_entry.get().strip()
        artist = self.artist_entry.get().strip()
        year = self.year_entry.get().strip()
        price = self.price_entry.get().strip()
        status = self.status_var.get()

        if not title or not artist or not year or not price:
            messagebox.showwarning("Warning", "Fill all fields")
            return

        try:
            year = int(year)
            price = float(price)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Year must be integer and price must be number"
            )
            return

        for art in gallery:
            if art["Title"].lower() == title.lower():
                messagebox.showwarning(
                    "Warning",
                    "Artwork already exists"
                )
                return

        sold_date = "Not Sold"

        if status == "Sold":
            sold_date = datetime.datetime.now().strftime("%d-%m-%Y")

        new_art = {
            "Title": title,
            "Artist": artist,
            "Created Year": year,
            "Price": price,
            "Sold Status": status,
            "Sold Date": sold_date
        }

        gallery.append(new_art)

        save_gallery(gallery)

        self.display_artworks()
        self.clear_inputs()

        messagebox.showinfo(
            "Success",
            "Artwork added successfully"
        )

    def delete_artwork(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select artwork first"
            )
            return

        values = self.tree.item(selected[0], "values")
        title = values[0]

        gallery = load_gallery()

        updated_gallery = []

        for art in gallery:
            if art["Title"] != title:
                updated_gallery.append(art)

        save_gallery(updated_gallery)

        self.display_artworks()

        messagebox.showinfo(
            "Deleted",
            "Artwork deleted successfully"
        )

    def sell_artwork(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select artwork first"
            )
            return

        values = self.tree.item(selected[0], "values")
        title = values[0]

        gallery = load_gallery()

        for art in gallery:
            if art["Title"] == title:

                if art["Sold Status"] == "Sold":
                    messagebox.showwarning(
                        "Warning",
                        "Artwork already sold"
                    )
                    return

                art["Sold Status"] = "Sold"
                art["Sold Date"] = datetime.datetime.now().strftime(
                    "%d-%m-%Y"
                )

        save_gallery(gallery)

        self.display_artworks()

        messagebox.showinfo(
            "Success",
            "Artwork marked as sold"
        )

    def search_artwork(self):

        search = self.search_entry.get().strip().lower()

        if not search:
            messagebox.showwarning(
                "Warning",
                "Enter title to search"
            )
            return

        gallery = load_gallery()

        for item in self.tree.get_children():
            self.tree.delete(item)

        found = False

        for art in gallery:
            if search in art["Title"].lower():

                found = True

                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        art["Title"],
                        art["Artist"],
                        art["Created Year"],
                        art["Price"],
                        art["Sold Status"],
                        art["Sold Date"]
                    )
                )

        if not found:
            messagebox.showinfo(
                "Result",
                "No artwork found"
            )

    def update_price(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select artwork first"
            )
            return

        values = self.tree.item(selected[0], "values")

        title = values[0]

        new_price = self.price_entry.get().strip()

        if not new_price:
            messagebox.showwarning(
                "Warning",
                "Enter new price in price field"
            )
            return
        try:
            new_price = float(new_price)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Price must be a number"
            )
            return

        gallery = load_gallery()

        for art in gallery:
            if art["Title"] == title:
                art["Price"] = new_price

        save_gallery(gallery)

        self.display_artworks()

        messagebox.showinfo(
            "Success",
            "Price updated"
        )

    def show_statistics(self):

        gallery = load_gallery()

        if not gallery:
            messagebox.showwarning(
                "Warning",
                "No artworks in gallery"
            )
            return

        total_artworks = len(gallery)

        sold_artworks = 0
        available_artworks = 0
        total_value = 0
        highest_price = 0

        for art in gallery:

            total_value += art["Price"]

            if art["Price"] > highest_price:
                highest_price = art["Price"]

            if art["Sold Status"] == "Sold":
                sold_artworks += 1
            else:
                available_artworks += 1

        stats = (
            f"Total artworks: {total_artworks}\n\n"
            f"Sold artworks: {sold_artworks}\n\n"
            f"Available artworks: {available_artworks}\n\n"
            f"Total gallery value: ${total_value}\n\n"
            f"Highest artwork price: ${highest_price}"
        )

        messagebox.showinfo(
            "Gallery Statistics",
            stats
        )

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.artist_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.status_var.set("Available")

root = tk.Tk()
app = GalleryApp(root)
root.mainloop()
