from config import *


class DisplayTable(ttk.Labelframe):
    def __init__(self,master , layout=False , pack=True):
        super().__init__(master=master)
        if layout is False: return
        self.layout = layout
        self.sheet = Sheet(self,headers=self.layout["headrs"],show_column_index=False,)
        self.sheet.set_column_widths(column_widths=self.layout["col_size"])
        binding = ("single_select", "row_select",
                   "column_width_resize", "double_click_column_resize", "row_width_resize", "column_height_resize",
                   "row_height_resize", "double_click_row_resize")
        self.sheet.enable_bindings(binding)
        self.sheet.popup_menu_add_command("Save sheet", func=lambda : sheet_to_csv(self.sheet))
        self.sheet.pack(fill="both", expand=True, padx=4, pady=4)
        if pack is True:
            self.pack(fill="both", expand=True, padx=4, pady=4)
        self.sheet.bind("<ButtonPress-1>", self.left_click_sheet)
        self.selected_row = self.selected_row_no= None
    ###############        ###############        ###############        ###############
    def update(self,data):
        data = [list(ls) for ls in data]
        self.sheet.set_sheet_data(data,False)
    ###############        ###############        ###############        ###############
    def left_click_sheet(self,event):
            try:
                row_no = self.sheet.identify_row(event, exclude_index = False, allow_end = True)
                row = self.sheet.get_row_data(row_no)
                self.selected_row_no = row_no
                self.selected_row = row
            except: 
                self.selected_row = self.selected_row_no= None
##############################################################################################################

def sheet_to_csv(sheet:Sheet):
    filepath = asksaveasfilename(
            title="Save sheet as",
            filetypes=[("CSV File", ".csv")],
            defaultextension=".csv",
            confirmoverwrite=True,
        )
    if not filepath or not filepath.lower().endswith((".csv")):
            return
    headers = sheet.headers()
    data = sheet.get_sheet_data()
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f, dialect=csv.excel)
        writer.writerow(headers)
        writer.writerows(data)
##############################################################################################################

class InfoTable(ttk.Frame):
    def __init__(self, master, headers=(), pack=True, on_select=None, scrollbars="both"):
        """
        A styled Treeview with optional scrollbars using ttkbootstrap.

        Args:
            master (tk.Widget): Parent container.
            headers (tuple): Column headers.
            pack (bool): Whether to pack the frame.
            on_select (callable): Optional callback on row select.
            scrollbars (str): "", "x", "y", or "both"
        """
        super().__init__(master)
        self.selected_row = None
        self.on_select = on_select
        self.scrollbars = scrollbars.lower()
        # Treeview
        self.tree = ttk.Treeview(self, columns=headers, show="headings", bootstyle="primary")
        for header in headers:
            label = header.replace("_", " ").capitalize()
            self.tree.heading(header, text=label)
            self.tree.column(header, anchor=CENTER, width=120)
        # Layout control
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Optional scrollbars
        if "y" in self.scrollbars or self.scrollbars == "both":
            y_scroll = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview, bootstyle="round")
            self.tree.configure(yscrollcommand=y_scroll.set)
            y_scroll.grid(row=0, column=1, sticky="ns")
        if "x" in self.scrollbars or self.scrollbars == "both":
            x_scroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tree.xview, bootstyle="round")
            self.tree.configure(xscrollcommand=x_scroll.set)
            x_scroll.grid(row=1, column=0, sticky="ew")
        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self.handle_selection)
        if pack:
            self.pack(fill="both", expand=True, padx=4, pady=4)
    ###############        ###############        ###############        ###############
    def handle_selection(self, event=None):
        selection = self.tree.selection()
        if not selection:
            self.selected_row = None
            return
        item_id = selection[0]
        values = self.tree.item(item_id, 'values')
        self.selected_row = values if values else None
        if self.on_select and self.selected_row:
            self.on_select(self.selected_row)
    ###############        ###############        ###############        ###############
    def clear(self):
        for child in self.tree.get_children():
            self.tree.delete(child)
        self.selected_row = None
    ###############        ###############        ###############        ###############
    def add_rows(self, rows=None):
        if rows:
            for row in rows:
                self.tree.insert('', ttk.END, values=row)
    ###############        ###############        ###############        ###############
    def add_new_rows(self, rows=None):
        self.clear()
        self.add_rows(rows)
    ###############        ###############        ###############        ###############
    def delete_selection(self):
        for sel_item in self.tree.selection():
            self.tree.delete(sel_item)
        self.selected_row = None
    ###############        ###############        ###############        ###############
    def get_selected_row(self):
        return self.selected_row
##############################################################################################################