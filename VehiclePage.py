from config import *
from models import Page , RightMenu , EntriesFrame , PlateNoFormatter , InfoTable , validate_entry ,DB , SearchFrame ,  AttachmentManager

class VehiclePage():
    def __init__(self):
        Page.create_new_page("")
        self.left_menu = RightMenu()
        menu = {
            "استعراض"           : VeiwVehicle,
            "اضافة / تعديل"       : AddVehicle,
            "استيراد"            : ImportVehicle,
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
        self.vehicle_table.InfoTable.on_select = self.select_vehicle_row
        frame = ttk.Frame(body_frame)
        frame.pack(fill="both",expand=True)
        frame.columnconfigure(0,weight=6)
        frame.columnconfigure(1,weight=10)
        self.vehicle_info_grid = InfoGrid(frame,"معلومات المركبة", columns=6)
        self.vehicle_info_grid.grid(row=0,column=1,sticky="news")
        # assign empty value to vehicle_info_grid
        columns = [x for x in v_keys_ar if x not in ["الموديل", "التصنيف", "نوع المركبة" , "رقم اللوحة"]]
        empty_data = {}
        for name in columns:
            empty_data[name] = "--"
        self.vehicle_info_grid.set_info(empty_data)
        # Attachment
        self.attachment = AttachmentManager(frame,pack=False,scrollbars='y')
        self.attachment.grid(row=0,column=0,sticky="news")
    ###############        ###############        ###############        ###############
    def select_vehicle_row(self,selected_row=None):
        if not selected_row:
            return
        columns = [x for x in v_keys_en if x not in ["plate_no", "model", "vehicle_type", "brand" ]]
        data = DB.select("vehicles", ["id"]+columns,  f"plate_no=?",[selected_row[0]])

        if not data: return
        vehicle_id = data[0][0]
        data = data[0][1:]
        
        columns = [x for x in v_keys_ar if x not in ["الموديل", "الماركة", "نوع المركبة" , "رقم اللوحة"]]
        info_dict = {}
        for key,value in zip(columns,data):
            info_dict[key] = value
        self.vehicle_info_grid.set_info(info_dict)
        self.attachment.parent_id = "v"+str(vehicle_id)
        self.attachment.load_attachments()
###############################################################################################################


class AddVehicle():
    def __init__(self):
        icon_config = [
            ("save_icon"        , "حفظ معلومات المركبة"         , self.save_vehicle),
            ("copy_data_icon"   , "اختيار معلومات مركبة اخرى"      , self.search_vehicle_window),
            ("reset_icon"       , "تصفية جميع الخانات"                       , self.clear_vehicle_entries),
        ]
        Page.create_new_page("اضافة / تعديل المركبات",icon_config)
        body_frame = Page.create_new_body()
        entries = (
            ("رقم اللوحة"       , "entry"       , (1, 2, 1), None),
            ("الموديل"          , "spinbox"     , (1, 1, 1), (1980, 2050, 1)),
            ("نوع المركبة"      , "entry"       , (2, 2, 1), None),
            ("الماركة"          , "entry"       , (3, 2, 1), None),
            ("اللون"            , "entry"       , (2, 1, 1), None),    
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
            ("حالة الضمان"       , "menu"      , (1, 3, 1), [ "ساري", "غير ساري",]),
            ("بداية الضمان"     , "entry"        , (1, 2, 1), None),
            ("نهاية الضمان"     , "entry"        , (1, 1, 1), None),
        )
        self.insurance_info = EntriesFrame(body_frame,entries, title="معلومات الضمان")  
        entries = (
            ("رقم الملف"       , "entry"     , (1, 1, 1), None),
            ("حالة المركبة"     , "menu"    , (2, 1, 1), [ "ممتازة", "جيدة", "بحاجة الى صيانة", "رجيع", "تالف" , "مباعة" ]),
            ("ملاحظات"          , "textbox"     , (3, 1, 2), None),
        )
        self.addtional_info = EntriesFrame(body_frame,entries, title="معلومات اضافية")
        self.addtional_info.entry_dict["ملاحظات"].configure(height=3)
        self.attachments = AttachmentManager(body_frame,edit_btns=True)
    ###############        ###############        ###############        ###############
    def save_vehicle(self):
        data = {}
        for frame in (self.vehicle_entries, self.benifatury_entries ,self.insurance_info ,self.addtional_info):
            data.update(frame.get_data())
        # Validate entries
        ret = validate_entry(data)
        if ret: return
        #
        plate_no = data["رقم اللوحة"]
        data = [data[key] for key in v_keys_ar]
        col_name = v_keys_en
        # check if plate_no exist in database
        vehicle_row = DB.select("vehicles","*","plate_no=?",(plate_no,))
        if vehicle_row:
            error_text = "رقم اللوحة موجود بالفعل '{}'. هل تريد استبدال البيانات الحالية؟".format(plate_no)
            ret =Messagebox.show_question(error_text,buttons=["نعم","لا"])
            if ret == "لا":
                return
            successful = DB.update("vehicles", col_name,"plate_no=?", list(data)+[plate_no])
            if not successful:
                return
            vehicle_id = vehicle_row[0][0]
            self.attachments.parent_id = "v"+str(vehicle_id) # vehicle id
        else:
            successful = DB.insert("vehicles", col_name, data)
            if not successful:
                return
            vehicle_row = DB.select("vehicles","*","plate_no=?",(plate_no,))
            vehicle_id = vehicle_row[0][0]
            self.attachments.parent_id = "v"+str(vehicle_id) # vehicle id
        self.attachments.save_changes()
        Messagebox.show_info("تم حفظ المركبة بنجاح","تم")
    ###############        ###############        ###############        ###############
    def search_vehicle_window(self):
        self.window = ttk.Toplevel( size=(600,300))
        self.search_frame = SearchFrame(self.window)
        self.search_frame.InfoTable.tree.bind('<Double-Button-1>',self.select_vehicle_from_window)
    ###############        ###############        ###############        ###############
    def select_vehicle_from_window(self,event=None):
        selected_row = self.search_frame.selected_row
        if not selected_row:
            return
        self.window.destroy()
        plate_no = selected_row[0]
        columns = ["id"]+list(v_keys_en)
        data = DB.select("vehicles", columns,  f"plate_no=?",[plate_no])
        vehicle_info = data[0][1:]
        vehicle_id = data[0][0]
        # self.vehicle_entries.change_all()
        for entries in (self.vehicle_entries, self.benifatury_entries, self.insurance_info ,self.addtional_info):
            keys = entries.entry_dict.keys()
            for entry_name in keys:
                entries.change_value(entry_name,vehicle_info.pop(0))
        self.attachments.parent_id = "v"+ str(vehicle_id)
        self.attachments.load_attachments()
    ###############        ###############        ###############        ###############
    def clear_vehicle_entries(self):
        for entries in (self.vehicle_entries, self.benifatury_entries, self.addtional_info):
            keys = entries.entry_dict.keys()
            for entry_name in keys:
                entries.change_value(entry_name,"")
        self.attachments.files.clear()
        self.attachments.table.clear()
###############################################################################################################

class ImportVehicle():
    def __init__(self):
        icon_config = [
            ("save_icon"        , "حفظ جميع المركبات المستوردة" , self.save_imported_vehicles),
            ("reset_icon"       , "تصفية جميع الخانات"           , self.clear_vehicles_table),
            ("excel_icon"       , "إنشاء قالب المركبات"          , self.create_vehicle_template),
        ]
        Page.create_new_page("استيراد المركبات" , icon_config)
        body_frame = Page.create_new_body()
        self.vehicle_table = SearchFrame(body_frame, "import vehicle")
        self.vehicle_table.entries.change_and_disable("اسم الملف","")
        self.vehicle_table.btn.configure(image="" , text="اختار ملف" , command=self.import_vehicles,width=10)
    ###############        ###############        ###############        ###############
    def import_vehicles(self):
        file_path = filedialog.askopenfilename(filetypes=[
                                                            ("Excel files", "*.xlsx"),
                                                            ("CSV files", "*.csv"),
                                                            ("All files", "*.*")
                                                        ])
        if not file_path:
            return
        rows = []
        if file_path.endswith(".xlsx"):
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip headers
                cleaned_row = [cell if cell is not None else "" for cell in row[:17]]
                rows.append(cleaned_row)
        elif file_path.endswith(".csv"):
            with open(file_path, newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # skip headers
                for row in reader:
                    cleaned_row = [cell if cell is not None else "" for cell in row[:17]]
                    rows.append(cleaned_row)
        self.vehicle_table.InfoTable.clear()
        self.vehicle_table.InfoTable.add_rows(rows)
        self.vehicle_table.entries.change_and_disable("اسم الملف",str(file_path))
    ###############        ###############        ###############        ###############
    def create_vehicle_template(self):
        headers = [
            "رقم اللوحة", "الموديل", "نوع المركبة", "التصنيف", "اللون",
            "نوع التسجيل", "الرقم التسلسلي", "رقم الهيكل", "الجهة المستفيدة", "مسجلة بعهدة",
            "المستخدم الفعلي", "رقم الهوية", "المالك", "هوية المالك", "رقم الملف",
            "حالة المركبة", "ملاحظات"
        ]

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel file", "*.xlsx"), ("CSV file", "*.csv")],
            title="اختر مكان حفظ ملف القالب"
        )
        if not file_path:
            return
        try:
            if file_path.endswith(".xlsx"):
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(headers)
                wb.save(file_path)
            elif file_path.endswith(".csv"):
                with open(file_path, mode='w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
            else:
                Messagebox.show_error("امتداد الملف غير مدعوم. استخدم .xlsx أو .csv" , "خطأ")
                return
            Messagebox.show_info(f"تم إنشاء الملف بنجاح:\n{os.path.basename(file_path)}","تم" )
        except Exception as e:
            Messagebox.show_error(str(e),"خطأ أثناء الحفظ" )
    ###############        ###############        ###############        ###############
    def save_imported_vehicles(self):
        # error_text = """هل تريد استبدال البيانات الحالية اذا وجدت؟ \n نعم:سيتم استيراد جميع المركبات مع تعديل الموجود في قاعدة البيانات. \n لا:سيتم استيراد المركبات الغير متوفرة في قاعدة البيانات(امن) \n"""
        # ret =Messagebox.show_question(error_text,buttons=["نعم","لا","الغاء العملية"])
        # if ret == "الغاء العملية":
        #     return
        tree =self.vehicle_table.InfoTable.tree
        col_name = v_keys_en
        for row_id in tree.get_children():
            values = tree.item(row_id, "values")
            # check if plate_no exist in database
            vehicle_row = DB.select("vehicles","*","plate_no=?",(values[0],))
            if vehicle_row:
                continue
            DB.insert("vehicles", col_name, values)
        Messagebox.show_info(f"تم استيراد الملف الى قاعدة البيانات بنجاح","تم" )
    ###############        ###############        ###############        ###############
    def clear_vehicles_table(self):
        self.vehicle_table.InfoTable.clear()
        self.vehicle_table.entries.change_and_disable("اسم الملف","")
###############################################################################################################

class InfoGrid(ttk.Labelframe):
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