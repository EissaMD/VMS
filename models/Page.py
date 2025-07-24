from config import *

class Page():
    c = {
        "bg": "default",
        "body_bg": "default",
    }
    def init_page(master):
        c= Page.c
        Page.main_window = master
        Page.page = ttk.Frame(master)
        Page.page.grid(row=1,column=0,sticky="nswe" , padx=10,pady=10)
        Page.frame = f = ttk.Frame(Page.page); f.pack(fill="both",expand=True)
    ###############        ###############        ###############        ###############
    def create_new_page(title="",options=[],scrolled=False):
        c= Page.c
        # Page
        Page.frame.destroy()
        Page.frame = f = ttk.Frame(Page.page); f.pack(fill="both",expand=True)
        # header
        if title:
            header = ttk.Frame(f) ; header.pack(fill="x" , side="top")
            ttk.Label(header,font=("Times", 25 ,"bold"),text=title).pack(fill="x" ,side="right",pady=2 )
        if options:
            icon_frame = ttk.Frame(header); icon_frame.pack(side="left")
            for icon_name, tooltip, func in options:
                btn = ttk.Button(icon_frame, image=icon_name, bootstyle="light", command=func)
                btn.pack(side="left", padx=5)
                ToolTip(btn, text=tooltip)
        # body
        Page.body_container = bc = ttk.Frame(f ) ; bc.pack(fill="both", expand=True)
        if not scrolled:
            return bc
        Page.body = b = ScrolledFrame(bc,autohide=True ) ; b.pack(fill="both", expand=True)
        return b
    ###############        ###############        ###############        ###############
    def option_clicked(choice):
        Page.options[choice]()
    ###############        ###############        ###############        ###############
    def create_new_body(scrolled=False):
        c= Page.c
        Page.body_container.destroy()
        Page.body_container = bc = ttk.Frame(Page.frame ) ; bc.pack(fill="both", expand=True)
        if not scrolled:
            return bc
        Page.body = b = ScrolledFrame(bc,autohide=True ) ; b.pack(fill="both", expand=True)
        return b
    ###############        ###############        ###############        ###############
    def create_footer(footer_btn=lambda :0 , text_btn="Confirm"):
        body = Page.body
        # footer_btn = lambda : messagebox.showinfo("Info","The process was successful!")
        Page.footer = ttk.Frame(body ,corner_radius=0) ; Page.footer.pack(fill="x" , side="bottom")
        if isinstance(text_btn,list):
            for func , text in zip(footer_btn,text_btn):
                ttk.Button(Page.footer,text=text ,command=func,border_width=0).pack(side="right",padx=2,pady=2) 
        else:
            ttk.Button(Page.footer,text=text_btn ,command=footer_btn,border_width=0,).pack(side="right",padx=2,pady=2)
##############################################################################################################