import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.style import Bootstyle
from tkinter.filedialog import askdirectory , asksaveasfilename 
from ttkbootstrap.dialogs import Messagebox 
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from tksheet import Sheet
from PIL import Image, ImageTk

from pathlib import Path

import openpyxl
import csv 

import tempfile, os ,sys
import base64
from io import BytesIO

import sqlite3 ,re

from cryptography.fernet import Fernet

v_keys_en = ("plate_no"         , "model"               , "vehicle_type"    , "brand"               , "color"               , 
            "registration_type" , "serial_no"           ,"chassis_no"       ,"beneficiary_entity"   , "registered_under_custody", 
            "actual_user"       , "national_id"         ,"owner"            , "owner_id"            , "insurance_status" , 
            "insurance_start"   , "insurance_end"       , "file_no"         ,"spare_no"             , "vehicle_status"    
            ,"notes"  )
v_keys_ar = ("رقم اللوحة"       , "الموديل"          , "نوع المركبة"    , "الماركة"         , "اللون",
            "نوع التسجيل"      , "الرقم التسلسلي"   , "رقم الهيكل"      , "الجهة المستفيدة", "مسجلة بعهدة",
            "المستخدم الفعلي"  , "رقم الهوية"       , "المالك"          , "هوية المالك"     , "حالة الضمان"     , 
            "بداية الضمان"      , "نهاية الضمان"    , "رقم الملف"       ,"رقم الاسبير"       ,"حالة المركبة"     
            , "ملاحظات"            )