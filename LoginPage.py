from config import *

class LoginPage(ttk.Frame):
    app = None  # Reference to the main application
    logged_in = False
    def start():
        LoginPage.user_name = "No USER"
        LoginPage.department = "local"
        main_frame = LoginPage.app.create_empty_frame()
        background = ttk.Label(main_frame, text="" ,image='background'); background.pack()
        background.bind('<Return>', LoginPage.login_btn)
        frame = ttk.Frame(main_frame ) ; frame.place(relx=0.28, rely=0.85, anchor="center")
        # ttk.Label(frame , image='user_icon' , text="" ).pack( pady=10,side="left")
        # input frame
        input_frame = ttk.Frame(master=frame )
        input_frame.pack(side="left")
        # user name
        ttk.Label(master=input_frame, text=" : اسم الستخدم " , width = 20).grid(row=0, column=2 )
        LoginPage.user = ttk.Entry(master=input_frame , width = 50 )
        LoginPage.user.grid(row=0, column=1)
        # password
        ttk.Label(master=input_frame, text=" : كلمة المرور" , width = 20).grid(row=1, column=2 , pady=(10,0) )
        LoginPage.password = ttk.Entry(master=input_frame , show="*" ,  width = 50 )
        LoginPage.password.grid(row=1, column=1 , pady=(10,0))
        # Define new style based on existing TLabel
        ttk.Button(input_frame,text="تسجيل الدخول" , width=30 , command=LoginPage.login_btn ,image='login_icon').grid(row=0, column=0,rowspan=2 ,sticky="ns" , padx=5)
        LoginPage.app.bind('<Return>', LoginPage.login_btn)
        LoginPage.logged_in = False
    ###############        ###############        ###############        ###############
    def login_btn(event=None):
        if LoginPage.logged_in:
            return
        username = LoginPage.user.get()
        password = LoginPage.password.get()
        print(f"Login attempt with username: {username} and password: {password}")
        LoginPage.app.create_main_frame()
        LoginPage.logged_in = True
###############################################################################################################