from config import *

class EntriesFrame(ttk.Labelframe):
    """Create a new Frame with multiple entries in grid format
    Args:
        master (tk): parent frame or window
        title (str): small text on the top left of the frame
        entry_ls (tuple or list): (entry_name , entry_type , (row , col, colspan) , options). Defaults to ().
    """
    def __init__(self,master,entry_ls=(),title="",pack=True,border=True):
        self.entry_dict = {}
        self.checkbox_dict = {}
        self.max_row = self.max_col=0
        if border:
            super().__init__(master, text=title, borderwidth=10,border=10, bootstyle="")
        else:
            super().__init__(master, text=None, borderwidth=0,border=0, bootstyle="")
        if pack:
            self.pack(fill="x" , pady =2, padx=2)
        self.entries_frame = ttk.Frame(self,bootstyle=""); self.entries_frame.pack(fill="both",expand=True,padx=2,pady=4)
        self.frames= {}
        self.entry_name_ls = []
        for entry in entry_ls:
            self.entry_name_ls.append(entry[0])
            self.add_entry(entry)
    ###############        ###############        ###############        ###############
    def add_entry(self,entry_info):
        entry_name , entry_type , pos , options=entry_info
        row, col , col_span = pos
        self.max_row = row if row > self.max_row else self.max_row
        self.max_col = col if col > self.max_col else self.max_col
        label =  " : "+ entry_name.replace('_',' ')
        self.entries_frame.grid_columnconfigure(col,weight=1)
        frame = ttk.Frame(self.entries_frame)
        frame.grid(sticky="we",row=row,column=col,columnspan=col_span,padx=2)
        # label or checkbox
        state = tk.NORMAL
        delete_disable = lambda : self.checkbox_func(entry_name)
        if "_checkbox1" in entry_type:
            entry_type = entry_type.replace("_checkbox1", "")
            self.checkbox_dict[entry_name] = checkbox(frame , command=delete_disable)
            self.checkbox_dict[entry_name].pack(side="right" ,anchor='w' , padx=10)
            self.checkbox_dict[entry_name].set(True)
        elif "_checkbox0" in entry_type:
            state= tk.DISABLED
            entry_type = entry_type.replace("_checkbox0", "")
            self.checkbox_dict[entry_name] = checkbox(frame  , command=delete_disable)
            self.checkbox_dict[entry_name].pack(side="right" ,anchor='w' , padx=10)
            self.checkbox_dict[entry_name].set(False)
        # else:
        ttk.Label(frame , text=f"{label}" ,width=20 ,anchor='e').pack(side="right", padx=10)
        # entry type
        if entry_type == "entry":
            self.entry_dict[entry_name] = ttk.Entry(frame , state=state ,justify='center' )
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
        elif entry_type == "menu":
            state = READONLY if state == tk.NORMAL else state
            self.entry_dict[entry_name] = Dropdown(frame, options=list(options) ,justify="center", state=state,bootstyle="info")
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
        elif entry_type == "date":
            self.entry_dict[entry_name] = ttk.DateEntry(master=frame , dateformat="%Y-%m-%d" )
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
            self.entry_dict[entry_name].entry.configure(justify='center')
        elif entry_type == "checkbox":
            self.entry_dict[entry_name] = checkbox(frame , text="", state=state) 
            self.entry_dict[entry_name].pack(side="right")
        elif entry_type == "textbox":
            self.entry_dict[entry_name] = ttk.Text(frame,state=state)
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
            self.entry_dict[entry_name].tag_configure('center', justify='center')
            self.entry_dict[entry_name].tag_add("center", 1.0, "end")
            self.entry_dict[entry_name].bind("<KeyRelease>", lambda e: self.entry_dict[entry_name].tag_add("center", "1.0", "end"))
        elif entry_type == "spinbox":
            self.entry_dict[entry_name] = ttk.Spinbox(frame,from_=options[0],to=options[1],increment=options[2],justify='center' ,state=state)
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
        self.frames[entry_name]= frame # save the frame in dictionary
    ###############        ###############        ###############        ###############
    def get_data(self):
        data = {}
        for entry_name in self.entry_dict:
            if isinstance(self.entry_dict[entry_name] , ttk.Text):
                data[entry_name] = self.entry_dict[entry_name].get("1.0", "end-1c")
            elif isinstance(self.entry_dict[entry_name] , ttk.DateEntry):
                data[entry_name] = self.entry_dict[entry_name].entry.get()
            else:
                data[entry_name] = self.entry_dict[entry_name].get()
        return data
    ###############        ###############        ###############        ###############
    def change_value(self,entry_name,value):
        if entry_name in self.checkbox_dict:
            self.checkbox_dict[entry_name].set(True)
        self.entry_dict[entry_name].configure(state=ttk.NORMAL)
        if isinstance(self.entry_dict[entry_name] , (ttk.Entry,)):
            self.entry_dict[entry_name].delete(0, ttk.END) 
            self.entry_dict[entry_name].insert(ttk.END,value)
        elif isinstance(self.entry_dict[entry_name] , (Dropdown,ttk.Spinbox)):
            self.entry_dict[entry_name].set(value)
        elif isinstance(self.entry_dict[entry_name] , ttk.DateEntry):
            if value:
                self.entry_dict[entry_name].entry.delete('0', 'end')
                self.entry_dict[entry_name].entry.insert(0, value)
            else:
                self.entry_dict[entry_name].entry.delete('0', 'end') 
        elif isinstance(self.entry_dict[entry_name] , (ttk.Text)):
            self.entry_dict[entry_name].delete(1.0, ttk.END) 
            self.entry_dict[entry_name].insert('insert',value)
            self.entry_dict[entry_name].tag_add("center", "1.0", "end")
    ###############        ###############        ###############        ###############
    def change_and_disable(self,entry_name,value):
        self.change_value(entry_name,value)
        self.entry_dict[entry_name].configure(state=ttk.DISABLED)
        if entry_name in self.checkbox_dict:
            self.checkbox_dict[entry_name].set(False)
    ###############        ###############        ###############        ###############
    def checkbox_func(self,entry_name):
        checkbox = self.checkbox_dict[entry_name].get()
        if checkbox == 0:
            self.change_and_disable(entry_name,"")
        else:
            self.enable_entry(entry_name)
    ###############        ###############        ###############        ###############
    def change_all(self,values):
        for entry_name,value in zip(self.entry_name_ls,values):
            if self.entry_dict[entry_name]._state == 'disabled' :
                self.change_and_disable(entry_name,value)
            else:
                self.change_value(entry_name,value)
    ###############        ###############        ###############        ###############
    def disable_all(self):
        for __ , entry in self.entry_dict.items():
            entry.configure(state=ttk.DISABLED)
    ###############        ###############        ###############        ###############
    def enable_entry(self, entry_name):
        self.entry_dict[entry_name].configure(state=ttk.NORMAL)
        if isinstance(self.entry_dict[entry_name] , Dropdown):
            first_value = self.entry_dict[entry_name].options[0] if len(self.entry_dict[entry_name].options) > 0 else ""
            self.entry_dict[entry_name].set(first_value)
            self.entry_dict[entry_name].configure(state=READONLY)
        elif isinstance(self.entry_dict[entry_name] , ttk.DateEntry):
            self.entry_dict[entry_name].entry.delete('0', 'end')
            self.entry_dict[entry_name].entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
