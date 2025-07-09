from config import *
from models import Page , RightMenu , EntriesFrame , PlateNoFormatter , DisplayTable

class VehiclePage():
    def __init__(self):
        Page.create_new_page("")
        self.left_menu = RightMenu()
        menu = {
            "استعراض"           : VeiwVehicle,
            "اضافة"             : self.empty_page,
            "تقارير"            : self.empty_page,
        }
        self.left_menu.update_menu(menu)
        VeiwVehicle()
    ###############        ###############        ###############        ###############
    def empty_page(self):
            Page.create_new_page(title="No Title")
###############################################################################################################

class VeiwVehicle():
    def __init__(self):
        Page.create_new_page("عرض المركبات")
        body_frame = Page.create_new_body()
        entries = (
            ("رقم اللوحة"       , "entry"   , (1, 4, 1), None),
            ("نوع المركبة"      , "menu_checkbox0"    , (1, 3, 1), ["سيارة", "شاحنة", "دراجة نارية"]),
            ("التصنيف"          , "menu"    , (1, 2, 1), ["سيارة", "شاحنة", "دراجة نارية"]),
            ("الموديل"          , "entry"   , (1, 1, 1), None),
        )
        self.search_frame = EntriesFrame(body_frame,entries, title="بحث المركبات")
        frame = self.search_frame.entries_frame
        ttk.Button( frame, text="بحث",command=self.get_entries).grid(row=1,column=0 , padx=10)
        PlateNoFormatter(self.search_frame.entry_dict["رقم اللوحة"])
        # Vehicle table
        frame = ttk.Frame(body_frame,height=300)
        frame.pack(fill="x",expand=True)
        col_size = 260
        col_sizes = [col_size, col_size, col_size, col_size]
        layout = { "headrs"   :[ "الموديل", "التصنيف", "نوع المركبة" , "رقم اللوحة"]            ,
                "col_size" :col_sizes}
        self.vehicle_table = DisplayTable(frame, layout)
        data=[
                ["2020", "خدمة", "وانيت", "س ع ر 3452"],
                ["2018", "رسمية", "جيب", "ب ن ك 8124"],
                ["2022", "نقل", "دينا", "ح ط ل 1023"],
                ["2019", "رسمية", "سيدان", "م ق س 7741"],
                ["2021", "خدمة", "بيك أب", "ش ل ي 2290"],
                ["2017", "رسمية", "صالون", "ف ك ت 6055"],
                ["2023", "نقل", "هايلكس", "و ص د 9903"],
                ["2020", "خدمة", "ميكروباص", "ق ب ن 4478"],
                ["2016", "رسمية", "هاف لوري", "ر ج ز 1330"],
                ["2021", "نقل", "راف فور", "ن س ع 3762"],
            ]
        self.vehicle_table.update(data)
        frame = ttk.Frame(body_frame,height=300)
        frame.pack(fill="x",expand=True)
        self.vehicle_info_grid = VehicleInfoGrid(frame)
    ###############        ###############        ###############        ###############
    def get_entries(self):
        print(self.search_frame.get_data())
###############################################################################################################

class VehicleInfoGrid(ttk.Frame):
    def __init__(self, parent, columns=4, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columns = columns
        self.labels = {}  # Store label widgets by key
    ###############        ###############        ###############        ###############
    def set_info(self, info_dict: dict):
        # Clear previous widgets
        for widget in self.winfo_children():
            widget.destroy()
        self.labels.clear()

        keys = list(info_dict.keys())
        for idx, key in enumerate(keys):
            row = idx // self.columns
            col = idx % self.columns

            value = info_dict[key]
            full_text = f"{key} : {value}"
            lbl = ttk.Label(self, text=full_text, anchor='e', justify='right', width=30)
            lbl.grid(row=row, column=col, padx=10, pady=8, sticky='e')

            self.labels[key] = lbl  # Optional: store label for direct access later
###############################################################################################################