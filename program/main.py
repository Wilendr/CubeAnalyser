import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from card_utilities import fetch_cards
from deck_utilities import make_cube_list, extract_decklists
from analysis_utilities import *
from visuals import *
from deck_images import *
import os
import json

SETTINGS_FILE = "program/settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings():
    settings = {
        "deck_folder": deck_folder_var.get(),
        "cube_file": cube_file_var.get(),
        "save_folder": save_folder_var.get(),
        "update": update_var.get(),
        "images": images_var.get(),
        "date": date_var.get(),
        "filter": filter_var.get(),
        "window": window_var.get()
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def run_analysis():
    deck_folder = deck_folder_var.get()
    cube_file = cube_file_var.get()
    save_folder = save_folder_var.get()
    update = update_var.get()
    images = images_var.get()
    date_analysis = date_var.get()
    card_filter = int(filter_var.get())
    window = int(window_var.get())

    if not deck_folder:
        messagebox.showerror("Error", "You must select a deck folder.")
        return
    if not save_folder:
        messagebox.showerror("Error", "You must select a location to save the results.")
        return

    os.makedirs(save_folder, exist_ok=True)
    save_settings()  # <-- LAGRE innstillinger

    status_var.set("Analysis in progress...")
    root.update()

    magic_cards = fetch_cards(update)

    if cube_file:
        cube_list = make_cube_list(cube_file, magic_cards, update)
    else:
        cube_list = []

    deck_dict = extract_decklists(deck_folder, magic_cards, cube_list, date_analysis, update)

    archetype_dict = export_archetype_analysis(deck_dict, save_folder)
    export_card_analysis(deck_dict, cube_list, magic_cards, card_filter, archetype_dict, save_folder)
    export_color_analysis(deck_dict, magic_cards, save_folder)
    export_player_analysis(deck_dict, save_folder)

    if date_analysis:
        archetypes, timecourse = export_timecourse_analysis(deck_dict, window)
        plot_timecourse(archetypes, timecourse, window, save_folder)

    color_curve = export_color_curve(deck_dict)
    plot_color_curve(color_curve, save_folder)
    plot_archetype_analysis(save_folder)
    plot_card_win_analysis(save_folder)
    plot_card_main_analysis(save_folder)
    plot_card_norm_analysis(save_folder)
    plot_color_analysis(save_folder)
    plot_player_analysis(save_folder)

    if images:
        make_deck_images(deck_folder, deck_dict, magic_cards, save_folder)

    status_var.set("Analysis complete!")

def view_analysis_images():
    folder = save_folder_var.get()
    if not folder or not os.path.exists(folder):
        messagebox.showerror("Error", "Please select a valid output folder first.")
        return

    image_files = [
        f for f in os.listdir(folder)
        if f.endswith(".png") and "deck_images" not in f.lower()
    ]
    if not image_files:
        messagebox.showinfo("No Images", "No analysis images found in the selected folder.")
        return

    # Start ny visnings-vindu
    viewer = tk.Toplevel(root)
    viewer.title("View Analyses")
    viewer.geometry("800x600")

    img_label = tk.Label(viewer)
    img_label.pack()

    index = [0]  # mutable for closure

    def show_image():
        img_path = os.path.join(folder, image_files[index[0]])
        pil_img = Image.open(img_path)

        # Skaler proporsjonalt til maks 750 bredde / 550 høyde
        max_width, max_height = 750, 550
        w, h = pil_img.size
        scale = min(max_width / w, max_height / h, 1)  # ikke forstørr
        new_size = (int(w * scale), int(h * scale))
        pil_img = pil_img.resize(new_size, Image.ANTIALIAS)

        img = ImageTk.PhotoImage(pil_img)
        img_label.config(image=img)
        img_label.image = img
        viewer.title(f"Analysis {index[0]+1} of {len(image_files)}: {image_files[index[0]]}")

    def neste():
        if index[0] < len(image_files) - 1:
            index[0] += 1
            show_image()

    def forrige():
        if index[0] > 0:
            index[0] -= 1
            show_image()

    btn_frame = tk.Frame(viewer)
    btn_frame.pack(side='bottom', fill='x', pady=10)

    tk.Button(btn_frame, text="Previous", command=forrige).pack(side='left', padx=20)
    tk.Button(btn_frame, text="Next", command=neste).pack(side='right', padx=20)
    show_image()


def open_readme_window():
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'program/README_gui.txt'))
    if not os.path.exists(readme_path):
        messagebox.showerror("Error", "README_gui.txt not found.")
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    win = tk.Toplevel(root)
    win.title("README - CubeAnalyser")
    win.geometry("500x600")

    # Bruk Frame + grid for bedre layout
    frame = tk.Frame(win)
    frame.pack(expand=True, fill='both')

    text_box = tk.Text(frame, wrap='word', font=("Helvetica", 14))
    text_box.insert('1.0', content)
    text_box.config(state='disabled')
    text_box.grid(row=0, column=0, sticky='nsew')

    scrollbar = tk.Scrollbar(frame, command=text_box.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    text_box.config(yscrollcommand=scrollbar.set)

    # Sørg for at innholdet strekker seg med vinduet
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)


