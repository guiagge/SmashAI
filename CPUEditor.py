import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

GROUNDED_MOVES_DISPLAY = {
    "0": "Jab", "1": "F Tilt", "2": "Up Tilt", "3": "Down Tilt",
    "4": "F Smash", "5": "Up Smash", "6": "Down Smash",
    "7": "Neutral B", "8": "Side B", "9": "Up B", "10": "Down B",
    "11": "Grab"
}
AERIAL_MOVES_DISPLAY = {
    "11": "Zair", "13": "Nair", "14": "Fair", "15": "Bair", "16": "Uair", "17": "Dair",
    "18": "Neutral B (A)", "19": "Side B (A)", "20": "Up B (A)", "21": "Down B (A)"
}

INTERNAL_MOVES = {
    "Jab": "0", "F Tilt": "1", "Up Tilt": "2", "Down Tilt": "3",
    "F Smash": "4", "Up Smash": "5", "Down Smash": "6",
    "Neutral B": "7", "Side B": "8", "Up B": "9", "Down B": "10",
    "Grab": "11",
    "Zair": "11", "Nair": "13", "Fair": "14", "Bair": "15", "Uair": "16", "Dair": "17",
    "Neutral B (A)": "18", "Side B (A)": "19", "Up B (A)": "20", "Down B (A)": "21"
}
INDEX_BY_INTERNAL_MOVE = {v: k for k, v in INTERNAL_MOVES.items()}

SITUATIONS_GROUND = [
    "Quick Attack", "Spaced Attack", "Strong Attack",
    "Dashing Attack", "Ledge Trap (2 Frame)", "Out of Shield"
]
SITUATIONS_AIR = [
    "General Aerial", "Edgeguard (Offstage)", "Rising Aerial", "Falling Aerial"
]

SITUATIONS_MAP = {
    "Quick Attack": ["0x0e6589ec1d", "0x1017f26175"],
    "Spaced Attack": ["0x0e783efc79", "0x100bd4c205"],
    "Strong Attack": ["0x0e954838f0", "0x107d9c0ad8"],
    "Dashing Attack": ["0x0b6c751ced", "0x0dbef37b28"],
    "Ledge Trap (2 Frame)": ["0x0cd0d6fe27", "0x0ec1e27b1b"],
    "General Aerial": ["0x0c5948494e", "0x0e20d80444"],
    "Edgeguard (Offstage)": ["0x114c2cfe49", "0x133a9ca1c8"],
    "Out of Shield": ["0x13cf48b010", "0x15c081a826"],
    "Rising Aerial": ["0x1304a30de4", "0x1505818845"],
    "Falling Aerial": ["0x10403b7660", "0x129db93926"]
}

SITUATIONS_ORDER = [
    "Quick Attack", "Spaced Attack",
    "Strong Attack", "Dashing Attack",
    "Out of Shield", "Ledge Trap (2 Frame)",
    "Edgeguard (Offstage)", "General Aerial",
    "Rising Aerial", "Falling Aerial",
]

