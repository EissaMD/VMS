from config import *
from models import Page , RightMenu , EntriesFrame , PlateNoFormatter , DisplayTable , InfoTable , validate_entry ,DB , SearchFrame

v_keys_en = ("plate_number"      , "model"               , "vehicle_type"  , "classification"       , "color"               , 
            "registration_type" , "serial_number"       ,"chassis_number" ,"beneficiary_entity"   , "registered_under_custody", 
            "actual_user"       , "national_id"         ,"owner"          , "owner_id"          , "file_number"             , 
            "vehicle_status"    ,"notes")
v_keys_ar = ("رقم اللوحة"       , "الموديل"          , "نوع المركبة"  , "التصنيف"           , "اللون",
            "نوع التسجيل"      , "الرقم التسلسلي"   , "رقم الهيكل"   , "الجهة المستفيدة" , "مسجلة بعهدة",
            "المستخدم الفعلي"  , "رقم الهوية"       , "المالك"        , "هوية المالك"    , "رقم الملف"        ,
            "حالة المركبة"     , "ملاحظات")
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
        self.vehicle_table = SearchFrame(body_frame, "Default")
        self.vehicle_table.sheet.on_select = self.select_vehicle_row
        frame = ttk.Frame(body_frame)
        frame.pack(fill="x",expand=True)
        self.vehicle_info_grid = VehicleInfoGrid(frame,"معلومات المركبة", columns=6)
        self.vehicle_info_grid.pack(side="right")
        columns = [x for x in v_keys_ar if x not in ["الموديل", "التصنيف", "نوع المركبة" , "رقم اللوحة"]]
        empty_data = {}
        for name in columns:
            empty_data[name] = "--"
        self.vehicle_info_grid.set_info(empty_data)
    ###############        ###############        ###############        ###############
    def select_vehicle_row(self,selected_row=None):
        if not selected_row:
            return
        columns = [x for x in v_keys_en if x not in ["plate_number", "model", "vehicle_type", "classification" ]]
        data = DB.select("vehicles", columns,  f"plate_number=?",[selected_row[0]])
        if not data: return
        data = data[0]
        columns = [x for x in v_keys_ar if x not in ["الموديل", "التصنيف", "نوع المركبة" , "رقم اللوحة"]]
        info_dict = {}
        for key,value in zip(columns,data):
            info_dict[key] = value
        self.vehicle_info_grid.set_info(info_dict)
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


class VehicleInfoGrid(ttk.Labelframe):
    def __init__(self, parent,title="", columns=3, *args, **kwargs):
        super().__init__(parent,text=title , *args, **kwargs)
        self.columns = columns
        self.label_widgets = []
    ###############        ###############        ###############        ###############  
    def set_info(self, info_dict: dict):
        # Clear previous content
        for widget in self.winfo_children():
            widget.destroy()
        self.label_widgets.clear()
        items = list(info_dict.items())
        for row_idx in range(0, len(items), self.columns):
            row_frame = ttk.Frame(self)
            row_frame.pack(fill='x', anchor='e', pady=4)
            for i in range(self.columns):
                idx = row_idx + i
                if idx >= len(items):
                    break
                key, value = items[idx]
                pair_frame = ttk.Frame(row_frame)
                pair_frame.pack(side='right', padx=10)
                key_lbl = ttk.Label(pair_frame, text=key, anchor='e', justify='right')
                key_lbl.pack(side='top', anchor='e')
                val_lbl = ttk.Label(pair_frame, text=value, anchor='e', justify='right', bootstyle='info')
                val_lbl.pack(side='top', anchor='e')
                self.label_widgets.append((key_lbl, val_lbl))
###############################################################################################################