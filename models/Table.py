from config import *


class DisplayTable(ttk.Labelframe):
    def __init__(self,master , layout=False , pack=True):
        super().__init__(master=master)
        if layout is False: return
        self.layout = layout
        self.sheet = Sheet(self,headers=self.layout["headrs"])
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