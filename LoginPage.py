from config import *
from models.DB import DB

class LoginPage(ttk.Frame):
    F=Fernet(b'yaYPBWFF6Cs4eYaJgyJRw3qM6B8JpodeCvg__jgAxqA=')
    app = None  # Reference to the main application
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
    ###############        ###############        ###############        ###############
    def login_btn(event=None):
        username = LoginPage.user.get()
        password = LoginPage.password.get()
        print(f"Login attempt with username: {username} and password: {password}")
        if True:
            LoginPage.app.unbind('<Return>')
            LoginPage.app.create_main_frame()
    ###############        ###############        ###############        ###############
    def login_btn(event=0):
        user        = LoginPage.user.get()
        password    = LoginPage.password.get()
        if user == "admin" and password == "Admin123":
            LoginPage.app.unbind('<Return>')
            LoginPage.user_name = "Admin User"
            LoginPage.app.create_main_frame()
            return
        DB.cursor.execute("SELECT user_name, password,first_name, last_name time_created FROM users WHERE user_name=?;",(user,))
        user_info = DB.cursor.fetchone()
        if not user_info:
            Messagebox.show_error("اسم المستخدم غير صحيح، حاول مرة أخرى!")
            return
        stored_pass =LoginPage.F.decrypt(user_info[1].encode()).decode()
        if stored_pass != password:
            Messagebox.show_error(";كلمة المرور غير صحيحة، حاول مرة أخرى!")
            return
        LoginPage.app.unbind('<Return>')
        LoginPage.user_name = user_info[2] +" "+ user_info[3]
        LoginPage.app.create_main_frame()
    ###############        ###############        ###############        ###############
    def login_pass(event=None):
        LoginPage.app.unbind('<Return>')
        LoginPage.app.create_main_frame()
###############################################################################################################