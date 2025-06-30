from config import *
from LoginPage import LoginPage

class MainMenu(ttk.Frame):
    def __init__(self,master):
        super().__init__(master,bootstyle="primary")
        self.frame = ttk.Frame(self); self.frame.place(relx=0.5, rely=0.5, anchor="center")
        frame = ttk.Frame(self ,bootstyle="") ; frame.pack(side="right")
        # frame = ttk.Frame(frame ) ; frame.pack(padx=2,pady=2)
        # frame = self
        ttk.Label(frame,text=LoginPage.user_name).pack(side="left" , padx=4)
        ttk.Button(frame , text="", image="logout_icon",width=20, command=LoginPage.start).pack(side="left")
    ###############        ###############        ###############        ###############
    def create(self):
        self.frame.destroy()
        self.frame = ttk.Frame(self,bootstyle="primary"); self.frame.place(relx=0.5, rely=0.5, anchor="center")
        menu = {
            "مركبات 1"             : lambda : print("About clicked"),
            "مركبات 2"             : lambda : print("About clicked"),
        }
        for text,btn in menu.items():
                ttk.Button(self.frame,text=text,command=btn ,width=10 , bootstyle="primary").pack(side="left",pady=2,padx=20)

class LeftMenu():
    def create_menu(self,master):
        LeftMenu.frame=ttk.Frame(master,bootstyle="light")
        LeftMenu.frame.grid(row=1,column=0,sticky="nswe")
        # title
        LeftMenu.title = t = ttk.Label(LeftMenu.frame , text="القائمة") ; t.pack(side="top" ,pady= 20)
        ttk.Separator(LeftMenu.frame).pack(fill="x" , pady=10)
        # logo
        ttk.Label(LeftMenu.frame , image='logo' , text="" ).pack(side="bottom", pady=10)
        LeftMenu.options_frame = f = ttk.Frame(LeftMenu.frame , width=0); f.pack(fill="both")
    ###############        ###############        ###############        ###############
    def update_menu(self,menu_ls={}):
        LeftMenu.options_frame.destroy()
        LeftMenu.options_frame = f = ttk.Frame(LeftMenu.frame); f.pack(fill="both")
        for text,func in menu_ls.items():
            ttk.Button(f,text=text ,command=func,text_color="black"  ).pack(fill="x" , pady=2)
    ###############        ###############        ###############        ###############
    def update_title(self,title="Empty"):
        LeftMenu.title.config(text=title)