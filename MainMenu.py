from config import *
from LoginPage import LoginPage

class MainMenu(ttk.Frame):
    def __init__(self,master):
        super().__init__(master,bootstyle="primary")
        self.frame = ttk.Frame(self); self.frame.place(relx=0.5, rely=0.5, anchor="center")
        frame = ttk.Frame(self ,bootstyle="") ; frame.pack(side="left")
        # frame = ttk.Frame(frame ) ; frame.pack(padx=2,pady=2)
        # frame = self
        ttk.Label(frame,text=LoginPage.user_name).pack(side="right" , padx=4)
        ttk.Button(frame , text="", image="logout_icon",width=20, command=LoginPage.start).pack(side="right")
    ###############        ###############        ###############        ###############
    def create(self):
        self.frame.destroy()
        self.frame = ttk.Frame(self,bootstyle="primary"); self.frame.place(relx=0.5, rely=0.5, anchor="center")
        menu = {
            "مركبات 1"             : lambda : print("About clicked"),
            "مركبات 2"             : lambda : print("About clicked"),
        }
        for text,btn in menu.items():
                ttk.Button(self.frame,text=text,command=btn ,width=10 , bootstyle="primary").pack(side="right",pady=2,padx=20)

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
            ttk.Button(f,text=text ,command=func,text_color="black"  ).pack(fill="x" , pady=2)
    ###############        ###############        ###############        ###############
    def update_title(self,title="Empty"):
        RightMenu.title.config(text=title)