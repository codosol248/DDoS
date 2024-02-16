import os
import time
import random
import socket
import threading
import argparse
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Tkinter GUI for user input
class DDoSGUI:
    def __init__(self, master):
        self.master = master
        master.title("DDoS Tool made by codosol248")
        master.geometry("450x250")

        self.icon_path = "ddos_icon.ico"  # Update the path if necessary
        icon_image = Image.open(self.icon_path)
        self.icon = ImageTk.PhotoImage(icon_image)
        master.iconphoto(True, self.icon)

        self.attack_type_label = ttk.Label(master, text="Select Attack Type:")
        self.attack_type_combobox = ttk.Combobox(master, values=["dos", "ddos"], state="readonly")
        self.attack_type_combobox.set("dos")
        self.attack_type_combobox.bind("<<ComboboxSelected>>", self.update_ip_entry_visibility)

        self.target_label = ttk.Label(master, text="Enter IP or Domain:")
        self.target_entry = ttk.Entry(master)

        self.port_label = ttk.Label(master, text="Enter Target Port:")
        self.port_entry = ttk.Entry(master)

        self.duration_label = ttk.Label(master, text="Enter Attack Duration (seconds):")
        self.duration_entry = ttk.Entry(master)

        self.ip_list_label = ttk.Label(master, text="Enter IP addresses for DDoS:")

        self.ip_entries_frame = ttk.Frame(master)
        self.ip_entries_frame.grid_columnconfigure(1, weight=1)

        self.ip_entries = []  # List to store IP entry widgets
        self.ip_entry_labels = []  # List to store IP entry labels
        self.ip_entry_count = 0  # Counter for tracking IP entries

        self.launch_button = ttk.Button(master, text="Launch Attack", command=self.launch_attack)
        self.add_ip_button = ttk.Button(master, text="Add IP", command=self.add_ip_entry)
        self.remove_ip_button = ttk.Button(master, text="Remove IP", command=self.remove_ip_entry)

        # Arrange widgets using grid
        self.attack_type_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.attack_type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.target_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.target_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.port_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.port_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.duration_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.ip_list_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.ip_entries_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.launch_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.add_ip_button.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.remove_ip_button.grid(row=7, column=1, padx=5, pady=5, sticky="e")

        # Initially hide IP addresses section and buttons
        self.hide_ip_entries()
        self.hide_ip_buttons()

    def update_ip_entry_visibility(self, event):
        selected_attack_type = self.attack_type_combobox.get()
        if selected_attack_type == 'ddos':
            self.show_ip_entries()
            self.show_ip_buttons()
            # Automatically add the first IP entry box when ddos is selected
            self.add_ip_entry()
        else:
            self.hide_ip_entries()
            self.hide_ip_buttons()

    def add_ip_entry(self):
        ip_entry_label = ttk.Label(self.ip_entries_frame, text=f"Added IP {self.ip_entry_count + 1}:")
        ip_entry_label.grid(row=self.ip_entry_count, column=0, padx=5, pady=2, sticky="w")

        ip_entry = ttk.Entry(self.ip_entries_frame)
        ip_entry.grid(row=self.ip_entry_count, column=1, padx=5, pady=2, sticky="we")

        self.ip_entry_labels.append(ip_entry_label)
        self.ip_entries.append(ip_entry)
        self.ip_entry_count += 1

        # Expand window vertically when adding IP entries
        self.master.geometry(f"{self.master.winfo_width()}x{self.master.winfo_height() + 30}")

    def remove_ip_entry(self):
        if self.ip_entries:
            entry_to_remove = self.ip_entries.pop()
            label_to_remove = self.ip_entry_labels.pop()
            entry_to_remove.destroy()
            label_to_remove.destroy()

            self.ip_entry_count -= 1

            # Shrink window vertically when removing IP entries
            self.master.geometry(f"{self.master.winfo_width()}x{self.master.winfo_height() - 30}")

    def show_ip_entries(self):
        self.ip_list_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.ip_entries_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    def hide_ip_entries(self):
        self.ip_list_label.grid_forget()
        self.ip_entries_frame.grid_forget()

    def show_ip_buttons(self):
        self.add_ip_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.remove_ip_button.grid(row=6, column=1, padx=5, pady=5, sticky="e")

    def hide_ip_buttons(self):
        self.add_ip_button.grid_forget()
        self.remove_ip_button.grid_forget()

    def launch_attack(self):
        # Retrieve user input
        attack_type = self.attack_type_combobox.get()
        target = self.target_entry.get()
        port = int(self.port_entry.get())
        duration = int(self.duration_entry.get())

        # Perform the attack
        if attack_type == 'dos':
            dos(target, port, duration)
        elif attack_type == 'ddos':
            ip_list = [ip_entry.get() for ip_entry in self.ip_entries]
            ddos(ip_list, port, duration)

if __name__ == '__main__':
    root = tk.Tk()
    app = DDoSGUI(root)
    root.mainloop()
