from config import *
from LoginPage import LoginPage
from VehiclePage import VehiclePage

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
            "المركبات"           : VehiclePage,
            "إعدادات"            : lambda : print("About clicked"),
            "عن البرنامج"        : lambda : print("About clicked"),
        }
        for text,btn in menu.items():
                ttk.Button(self.frame,text=text,command=btn ,width=10 , bootstyle="primary").pack(side="right",pady=2,padx=20)