##############################################################################################################


class checkbox(ttk.Checkbutton):
    def __init__(self, master, checked=False, **kwargs):
        self.var = ttk.BooleanVar(value=checked)
        super().__init__(master, variable=self.var, compound="right", **kwargs)
    ###############        ###############        ###############        ###############
    def set(self, checked: bool):
        """Set checked state (True/False)."""
        self.var.set(bool(checked))
    ###############        ###############        ###############        ###############
    def get(self) -> bool:
        """Return current checked state."""
        return self.var.get()
##############################################################################################################

class Dropdown(ttk.Combobox):
    def __init__(self, master, options=[], default=None, **kwargs):
        self.var = ttk.StringVar(value=default or (options[0] if options else ""))
        super().__init__(master, textvariable=self.var, values=options, **kwargs)
        self.options = options
        if default:
            self.set(default)
        elif options:
            self.set(options[0])
        self.bind("<<ComboboxSelected>>", self._on_select)
    ###############        ###############        ###############        ###############
    def _on_select(self, event=None):
        pass  # Override this method if you want a callback on selection
    ###############        ###############        ###############        ###############
    def set(self, value):
        """Set the current selection."""
        if value in self.options:
            super().set(value)
            self.var.set(value)
    ###############        ###############        ###############        ###############
    def get(self):
        """Get the current selection."""
        return self.var.get()
    ###############        ###############        ###############        ###############
    def reset_options(self, options, default=None):
        """Reset the list of options and optionally set a new default."""
        self.options = options
        self.config(values=options)
        new_value = default or (options[0] if options else "")
        self.set(new_value)
##############################################################################################################

class PlateNoFormatter:
    def __init__(self, entry: ttk.Entry):
        self.entry = entry
        self.var = entry.cget("textvariable")
        if not self.var:
            self.var = tk.StringVar()
            entry.config(textvariable=self.var)
        self.var = entry["textvariable"]
        entry.bind("<KeyRelease>", self._on_key_release)
    ###############        ###############        ###############        ###############
    def _on_key_release(self, event=None):
        # Get current cursor position and raw text
        raw_text = self.entry.get()
        cursor_pos = self.entry.index(tk.INSERT)
        # Extract only Arabic letters and digits
        letters = re.findall(r'[\u0621-\u064A]', raw_text)
        digits = re.findall(r'\d', raw_text)

        letters = letters[:3]
        digits = digits[:4]
        formatted = " ".join(letters)
        if digits:
            formatted += " " + "".join(digits)
        # Try to preserve cursor position
        cleaned_before_cursor = re.findall(r'[\u0621-\u064A\d]', raw_text[:cursor_pos])
        new_cursor_pos = 0
        count = 0
        for char in formatted:
            if char != ' ':
                count += 1
            new_cursor_pos += 1
            if count == len(cleaned_before_cursor):
                break
        self.entry.delete(0, tk.END)
        self.entry.insert(0, formatted)
        self.entry.icursor(new_cursor_pos)
##############################################################################################################