def on_close():
    save_settings()
    root.destroy()
    root.quit()

# ---------------- GUI Start ----------------
root = tk.Tk()
root.title("Magic Cube Analysis")

settings = load_settings()

# Variabler
deck_folder_var = tk.StringVar(value=settings.get("deck_folder", ""))
cube_file_var = tk.StringVar(value=settings.get("cube_file", ""))
save_folder_var = tk.StringVar(value=settings.get("save_folder", ""))
update_var = tk.BooleanVar(value=settings.get("update", False))
images_var = tk.BooleanVar(value=settings.get("images", False))
date_var = tk.BooleanVar(value=settings.get("date", False))
filter_var = tk.StringVar(value=settings.get("filter", "0"))
window_var = tk.StringVar(value=settings.get("window", "100"))

# Deck-mappe
tk.Label(root, text="Select deck folder:").grid(row=0, column=0, sticky='w')
tk.Entry(root, textvariable=deck_folder_var, width=30).grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: deck_folder_var.set(filedialog.askdirectory())).grid(row=0, column=2)

# Cube-liste
tk.Label(root, text="Select cube list:").grid(row=1, column=0, sticky='w')
tk.Entry(root, textvariable=cube_file_var, width=30).grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: cube_file_var.set(filedialog.askopenfilename())).grid(row=1, column=2)

# Lagringsmappe
tk.Label(root, text="Select output folder:").grid(row=2, column=0, sticky='w')
tk.Entry(root, textvariable=save_folder_var, width=30).grid(row=2, column=1)
tk.Button(root, text="Browse", command=lambda: save_folder_var.set(filedialog.askdirectory())).grid(row=2, column=2)

# Valg
tk.Checkbutton(root, text="Update card data (Scryfall)", variable=update_var).grid(row=3, column=0, columnspan=2, sticky='w')
tk.Checkbutton(root, text="Generate deck images", variable=images_var).grid(row=4, column=0, columnspan=2, sticky='w')
tk.Checkbutton(root, text="Time trend analysis", variable=date_var).grid(row=5, column=0, columnspan=2, sticky='w')

# Filter og window
tk.Label(root, text="Filter value:").grid(row=6, column=0, sticky='w')
tk.Entry(root, textvariable=filter_var, width=5).grid(row=6, column=1, sticky='w')

tk.Label(root, text="Window (time trend):").grid(row=7, column=0, sticky='w')
tk.Entry(root, textvariable=window_var, width=5).grid(row=7, column=1, sticky='w')

# Start-knapp
tk.Button(root, text="Start Analysis", command=run_analysis).grid(row=9, column=0, columnspan=3, pady=10)

# Statuslabel
status_var = tk.StringVar()
tk.Label(root, textvariable=status_var, fg='green').grid(row=8, column=0, columnspan=3)

tk.Button(root, text="View Analysis Images", command=view_analysis_images).grid(row=10, column=0, columnspan=3, pady=5)

tk.Button(root, text="View README", command=open_readme_window).grid(row=11, column=0, columnspan=3, pady=5)

# Lukkehandling
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
