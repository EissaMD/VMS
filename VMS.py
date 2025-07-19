from config import *
from LoginPage import LoginPage
from MainMenu import MainMenu     
from models import Page , RightMenu , DB

class App(ttk.Window):
    WIDTH = 1280
    HEIGHT = 720
    def __init__(self):
        super().__init__(themename="minty") 
        self.title("إدارة المركبات")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.main_frame = ttk.Frame(self)
        ################## IMAGES #################
        image_files = (     ('logo'                 ,   'logo.png'          ,120   ,100                 ),
                            ('user_icon'            ,   'user_icon.png'     ,120   ,100                 ),
                            ('background'           ,   'background.png'    ,App.WIDTH    ,App.HEIGHT   ),
                            ('logout_icon'          ,   'logout.png'        ,20    ,20                  ),
                            ('login_icon'           ,   'login.png'         ,40    ,40                  ),
                            ('save_icon'            ,   'save.png'          ,20    ,20                  ),
                            ('reset_icon'           ,   'reset.png'         ,20    ,20                  ),
                            ('copy_data_icon'       ,   'copy_data.png'     ,20    ,20                  ),
                            ('search_icon'          ,   'search_icon.png'   ,20    ,20                  ),
            )
        self.photoimages = []
        for name, file_name ,w ,h in image_files:
            path = r"./assets/" + file_name 
            img =Image.open(path).resize((w,h))
            self.photoimages.append(ImageTk.PhotoImage(img ,name=name))
            if name == "logo":
                self.iconphoto(False, self.photoimages[-1])
        ################## IMAGES #################
        DB.connect("VMS.db")
        LoginPage.app = self
        LoginPage.start()
        LoginPage.login_pass()
    ###############        ###############        ###############        ###############
    def create_empty_frame(self):
        self.main_frame.destroy()
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both",expand=True)
        return self.main_frame
    ###############        ###############        ###############        ###############
    def create_main_frame(self):
        self.create_empty_frame()
        # create the main menu
        self.main_frame.columnconfigure((0),weight=1)
        main_menu = MainMenu(self.main_frame)
        main_menu.grid(row=0,column=0, columnspan=2, sticky="nswe" )
        main_menu.create()
        # create secondary menu
        self.main_frame.rowconfigure((1),weight=1)
        self.main_frame.columnconfigure((1),minsize=160)
        RightMenu().create_menu(self.main_frame)
        # create Body Frame
        Page.init_page(self.main_frame)
        bodyframe = Page.create_new_page("- - -")
        frame = ttk.Frame(bodyframe)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(frame, text="مرحباً بك في نظام إدارة المركبات", font=("Arial", 20)).pack()
        ttk.Label(frame, text="للبدء في استخدام النظام يرجى اختيار من القائمة العلوية", font=("Arial", 16)).pack()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
