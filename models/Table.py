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

class InfoTable(ttk.Treeview):
    def __init__(self,master,headers=()):
        self.data = {} # initialize empty tree
        super().__init__(master, columns=headers, show="headings" , bootstyle="primary" )
        for header in headers:
            label = header.replace("_", " ")
            label = label.capitalize()
            self.heading(header, text=label)
    ###############        ###############        ###############        ###############
    def clear(self):
        self.data = []
        self.delete(*self.get_children())
    ###############        ###############        ###############        ###############
    def add_rows(self,rows=None):
        if rows is not None:
            for row in rows:
                self.insert('', ttk.END, values=row)
                self.data[self.get_children()[-1]] = row
    ###############        ###############        ###############        ###############
    def add_new_rows(self,rows=None):
        if rows is not None:
            self.data = {}
            self.clear()
            self.add_rows(rows)
    ###############        ###############        ###############        ###############
    def delete_selection(self):
        for sel_item in self.selection():
            self.delete(sel_item)
            self.data.pop(sel_item)
##############################################################################################################