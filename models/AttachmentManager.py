from config import *
from .Table import InfoTable
from .DB import DB

class AttachmentManager(ttk.Labelframe):
    def __init__(self, master,  parent_id="default", title="المرفقات",edit_btns=False,pack=True):
        self.parent_id = parent_id
        self.files = []  # unified list of dicts
        super().__init__(master, text=title)
        if pack:
            self.pack(fill="both",expand=True, padx=4, pady=4)
        self.table = InfoTable(self, headers=("الحجم", "الاسم"))
        self.table.pack(fill=BOTH, expand=True, side=LEFT)
        self.table.tree.bind("<Double-1>", self.open_selected_file)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=LEFT, fill=Y, padx=4)
        if edit_btns:
            ttk.Button(btn_frame, text="إضافة مرفق +", bootstyle="outline-primary", command=self.add_attachment).pack(fill='both', pady=2)
            ttk.Button(btn_frame, text="إزالة مرفق -", bootstyle="outline-danger", command=self.ui_remove_selected).pack(fill='both', pady=2)
    ###############        ###############        ###############        ###############
    def add_attachment(self):
        paths = filedialog.askopenfilenames(title="اختر الملفات")
        for path in paths:
            name = os.path.basename(path)
            if self._file_exists(name):  # prevent duplicates
                continue
            with open(path, "rb") as f:
                data = f.read()
            size = os.path.getsize(path)
            self.files.append({"name": name, "size": size, "data": data, "type": "added"})
            self.table.tree.insert('', 'end', values=(self._get_readable_size(size), name))
    ###############        ###############        ###############        ###############
    def _file_exists(self, name):
        for f in self.files:
            if f["name"] == name and f["type"] != "deleted":
                return True
        return False
    ###############        ###############        ###############        ###############
    def ui_remove_selected(self):
        for item in self.table.tree.selection():
            name = self.table.tree.item(item)["values"][1]
            self.table.tree.delete(item)

            for file in self.files:
                if file["name"] == name:
                    if file["type"] == "added":
                        self.files.remove(file)
                    elif file["type"] == "loaded":
                        file["type"] = "deleted"
                    break
    ###############        ###############        ###############        ###############
    def save_changes(self):
        # Delete
        for file in self.files[:]:
            if file["type"] == "deleted":
                DB.cursor.execute(
                    "DELETE FROM attachments WHERE parent_id=? AND file_name=?",
                    (self.parent_id, file["name"])
                )
                self.files.remove(file)
        # Insert new
        for file in self.files:
            if file["type"] == "added":
                DB.cursor.execute("""
                    INSERT INTO attachments (parent_id, file_name, file_size, file_data)
                    VALUES (?, ?, ?, ?)
                """, (self.parent_id, file["name"], file["size"], file["data"]))
                file["type"] = "loaded"
        DB.conn.commit()
    ###############        ###############        ###############        ###############
    def load_attachments(self):
        self.files.clear()
        self.table.clear()
        DB.cursor.execute("SELECT file_name, file_size, file_data FROM attachments WHERE parent_id=?", (self.parent_id,))
        for name, size, data in DB.cursor.fetchall():
            self.files.append({"name": name, "size": size, "data": data, "type": "loaded"})
            self.table.tree.insert('', 'end', values=(self._get_readable_size(size), name))
    ###############        ###############        ###############        ###############
    def open_selected_file(self, event=None):
        selected_row = self.table.get_selected_row()
        if not selected_row: return
        name = selected_row[1]
        file = next((f for f in self.files if f["name"] == name and f["type"] != "deleted"), None)
        if file:
            path = os.path.join(tempfile.gettempdir(), name)
            with open(path, "wb") as f:
                f.write(file["data"])
            os.startfile(path)
    ###############        ###############        ###############        ###############
    @staticmethod
    def _get_readable_size(size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"