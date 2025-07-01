from config import *
from models import Page , RightMenu , EntriesFrame

class VehiclePage():
    def __init__(self):
        Page.create_new_page("- - -")
        self.left_menu = RightMenu()
        menu = {
            "استعراض"           : VeiwVehicle,
            "اضافة\تعديل"           : self.empty_page,
            "تقارير"           : self.empty_page,
        }
        self.left_menu.update_menu(menu)
        VeiwVehicle()
    ###############        ###############        ###############        ###############
    def empty_page(self):
            Page.create_new_page(title="No Title")
###############################################################################################################

class VeiwVehicle():
    def __init__(self):
        body_frame = Page.create_new_body()
        entries = (
            ("اسم المركبة", "textbox", (0, 0, 1), ["سيارة", "شاحنة", "دراجة نارية"]),
            ("رقم اللوحة"  , "entry", (0, 1, 1), None),
        )

        self.search_frame = EntriesFrame(body_frame,entries)

        ttk.Button(
            body_frame, 
            text="بحث",command=self.get_entries).pack()
    
    def get_entries(self):
        print(self.search_frame.get_data())