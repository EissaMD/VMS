from config import *
from models import Page , RightMenu , EntriesFrame , PlateNoFormatter , DisplayTable , InfoTable , validate_entry ,DB
class VehiclePage():
    def __init__(self):
        Page.create_new_page("")
        self.left_menu = RightMenu()
        menu = {
            "استعراض"           : VeiwVehicle,
            "اضافة"             : AddVehicle,
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
            ("رقم اللوحة"       , "entry"               , (1, 4, 1), None),
            ("نوع المركبة"      , "menu_checkbox0"      , (1, 3, 1), ["سيارة", "شاحنة", "دراجة نارية"]),
            ("التصنيف"          , "menu"                , (1, 2, 1), ["سيارة", "شاحنة", "دراجة نارية"]),
            ("الموديل"          , "entry"               , (1, 1, 1), None),
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


class AddVehicle():
    def __init__(self):
        icon_config = [
            ("save_icon"        , "حفظ معلومات المركبة"         , self.save_vehicle),
            ("copy_data_icon"   , "نسخ معلومات مركبة اخرى"      , lambda: print("Save clicked")),
            ("reset_icon"       , "تصفية"                       , lambda: print("Logout clicked")),
        ]
        Page.create_new_page("اضافة مركبة",icon_config)
        body_frame = Page.create_new_body()
        entries = (
            ("رقم اللوحة"       , "entry"       , (1, 2, 1), None),
            ("الموديل"          , "spinbox"     , (1, 1, 1), (1980, 2050, 1)),
            ("نوع المركبة"      , "entry"       , (2, 2, 1), None),
            ("اللون"            , "entry"       , (2, 1, 1), None),
            ("التصنيف"          , "entry"       , (3, 2, 1), None),
            ("نوع التسجيل"      , "entry"       , (3, 1, 1), None),
            ("الرقم التسلسلي"   , "entry"       , (4, 1, 2), None),
            ("رقم الهيكل"       , "entry"       , (5, 1, 2), None),
            
        )
        self.vehicle_entries = EntriesFrame(body_frame,entries, title="معلومات المركبة")
        PlateNoFormatter(self.vehicle_entries.entry_dict["رقم اللوحة"])
        entries = (
            ("الجهة المستفيدة"          , "entry"       , (1, 2, 1), None),
            ("مسجلة بعهدة"              , "entry"       , (1, 1, 1), (1980, 2050, 1)),
            ("المستخدم الفعلي"          , "entry"       , (2, 2, 1), None),
            ("رقم الهوية"               , "entry"       , (2, 1, 1), None),
            ("المالك"                   , "entry"       , (3, 2, 1), None),
            ("هوية المالك"              , "entry"       , (3, 1, 1), None),
            
        )
        self.benifatury_entries = EntriesFrame(body_frame,entries, title="معلومات المستفيد")
        entries = (
            ("رقم الملف"       , "entry"     , (1, 1, 1), None),
            ("حالة المركبة"     , "menu"    , (2, 1, 1), [ "نشطة", "غير نشطة", "موقوفة"]),
            ("ملاحظات"          , "textbox"     , (3, 1, 2), None),
        )
        self.addtional_info = EntriesFrame(body_frame,entries, title="معلومات اضافية")
        self.addtional_info.entry_dict["ملاحظات"].configure(height=5)
        # Attachments
        frame = ttk.Labelframe(body_frame,text="إضافة مرفقات")
        frame.pack(fill="x"  ,padx=2, pady=2)
        headers = ( "حجم المرفق","اسم المرفق")
        self.img_table = InfoTable(frame,headers)
        self.img_table.pack(fill="x" , expand=True ,side="left")
        frame = ttk.Frame(frame); frame.pack(side="left",fill="y")
        ttk.Button(frame,text="+" ,bootstyle="outline" ,).pack(fill="both",expand=True)
        ttk.Button(frame,text="-" ,bootstyle="outline" , command=self.img_table.delete_selection).pack(fill="both",expand=True)
    ###############        ###############        ###############        ###############
    def save_vehicle(self):
        # data = {}
        # for frame in (self.vehicle_entries, self.benifatury_entries, self.addtional_info):
        #     data.update(frame.get_data())
        # # Validate entries
        # ret = validate_entry(data)
        # if ret: return
        # Process data
        data = {"رقم اللوحة": "س د ك 1234"  ,"الموديل": 2022,"نوع المركبة": "تويوتا","اللون": "أسود"            ,"التصنيف": "خصوصي",
                "نوع التسجيل": "خاصة"       ,"الجهة المستفيدة": "بلدية الرياض"      ,"مسجلة بعهدة": "نعم"       ,"المستخدم الفعلي": "محمد العتيبي",
                "رقم الهوية": "1020304050"  ,"الرقم التسلسلي": "SN123456789"        ,"رقم الهيكل": "CH987654321"    ,"المالك": "أمانة الرياض",
                "هوية المالك": "3030303030" ,"ملاحظات": "السيارة بحالة ممتازة"      ,"حالة المركبة": "قيد الخدمة"   ,"رقم الملف": "VR-8907"
                }
        
        data = (data["رقم اللوحة"],data["الموديل"]      ,data["نوع المركبة"]    ,data["اللون"]          ,data["التصنيف"],
                data["نوع التسجيل"],data["الرقم التسلسلي"],data["رقم الهيكل"]    ,data["الجهة المستفيدة"],data["مسجلة بعهدة"],
                data["المستخدم الفعلي"],data["رقم الهوية"],data["المالك" ],data["هوية المالك"],
                data["رقم الملف"]    ,data["حالة المركبة"]   ,data["ملاحظات"])
        col_name = ("plate_number"      , "model"               , "vehicle_type"    , "color"               , "classification", 
                    "registration_type" , "serial_number"       ,"chassis_number" ,"beneficiary_entity"   , "registered_under_custody", 
                    "actual_user"       , "national_id"         ,"owner"          , "owner_id"          ,
                    "notes"             , "vehicle_status"      , "file_number")
        successful = DB.insert("vehicles", col_name, data)

        
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