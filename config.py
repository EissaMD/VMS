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

import csv 
import tempfile, os
import base64
from io import BytesIO

import sqlite3 ,re