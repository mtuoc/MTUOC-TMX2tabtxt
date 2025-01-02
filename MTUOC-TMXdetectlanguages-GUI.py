#    MTUOC-TMXdetectlanguages-GUI
#    Copyright (C) 2025  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import xml.etree.ElementTree as ET
import sys
import codecs

from tkinter import *
from tkinter.ttk import *
import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext

def detectlanguages(fentrada):
    
    context = ET.iterparse(fentrada, events=("start", "end"))
    root = next(context)  # Get the root element
    sl_text = ""
    tl_text = ""
    langs={}
    for event, elem in context:
        if event == "end" and elem.tag == "tu":
            for tuv in elem.findall("tuv"):
                try:
                    lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                    langs[lang]=1        
                except:
                    pass
    for l in langs:
        print(l)
        TA1.insert(INSERT,l+"\n")
        
def select_TMX():
    infile = askopenfilename(initialdir = ".",filetypes =(("TMX files", ["*.tmx"]),("All Files","*.*")),title = "Choose an input TMX file.")
    E1.delete(0,END)
    E1.insert(0,infile)
    E1.xview_moveto(1)

def go():
    tmxfile=E1.get()
    detectlanguages(tmxfile)

top = Tk()
top.title("MTUOC-TMXdetectlanguages-GUI")

B1=tkinter.Button(top, text = str("Input file"), borderwidth = 1, command=select_TMX,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.grid(row=0,column=1)

TA1 = scrolledtext.ScrolledText(top, bd = 5,
                                      
                                      width = 36, 
                                      height = 5)
  
TA1.grid(row=1, column = 1, pady = 10, padx = 10)

B5=tkinter.Button(top, text = str("Go!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=1,column=0)

top.mainloop()

'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MTUOC program for detecting the language codes of a TMX file.')
    parser.add_argument('-i','--in', action="store", dest="inputfile", help='The input TMX file.',required=True)
    args = parser.parse_args()
    fentrada=args.inputfile
    detectlanguages(fentrada)
'''
