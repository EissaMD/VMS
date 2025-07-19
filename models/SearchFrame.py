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
        ttk.Button(frame ,image="search_icon" , text="" , command=self.search_btn,width=50).grid(sticky="nwes",row=0,column=0,rowspan=row+1,padx=(0,8),pady=2)
        frame = ttk.Frame(self,); frame.pack(fill="both" , padx=4 , pady=2,expand=True)
        self.sheet = Sheet(frame, show_x_scrollbar=True,height=200,show_top_left=False,
                                headers=self.layout["headrs"],
                                )
        self.sheet.set_column_widths(column_widths = self.layout["col_size"])
        binding = ("row_select", "column_width_resize", "double_click_column_resize", "column_height_resize", "arrowkeys","row_select","single_select")
        self.sheet.popup_menu_add_command("Save sheet", lambda : print("Save sheet clicked"))
        self.sheet.enable_bindings(binding)
        self.sheet.pack(fill="both", padx=4, pady=4,expand=True)
        self.window_exist = True
        self.sheet.bind("<ButtonPress-1>", self.on_select)
        self.selected_row = self.selected_row_no= None
    ###############        ###############        ###############        ###############
    def search_btn(self):
        entries = self.entries.get_data()
        values = tuple(entries.values())
        sql = self.layout["sql"].format(*values)
        DB.cursor.execute(sql) 
        records = DB.cursor.fetchall() or []
        records = [list(record) for record in records]
        self.sheet.set_sheet_data(records,False)
    ###############        ###############        ###############        ###############
    def on_select(self,event=None):
        try:
            row_no = self.sheet.identify_row(event, exclude_index = False, allow_end = True)
            row = self.sheet.get_row_data(row_no)
            self.selected_row_no = row_no
            self.selected_row = row
        except: 
            self.selected_row = self.selected_row_no= None
    ###############        ###############        ###############        ###############
    def select_layout(self,selected_layout):
        if selected_layout == "Default": ##############
            col_size =100
            col_size= [col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size,col_size]
            self.layout = { "search_entries"  :(("رقم اللوحة"       , "entry"               , (1, 2, 1), None),
                                                ("نوع المركبة"      , "menu"                , (1, 1, 1), ["","سيارة", "شاحنة", "دراجة نارية"]),
                                                ("التصنيف"          , "menu"                , (2, 2, 1), ["","سيارة", "شاحنة", "دراجة نارية"]),
                                                ("الموديل"          , "entry"               , (2, 1, 1), None),
                                                )        , 
                            "headrs"   :["رقم اللوحة"       , "الموديل"          , "نوع المركبة"  , "التصنيف"           , "اللون",
                                        "نوع التسجيل"      , "الرقم التسلسلي"   , "رقم الهيكل"   , "الجهة المستفيدة" , "مسجلة بعهدة",
                                        "المستخدم الفعلي"  , "رقم الهوية"       , "المالك"        , "هوية المالك"    , "رقم الملف"        ,
                                        "حالة المركبة"     , "ملاحظات"]            ,
                            "sql"      :"SELECT plate_number, model, vehicle_type, classification, color, registration_type, serial_number, chassis_number, beneficiary_entity, registered_under_custody, actual_user, national_id, owner, owner_id, file_number, vehicle_status FROM vehicles where plate_number LIKE'%{}%' AND vehicle_type LIKE'%{}%' AND classification LIKE'%{}%' AND model LIKE'%{}%'",
                            "col_size" :col_size}