class SmashXMLManipulatorApp:
    def __init__(self, master):
        self.master = master
        master.title("CPU Editor")
        master.geometry("608x720")

        self.filepath = None
        self.xml_tree = None
        self.situations_data = {}

        self.GROUNDED_MOVES_DISPLAY = GROUNDED_MOVES_DISPLAY
        self.AERIAL_MOVES_DISPLAY = AERIAL_MOVES_DISPLAY
        self.INTERNAL_MOVES = INTERNAL_MOVES

        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        self.open_button = tk.Button(button_frame, text="Open XML", command=self.load_xml)
        self.open_button.grid(row=0, column=0, padx=30)

        self.save_button = tk.Button(button_frame, text="Save XML", command=self.save_xml, state=tk.DISABLED)
        self.save_button.grid(row=0, column=1, padx=70)

        self.content_frame = tk.Frame(self.master)
        self.content_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.content_frame)
        self.scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def get_golpes_validos_display(self, situation_name):
        if situation_name in SITUATIONS_GROUND:
            return sorted(self.GROUNDED_MOVES_DISPLAY.values())
        elif situation_name in SITUATIONS_AIR:
            return sorted(self.AERIAL_MOVES_DISPLAY.values())
        return sorted(self.INTERNAL_MOVES.keys())

    def get_golpe_index(self, golpe_display_name):
        return self.INTERNAL_MOVES.get(golpe_display_name)

    def get_internal_golpe_name(self, golpe_display_name):
        return self.INTERNAL_MOVES.get(golpe_display_name)

    def load_xml(self):
        self.filepath = filedialog.askopenfilename(
            defaultextension=".xml",
            filetypes=[("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
        )
        if self.filepath:
            try:
                self.xml_tree = ET.parse(self.filepath)
                self.root = self.xml_tree.getroot()
                self.populate_interface()
                self.save_button.config(state=tk.NORMAL)
            except ET.ParseError:
                messagebox.showerror("Error", "Error parsing XML file!")

    def populate_interface(self):
        # Cleans interface
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.situations_data = {}

        list_element = self.root.find('list')
        if list_element is not None:
            for i, situation_name in enumerate(SITUATIONS_ORDER):
                situation_hashes = SITUATIONS_MAP[situation_name]
                coluna = i % 2
                linha = i // 2

                situation_frame = tk.LabelFrame(self.scrollable_frame, text=situation_name)
                situation_frame.grid(row=linha, column=coluna, padx=10, pady=5, sticky="ew")
                situation_frame.columnconfigure(0, weight=1)
                self.situations_data[situation_name] = []
                golpes_na_situacao = {}

                golpes_validos_display = self.get_golpes_validos_display(situation_name)

                for index_attr_xml, golpe_nome_interno_xml in INDEX_BY_INTERNAL_MOVE.items():
                    golpe_display_name = None
                    if situation_name in SITUATIONS_GROUND and index_attr_xml in self.GROUNDED_MOVES_DISPLAY:
                        golpe_display_name = self.GROUNDED_MOVES_DISPLAY[index_attr_xml]
                    elif situation_name in SITUATIONS_AIR and index_attr_xml in self.AERIAL_MOVES_DISPLAY:
                        golpe_display_name = self.AERIAL_MOVES_DISPLAY[index_attr_xml]
                    elif index_attr_xml in self.GROUNDED_MOVES_DISPLAY:
                        golpe_display_name = self.GROUNDED_MOVES_DISPLAY[index_attr_xml]
                    elif index_attr_xml in self.AERIAL_MOVES_DISPLAY:
                        golpe_display_name = self.AERIAL_MOVES_DISPLAY[index_attr_xml]

                    if golpe_display_name in golpes_validos_display:
                        display_for_dropdown = golpe_display_name

                        for struct in list_element.findall(f'struct[@index="{index_attr_xml}"]'):
                            percentage = None
                            for situation_hash in situation_hashes:
                                percentage_element = struct.find(f'int[@hash="{situation_hash}"]')
                                if percentage_element is not None:
                                    percentage = int(percentage_element.text)
                                    break
                            if percentage is not None and percentage > 0:
                                self.add_golpe_to_situation_frame(situation_frame, situation_name, display_for_dropdown, str(percentage), golpe_nome_interno_xml)
                                golpes_na_situacao[display_for_dropdown] = True

                add_button = tk.Button(situation_frame, text="+ Adicionar", command=lambda s=situation_name, f=situation_frame: self.add_new_golpe(f, s))
                add_button.pack(pady=5, fill=tk.X, side=tk.BOTTOM)
    
    def add_golpe_to_situation_frame(self, situation_frame, situation_name, golpe_display_name, percentage, golpe_nome_interno=None):
        golpe_frame = tk.Frame(situation_frame)
        golpe_frame.pack(fill=tk.X, pady=2)

        golpe_var = tk.StringVar(value=golpe_display_name)
        percentage_var = tk.StringVar(value=percentage)
        internal_name = golpe_nome_interno if golpe_nome_interno else self.get_internal_golpe_name(golpe_display_name)

        golpe_data = {'golpe_var': golpe_var, 'percentage_var': percentage_var, 'golpe_interno': internal_name}
        golpe_frame.golpe_data = golpe_data
        self.situations_data[situation_name].append(golpe_data)

        golpes_validos_display = self.get_golpes_validos_display(situation_name)
        golpe_dropdown = ttk.Combobox(golpe_frame, textvariable=golpe_var, values=sorted(golpes_validos_display), state="readonly")
        golpe_dropdown.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        golpe_dropdown.bind('<<ComboboxSelected>>', lambda event, s=situation_name, g_var=golpe_var, p_var=percentage_var: self.update_percentage_on_golpe_change(s, g_var, p_var))

        percentage_entry = tk.Entry(golpe_frame, textvariable=percentage_var, width=5)
        percentage_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(golpe_frame, text="%").pack(side=tk.LEFT)

        delete_button = tk.Button(golpe_frame, text="X", width=3, command=lambda gf=golpe_frame, sn=situation_name, gd=golpe_data: self.delete_golpe(gf, sn, gd))
        delete_button.pack(side=tk.LEFT, padx=5)

    def update_percentage_on_golpe_change(self, situation_name, golpe_var, percentage_var):
        golpe_display_name = golpe_var.get()
        golpe_index = self.get_golpe_index(golpe_display_name)
        if self.xml_tree is not None and golpe_index is not None:
            list_element = self.root.find('list')
            if list_element is not None:
                situation_hashes = SITUATIONS_MAP[situation_name]
                for struct in list_element.findall(f'struct[@index="{golpe_index}"]'):
                    found_percentage = False
                    for situation_hash in situation_hashes:
                        percentage_element = struct.find(f'int[@hash="{situation_hash}"]')
                        if percentage_element is not None and int(percentage_element.text) > 0:
                            percentage_var.set(percentage_element.text)
                            found_percentage = True
                            break
                    if found_percentage:
                        return
        percentage_var.set("100")

    def add_new_golpe(self, situation_frame, situation_name):
        new_golpe_frame = tk.Frame(situation_frame)
        new_golpe_frame.pack(fill=tk.X, pady=2)

        golpes_validos_display = self.get_golpes_validos_display(situation_name)
        new_golpe_var = tk.StringVar(value=sorted(golpes_validos_display)[0] if golpes_validos_display else "")
        new_percentage_var = tk.StringVar(value="100")
        internal_new_golpe = self.get_internal_golpe_name(new_golpe_var.get())

        new_golpe_data = {'golpe_var': new_golpe_var, 'percentage_var': new_percentage_var, 'golpe_interno': internal_new_golpe}
        new_golpe_frame.golpe_data = new_golpe_data
        self.situations_data[situation_name].append(new_golpe_data)

        golpe_dropdown = ttk.Combobox(new_golpe_frame, textvariable=new_golpe_var, values=sorted(golpes_validos_display), state="readonly")
        golpe_dropdown.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        golpe_dropdown.bind('<<ComboboxSelected>>', lambda event, s=situation_name, g_var=new_golpe_var, p_var=new_percentage_var: self.update_percentage_on_golpe_change(s, g_var, p_var))

        percentage_entry = tk.Entry(new_golpe_frame, textvariable=new_percentage_var, width=5)
        percentage_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(new_golpe_frame, text="%").pack(side=tk.LEFT)
        delete_button = tk.Button(new_golpe_frame, text="X", width=3, command=lambda gf=new_golpe_frame, sn=situation_name, gd=new_golpe_data: self.delete_golpe(gf, sn, gd))
        delete_button.pack(side=tk.LEFT, padx=5)

    def delete_golpe(self, golpe_frame, situation_name, golpe_data):
        golpe_frame.destroy()
        try:
            self.situations_data[situation_name].remove(golpe_data)
        except ValueError:
            print(f"Erro ao remover golpe_data: {golpe_data} da situação: {situation_name}")

    def save_xml(self):
        if self.filepath and self.xml_tree:
            try:
                list_element = self.root.find('list')
                if list_element is not None:
                    # Resets all percentages
                    for struct in list_element.findall('struct'):
                        for int_element in struct.findall('int'):
                            int_element.text = "0"
                    # Updates the percentages according to the values in the GUI
                    for situation_name, golpes_data_list in self.situations_data.items():
                        situation_hashes = SITUATIONS_MAP[situation_name]
                        for golpe_info in golpes_data_list:
                            golpe_display_name = golpe_info['golpe_var'].get()
                            percentage = golpe_info['percentage_var'].get()
                            internal_golpe_name = golpe_info.get('golpe_interno')
                            golpe_index_interno = self.INTERNAL_MOVES.get(golpe_display_name)
                            if golpe_index_interno:
                                for struct in list_element.findall(f'struct[@index="{golpe_index_interno}"]'):
                                    for situation_hash in situation_hashes:
                                        percentage_element = struct.find(f'int[@hash="{situation_hash}"]')
                                        if percentage_element is not None:
                                            percentage_element.text = percentage
                                        else:
                                            new_percentage = ET.SubElement(struct, 'int', {'hash': situation_hash})
                                            new_percentage.text = percentage
                # Saves the changes to the file
                ET.indent(self.xml_tree, space="  ", level=0)
                self.xml_tree.write(self.filepath, encoding="utf-8", xml_declaration=True)
                messagebox.showinfo("Sucess", "XML file saved sucessfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Error saving XML file: {e}")
        else:
            messagebox.showerror("Error", "No XML file was loaded!?")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmashXMLManipulatorApp(root)
    root.mainloop()