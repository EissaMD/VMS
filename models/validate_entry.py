from config import *

def validate_entry(entry_dict={},popup_msg=True):
    failed_ls = []
    for key, value in entry_dict.items():
        key = key.lower()
        # check text
        if key in ("نوع المركبة","اللون","التصنيف" ,"نوع التسجيل" ,"الرقم التسلسلي" ,"رقم الهيكل","الجهة المستفيدة" ,"مسجلة بعهدة","المستخدم الفعلي","رقم اللوحة"):
            if not value or not isinstance(value, str):
                failed_ls.append(key)
                continue
        # check float
        if key in (1,):
            try:
                test=float(value)
            except:
                failed_ls.append(key)
        # check integer
        if key in ("الموديل" ,"رقم الهوية"):
            try:
                test=int(value)
            except:
                failed_ls.append(key)
        # check quantity
        if key in (1,):
            try:
                if int(value) <1:
                    raise Exception
            except:
                failed_ls.append(key)
        # check date entry
        if key in (1,):
            try:
                if value != "":
                    test = datetime.strptime(value, r"%Y-%m-%d")
            except:
                failed_ls.append(key)
        # check email
        if key in ("email",'email_address'):
            regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(regex, value):
                failed_ls.append(key)
    if popup_msg is True and len(failed_ls)>0:
        error_text = f"الإدخال غير صحيح، يُرجى التحقق من البيانات والمحاولة مرة أخرى.\nالمدخلات التالية تحتاج للمراجعة: {str(failed_ls)}"
        Messagebox.show_error(error_text)
    return failed_ls