import os
import cx_Freeze
from cx_Freeze import Executable

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'
executables = [cx_Freeze.Executable("gamemanager.py")]
#create an executable file
cx_Freeze.setup(
    name="Risk",
    discription="Risk with a bot-player",
    options={"build_exe": {"packages": ["pygame", "os", "sys", "csv", "random"],
                           "include_files": ['data/', 'GUI/']}},
    executables=[Executable(script=r"gamemanager.py",
                            icon=".\\data\\icons\\Risk-icon2.ico",
                            targetName="Risk.exe")]
)
