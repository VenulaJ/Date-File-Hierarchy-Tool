import customtkinter as ctk
import os
import shutil
from tkinter import filedialog

source_path = None
destination_path = None
source_size_bytes = 0

def browse_folder(title):
    folder = filedialog.askdirectory(title=title)
    return folder

def update_entry(entry, value):
    entry.delete(0, ctk.END)
    entry.insert(0, value)

def browse_source_folder():
    global source_path, source_path_entry, source_size_bytes, source_size_entry, space_status_button
    folder = browse_folder("Select Source Folder")
    if folder:
        source_path = folder
        update_entry(source_path_entry, source_path)
        source_size_bytes = get_directory_size(source_path)
        update_source_size_display()
        update_space_status()

def browse_destination_folder():
    global destination_path, destination_path_entry, available_space_entry, space_status_button
    folder = browse_folder("Select Destination Folder")
    if folder:
        destination_path = folder
        update_entry(destination_path_entry, destination_path)
        update_available_space()
        update_space_status()

def get_disk_space(path, get_free=True):
    try:
        total, used, free = shutil.disk_usage(path)
        return free if get_free else total
    except (FileNotFoundError, OSError) as e:
        print(f"Error accessing path {path}: {e}")
        return None

def get_disk_free_space(path):
    return get_disk_space(path, get_free=True)

def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size

def update_space_display(entry, space_bytes, label_text="Select Destination"):
    entry.configure(state="normal")
    entry.delete(0, ctk.END)
    if space_bytes is not None:
        space_gb = space_bytes / (1024**3)
        entry.insert(0, f"{space_gb:.2f} GB")
    else:
        entry.insert(0, "N/A")
    entry.configure(state="readonly")

def update_available_space():
    global destination_path, available_space_entry
    space = get_disk_free_space(destination_path)
    update_space_display(available_space_entry, space, "Select Destination")

def update_source_size_display():
    global source_size_bytes, source_size_entry
    update_space_display(source_size_entry, source_size_bytes, "Select Source")

def update_space_status():
    global source_size_bytes, destination_path, space_status_button
    space_status_button.configure(text="", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"]) # Reset
    if source_size_bytes > 0 and destination_path:
        free_space = get_disk_free_space(destination_path)
        if free_space is not None:
            if free_space >= source_size_bytes:
                space_status_button.configure(text="✓ Enough space", fg_color="green", text_color="white", hover_color="#386F38")
            else:
                space_status_button.configure(text="✗ Not enough space", fg_color="red", text_color="white", hover_color="#8B0000")
        else:
            space_status_button.configure(text="⚠️ Cannot check space", fg_color="orange", text_color="black", hover_color="#FFA500")
    else:
        space_status_button.configure(text="Waiting...", fg_color="#4A4A4A", text_color="white", hover_color="#636363") # Indicate waiting

def create_label_entry_pair(parent, label_text, entry_width=240, entry_state="normal"):
    label = ctk.CTkLabel(parent, text=label_text, font=('Arial', 14))
    label.pack(pady=5)
    entry = ctk.CTkEntry(parent, width=entry_width, state=entry_state)
    entry.pack(pady=5)
    return label, entry

def create_button(parent, text, command, width=180, height=28, pady=10):
    button = ctk.CTkButton(parent, text=text, width=width, height=height, command=command)
    button.pack(pady=pady)
    return button

def Main():
    global source_path_entry, destination_path_entry, available_space_entry, source_size_entry, space_status_button

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title('DTFT v1.0')

    # Wrapper frame for centering content
    container = ctk.CTkFrame(app)
    container.pack(expand=True, padx=20, pady=40)

    greetingLabel = ctk.CTkLabel(container, text="Let's get organized!", font=("Arial", 16))
    greetingLabel.pack(pady=10)

    available_space_label, available_space_entry = create_label_entry_pair(container, 'Available space in destination path', entry_state="readonly")
    available_space_entry.insert(0, "Select Destination")

    source_size_label, source_size_entry = create_label_entry_pair(container, 'Source Folder Size', entry_state="readonly")
    source_size_entry.insert(0, "Select Source")

    # New button-like label for space status
    space_status_button = ctk.CTkButton(container, text="Waiting...", state="disabled", width=240, height=28, corner_radius=5, border_spacing=3, fg_color="#4A4A4A", text_color="white", hover_color="#636363")
    space_status_button.pack(pady=5)

    create_button(container, 'Browse Source', browse_source_folder)

    source_path_entry = ctk.CTkEntry(container, width=240)
    source_path_entry.pack(pady=5)
    source_path_entry.bind("<KeyRelease>", lambda event: source_path_entry._entry.edit_modified())  # Tracks changes for undo

    create_button(container, 'Browse Destination', browse_destination_folder)

    destination_path_entry = ctk.CTkEntry(container, width=240)
    destination_path_entry.pack(pady=(5, 10))
    destination_path_entry.bind("<KeyRelease>", lambda event: destination_path_entry._entry.edit_modified())  # Tracks changes for undo
    destination_path_entry.bind("<FocusOut>", lambda event: update_available_space()) # Update when focus leaves the entry

    # Get the minimum size based on the container
    container.update()
    min_width = container.winfo_reqwidth()
    min_height = container.winfo_reqheight()

    # Set the minimum size of the application window
    app.minsize(min_width + 20, min_height + 20) # Add some padding
    app.geometry('400x' + str(container.winfo_reqheight() + 80)) # Set initial height based on content

    app.mainloop()

Main()
