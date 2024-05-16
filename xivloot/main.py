import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from loot_manager import load_data, save_data, add_boss, remove_boss, lock_player, unlock_player

class LootApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loot Distribution System")
        self.data = load_data()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.home_tab = ttk.Frame(self.notebook)
        self.edit_tab = ttk.Frame(self.notebook)
        self.loot_management_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.home_tab, text='Home')
        self.notebook.add(self.edit_tab, text='Edit')
        self.notebook.add(self.loot_management_tab, text='Loot Management')
        
        self.setup_home_gui()
        self.setup_edit_gui()
        self.setup_loot_management_gui()

        self.player_checkboxes = {}  # Initialize the player_checkboxes dictionary

    def setup_home_gui(self):
        tk.Label(self.home_tab, text="Select Boss:").grid(row=0, column=0)
        self.home_boss_combobox = ttk.Combobox(self.home_tab, values=self.data['bosses'])
        self.home_boss_combobox.grid(row=0, column=1)
        self.home_boss_combobox.bind("<<ComboboxSelected>>", self.update_player_lists)

        self.locked_listbox = tk.Listbox(self.home_tab)
        self.locked_listbox.grid(row=3, column=1, padx=10, pady=10)
        tk.Label(self.home_tab, text="Locked Players:").grid(row=2, column=1, padx=10, pady=10)

        self.unlocked_listbox = tk.Listbox(self.home_tab)
        self.unlocked_listbox.grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self.home_tab, text="Unlocked Players:").grid(row=2, column=0, padx=10, pady=10)

    def setup_edit_gui(self):
        # Boss management section
        tk.Label(self.edit_tab, text="Boss Management:").grid(row=0, column=0, columnspan=2)
        self.edit_boss_combobox = ttk.Combobox(self.edit_tab, values=self.data['bosses'])
        self.edit_boss_combobox.grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.edit_tab, text="Add Boss", command=self.add_boss_gui).grid(row=1, column=1)
        tk.Button(self.edit_tab, text="Remove Boss", command=self.remove_boss_gui).grid(row=1, column=2)

        # Player name editing section
        tk.Label(self.edit_tab, text="Edit Player Names:").grid(row=2, column=0, columnspan=2)
        self.player_name_entries = {}
        row = 3
        player_number = 1
        for player in self.data['players']:
            tk.Label(self.edit_tab, text=str(player_number)).grid(row=row, column=0)
            new_name_var = tk.StringVar(value=player['name'])
            entry = tk.Entry(self.edit_tab, textvariable=new_name_var)
            entry.grid(row=row, column=1)
            self.player_name_entries[player['name']] = new_name_var
            row += 1
            player_number += 1
        tk.Button(self.edit_tab, text="Update Names", command=self.update_player_names).grid(row=row, column=0, columnspan=2)

    def setup_loot_management_gui(self):
        tk.Label(self.loot_management_tab, text="Select Boss:").grid(row=0, column=0)
        self.loot_boss_combobox = ttk.Combobox(self.loot_management_tab, values=self.data['bosses'])
        self.loot_boss_combobox.grid(row=1, column=0)
        self.loot_boss_combobox.bind("<<ComboboxSelected>>", self.update_unlocked_players_checkboxes)

        self.players_frame = tk.Frame(self.loot_management_tab)
        self.players_frame.grid(row=2, column=0, columnspan=2)

        self.lockout_button = tk.Button(self.loot_management_tab, text="Lockout Selected", command=self.perform_lockout)
        self.lockout_button.grid(row=1, column=2, columnspan=2)

        self.victory_count = 0
        self.victory_label = tk.Label(self.loot_management_tab, text=f"Victories: {self.victory_count}")
        self.victory_label.grid(row=3, column=0)
        self.victory_button = tk.Button(self.loot_management_tab, text="Victory", command=self.increment_victory)
        self.victory_button.grid(row=3, column=1)
        self.reset_victories_button = tk.Button(self.loot_management_tab, text="Reset Victories", command=self.reset_victories)
        self.reset_victories_button.grid(row=3, column=2)

    def update_unlocked_players_checkboxes(self, event):
        selected_boss = self.loot_boss_combobox.get()
        for widget in self.players_frame.winfo_children():
            widget.destroy()
        row = 0
        for player in self.data['players']:
            if not player['locked'].get(selected_boss, False):
                var = tk.BooleanVar()
                chk = tk.Checkbutton(self.players_frame, text=player['name'], variable=var)
                chk.grid(row=row, column=0, sticky='w')
                self.player_checkboxes[player['name']] = var
                row += 1

    def perform_lockout(self):
        selected_boss = self.loot_boss_combobox.get()
        for player_name, var in self.player_checkboxes.items():
            if var.get():
                lock_player(self.data, player_name, selected_boss)
        save_data(self.data)
        self.update_unlocked_players_checkboxes(None)

    def increment_victory(self):
        self.victory_count += 1
        self.victory_label.config(text=f"Victories: {self.victory_count}")
        if self.victory_count >= 2:
            selected_boss = self.loot_boss_combobox.get()
            for player in self.data['players']:
                if player['locked'].get(selected_boss, False):
                    unlock_player(self.data, player['name'], selected_boss)
            save_data(self.data)
            self.update_unlocked_players_checkboxes(None)
            self.victory_count = 0

    def reset_victories(self):
        selected_boss = self.loot_boss_combobox.get()
        for player in self.data['players']:
            player['victories'][selected_boss] = 0
        save_data(self.data)
        messagebox.showinfo("Reset Successful", f"All victories for '{selected_boss}' have been reset.")
        self.victory_count = 0
        self.victory_label.config(text=f"Victories: {self.victory_count}")

    def setup_edit_gui(self):
        # Boss management section
        tk.Label(self.edit_tab, text="Boss Management:").grid(row=0, column=0, columnspan=2)
        self.edit_boss_combobox = ttk.Combobox(self.edit_tab, values=self.data['bosses'])
        self.edit_boss_combobox.grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.edit_tab, text="Add Boss", command=self.add_boss_gui).grid(row=1, column=1)
        tk.Button(self.edit_tab, text="Remove Boss", command=self.remove_boss_gui).grid(row=1, column=2)

        # Player name editing section
        tk.Label(self.edit_tab, text="Edit Player Names:").grid(row=2, column=0, columnspan=2)
        self.player_name_entries = {}
        row = 3
        player_number = 1
        for player in self.data['players']:
            tk.Label(self.edit_tab, text=str(player_number)).grid(row=row, column=0)
            new_name_var = tk.StringVar(value=player['name'])
            entry = tk.Entry(self.edit_tab, textvariable=new_name_var)
            entry.grid(row=row, column=1)
            self.player_name_entries[player['name']] = new_name_var
            row += 1
            player_number += 1
        tk.Button(self.edit_tab, text="Update Names", command=self.update_player_names).grid(row=row, column=0, columnspan=2)

    def add_boss_gui(self):
        boss_name = simpledialog.askstring("Add Boss", "Enter the name of the new boss:")
        if boss_name:
            add_boss(self.data, boss_name)
            self.refresh_boss_comboboxes()
            messagebox.showinfo("Boss Added", f"Boss '{boss_name}' added successfully.")
        else:
            messagebox.showerror("Error", "No boss name provided.")

    def remove_boss_gui(self):
        boss_name = self.edit_boss_combobox.get()
        if boss_name and messagebox.askyesno("Remove Boss", f"Are you sure you want to remove '{boss_name}'?"):
            remove_boss(self.data, boss_name)
            self.refresh_boss_comboboxes()
            messagebox.showinfo("Boss Removed", f"Boss '{boss_name}' removed successfully.")
        elif not boss_name:
            messagebox.showerror("Error", "No boss selected.")

    def refresh_boss_comboboxes(self):
        boss_list = self.data['bosses']
        self.home_boss_combobox['values'] = boss_list
        self.edit_boss_combobox['values'] = boss_list

    def update_player_lists(self, event):
        selected_boss = self.home_boss_combobox.get()
        self.locked_listbox.delete(0, tk.END)
        self.unlocked_listbox.delete(0, tk.END)
        for player in self.data['players']:
            if player['locked'].get(selected_boss, False):
                self.locked_listbox.insert(tk.END, player['name'])
            else:
                self.unlocked_listbox.insert(tk.END, player['name'])

    def update_player_names(self):
        for original_name, new_name_var in self.player_name_entries.items():
            new_name = new_name_var.get()
            for player in self.data['players']:
                if player['name'] == original_name:
                    player['name'] = new_name
        save_data(self.data)
        messagebox.showinfo("Update Successful", "Player names updated successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LootApp(root)
    root.mainloop()