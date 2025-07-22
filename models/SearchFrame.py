from config import *
from .DB import DB
from .EntriesFrame import EntriesFrame
from .Table import DisplayTable, InfoTable

class SearchFrame(ttk.Labelframe):
    def __init__(self,master , layout="Default",title="بحث",pack=True):
        super().__init__(master=master , text=title)
        if isinstance(layout,dict): # layout not inclduded
            self.layout=layout
        else:
            ret = self.select_layout(layout)
            if ret is False: return
        if pack:
            self.pack(fill="both", expand=True, padx=4, pady=4)
        self.entries = EntriesFrame(self,self.layout["search_entries"],"",True,False) 
        col , row = self.entries.max_col , self.entries.max_row
        frame = self.entries.entries_frame 
        self.btn = ttk.Button(frame ,image="search_icon" , text="" , command=self.search_btn,width=50)
        self.btn.grid(sticky="nwes",row=0,column=0,rowspan=row+1,padx=(0,8),pady=2)
        frame = ttk.Frame(self,); frame.pack(fill="both" , padx=4 , pady=2,expand=True)
        self.InfoTable = InfoTable(frame,self.layout["headrs"],on_select=self.on_select)
    ###############        ###############        ###############        ###############
    def search_btn(self):
        entries = self.entries.get_data()
        values = tuple(entries.values())
        sql = self.layout["sql"].format(*values)
        DB.cursor.execute(sql) 
        records = DB.cursor.fetchall() or []
        records = [list(record) for record in records]
        self.InfoTable.add_new_rows(records)
    ###############        ###############        ###############        ###############
    def on_select(self,selected_row=None):
            self.selected_row =selected_row
    ###############        ###############        ###############        ###############
    def select_layout(self,selected_layout):
        if selected_layout == "Default": ##############
            col_size =100
            col_size= [col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size]
            self.layout = { "search_entries"  :(("رقم اللوحة"       , "entry"               , (1, 2, 1), None),
                                                ("نوع المركبة"      , "entry"                , (1, 1, 1), ["","سيارة", "شاحنة", "دراجة نارية"]),
                                                ("التصنيف"          , "entry"                , (2, 2, 1), ["","سيارة", "شاحنة", "دراجة نارية"]),
                                                ("الموديل"          , "entry"               , (2, 1, 1), None),
                                                )        , 
                            "headrs"   :["رقم اللوحة"       , "الموديل"          , "نوع المركبة"  , "التصنيف"           , "اللون",
                                        "نوع التسجيل"      , "الرقم التسلسلي"   , "رقم الهيكل"   , "الجهة المستفيدة" , "مسجلة بعهدة",
                                        "المستخدم الفعلي"  , "رقم الهوية"       , "المالك"        , "هوية المالك"    , "رقم الملف"        ,
                                        "حالة المركبة"     , "ملاحظات"]            ,
                            "sql"      :"SELECT plate_no, model, vehicle_type, classification, color, registration_type, serial_number, chassis_number, beneficiary_entity, registered_under_custody, actual_user, national_id, owner, owner_id, file_number, vehicle_status FROM vehicles where plate_no LIKE'%{}%' AND vehicle_type LIKE'%{}%' AND classification LIKE'%{}%' AND model LIKE'%{}%'",
                            "col_size" :col_size}
        elif selected_layout == "import vehicle": ##############
            col_size =100
            col_size= [col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size]
            self.layout = { "search_entries"  :(("اسم الملف"       , "entry"               , (1, 2, 1), None),),
                            "headrs"   :["رقم اللوحة"       , "الموديل"          , "نوع المركبة"  , "التصنيف"           , "اللون",
                                        "نوع التسجيل"      , "الرقم التسلسلي"   , "رقم الهيكل"   , "الجهة المستفيدة" , "مسجلة بعهدة",
                                        "المستخدم الفعلي"  , "رقم الهوية"       , "المالك"        , "هوية المالك"    , "رقم الملف"        ,
                                        "حالة المركبة"     , "ملاحظات"]            ,
                            "sql"      :"SELECT plate_no, model, vehicle_type, classification, color, registration_type, serial_number, chassis_number, beneficiary_entity, registered_under_custody, actual_user, national_id, owner, owner_id, file_number, vehicle_status FROM vehicles where plate_no LIKE'%{}%' AND vehicle_type LIKE'%{}%' AND classification LIKE'%{}%' AND model LIKE'%{}%'",
                            "col_size" :col_size}