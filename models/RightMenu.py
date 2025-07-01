from config import *

class RightMenu():
    bg = "light"
    def create_menu(self,master):
        RightMenu.frame=ttk.Frame(master,bootstyle=RightMenu.bg)
        RightMenu.frame.grid(row=1,column=1,sticky="nswe")
        # title
        RightMenu.title = t = ttk.Label(RightMenu.frame , text="القائمة" ,bootstyle="inverse-"+RightMenu.bg) ; t.pack(side="top" ,pady= 20)
        ttk.Separator(RightMenu.frame).pack(fill="x" , pady=10)
        # logo
        ttk.Label(RightMenu.frame , image='logo' ,bootstyle="inverse-"+RightMenu.bg).pack(side="bottom", pady=10)
        RightMenu.options_frame = f = ttk.Frame(RightMenu.frame , width=0); f.pack(fill="both")
    ###############        ###############        ###############        ###############
    def update_menu(self,menu_ls={}):
        RightMenu.options_frame.destroy()
        RightMenu.options_frame = f = ttk.Frame(RightMenu.frame); f.pack(fill="both")
        for text,func in menu_ls.items():
            ttk.Button(f,text=text ,command=func).pack(fill="x" , pady=2)
    ###############        ###############        ###############        ###############
    def update_title(self,title="Empty"):
        RightMenu.title.config(text=title)