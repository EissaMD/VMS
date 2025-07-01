from config import *

class EntriesFrame(ttk.Frame):
    """Create a new Frame with multiple entries in grid format
    Args:
        master (tk): parent frame or window
        title (str): small text on the top left of the frame
        entry_ls (tuple or list): (entry_name , entry_type , (row , col, colspan) , options). Defaults to ().
    """
    def __init__(self,master,entry_ls=(),pack=True):
        self.entry_dict = {}
        self.checkbox_dict = {}
        self.max_row = self.max_col=0
        super().__init__(master, borderwidth=10,border=10, bootstyle="")
        if pack:
            self.pack(fill="x" , pady =2, padx=2)
        self.entries_frame = ttk.Frame(self,bootstyle="light"); self.entries_frame.pack(fill="both",expand=True,padx=2,pady=4)
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
        ttk.Label(frame , text=f"{label}" ).pack(side="right" ,anchor='w', padx=10)
        # entry type
        if entry_type == "entry":
            self.entry_dict[entry_name] = ttk.Entry(frame , state=state)
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
            self.entry_dict[entry_name]._state = state
        elif entry_type == "menu":
            self.entry_dict[entry_name] = Dropdown(frame, options=list(options) , state=state)
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
            self.entry_dict[entry_name]._state = state
        elif entry_type == "date":
            self.entry_dict[entry_name] = ttk.DateEntry(master=frame , dateformat="%Y-%m-%d" )
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
            self.entry_dict[entry_name]._state = state
        elif entry_type == "checkbox":
            self.entry_dict[entry_name] = checkbox(frame , text="", state=state) 
            self.entry_dict[entry_name].pack(side="right")
            self.entry_dict[entry_name]._state = state
        elif entry_type == "textbox":
            self.entry_dict[entry_name] = ttk.Text(frame ,state=state)
            self.entry_dict[entry_name].pack(side="right", fill="x" , expand=True)
            self.entry_dict[entry_name]._state = state
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
        elif isinstance(self.entry_dict[entry_name] , (Dropdown,)):
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
    ###############        ###############        ###############        ###############
    def change_and_disable(self,entry_name,value):
        self.change_value(entry_name,value)
        self.entry_dict[entry_name].configure(state=ttk.DISABLED)
        self.entry_dict[entry_name]._state = 'disabled'
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
            entry._state = 'disabled'
    ###############        ###############        ###############        ###############
    def enable_entry(self, entry_name):
        self.entry_dict[entry_name].configure(state=ttk.NORMAL)
        if isinstance(self.entry_dict[entry_name] , Dropdown):
            first_value = self.entry_dict[entry_name]._values[0]
            self.entry_dict[entry_name].set(first_value)
        elif isinstance(self.entry_dict[entry_name] , ttk.DateEntry):
            self.entry_dict[entry_name].entry.delete('0', 'end')
            self.entry_dict[entry_name].entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_dict[entry_name]._state = 'normal'
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

class Dropdown(ttk.Menubutton):
    def __init__(self, master, options, default=None, **kwargs):
        self.var = ttk.StringVar(value=default or (options[0] if options else ""))
        super().__init__(master, text=self.var.get(), **kwargs)
        self.menu = ttk.Menu(self, tearoff=0)
        self["menu"] = self.menu
        self.options = options
        self._build_menu()
    ###############        ###############        ###############        ###############
    def _build_menu(self):
        self.menu.delete(0, "end")
        for option in self.options:
            self.menu.add_radiobutton(label=option, variable=self.var,
                                      command=self._on_select)
    ###############        ###############        ###############        ###############
    def _on_select(self):
        self.config(text=self.var.get())
    ###############        ###############        ###############        ###############
    def set(self, value):
        """Set the current selection."""
        if value in self.options:
            self.var.set(value)
            self.config(text=value)
    ###############        ###############        ###############        ###############
    def get(self):
        """Get the current selection."""
        return self.var.get()
    ###############        ###############        ###############        ###############
    def reset_options(self, options, default=None):
        """Reset the list of options and optionally set a new default."""
        self.options = options
        new_value = default or (options[0] if options else "")
        self.var.set(new_value)
        self.config(text=new_value)
        self._build_menu()
##############################################################################################################