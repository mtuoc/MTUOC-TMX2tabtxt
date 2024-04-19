#    MTUOC-TMX2tabtxt-GUI
#    Copyright (C) 2023  Antoni Oliver
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
import lxml
import lxml.etree as ET
import sys
import codecs

import html
import re
from ftfy import fix_encoding

from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import ttk

def lreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)

def rreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' ends 'string'.
    """
    return re.sub('%s$' % pattern, sub, string)
    
def FT2ST(segment):
    segmenttagsimple=segment
    segmenttagsimple=re.sub('(<[^>]+?/>)', "<t/>",segmenttagsimple)
    segmenttagsimple=re.sub('(</[^>]+?>)', "</t>",segmenttagsimple)
    segmenttagsimple=re.sub('(<[^/>]+?>)', "<t>",segmenttagsimple)
    return(segmenttagsimple)
    
def FT2NT(segment):
    segmentnotags=re.sub('(<[^>]+>)', " ",segment)
    segmentnotags=' '.join(segmentnotags.split()).strip()
    return(segmentnotags)

def TMX2tabtxt():
    try:
    
        CBnotagsState=CBnotags.state()
        argsnoTags=False
        if "selected" in CBnotagsState:
            argsnoTags=True
        CBsimpletagsState=CBsimpletags.state()
        argssimpleTags=False
        if "selected" in CBsimpletagsState and not argsnoTags:
            argssimpleTags=True
        CBnoentitiesState=CBnoentities.state()
        argsnoEntities=False
        if "selected" in CBnoentitiesState:
            argsnoEntities=True
        CBfixencodingState=CBfixencoding.state()
        argsfixencoding=False
        if "selected" in CBfixencodingState:
            argsfixencoding=True   
        fentrada=E1.get()
        fsortida=E2.get()
        l1=E3.get().split(" ")
        l2=E4.get().split(" ")
    
        parser = ET.XMLParser(recover=True)
        tree = ET.parse(fentrada, parser=parser)
        root = tree.getroot()

        sortida=codecs.open(fsortida,"w",encoding="utf-8")

        for tu in root.iter('tu'):
            sl_text=""
            tl_text=""
            for tuv in tu.iter('tuv'):
                lang=tuv.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                for seg in tuv.iter('seg'):
                    try:
                        text=ET.tostring(seg).decode("'utf-8").strip()
                        text=lreplace("<seg>","",text)
                        text=rreplace("</seg>","",text)
                        if argsnoEntities:
                            text=html.unescape(text)
                        if argssimpleTags:
                            text=FT2ST(text)
                        if argsnoTags:
                            text=FT2NT(text)
                        if argsfixencoding:
                            text=fix_encoding(text)
                        if lang in l1: sl_text=text.replace("\n"," ")
                        elif lang in l2: tl_text=text.replace("\n"," ")
                    except:
                        print("ERROR",sys.exc_info())
                        sl_text=""
                        tl_text=""
            
                
            if not sl_text=="" and not tl_text=="":
                try:
                    cadena=sl_text+"\t"+tl_text
                    sortida.write(cadena+"\n")
                except:
                    pass
    except:
        print("ERROR:",sys.exc_info())
        pass
        
        
###

def select_corpus():
    infile = askopenfilename(initialdir = ".",filetypes =(("TMX files", ["*.tmx"]),("All Files","*.*")),title = "Choose a TMX input file.")
    E1.delete(0,END)
    E1.insert(0,infile)
    E1.xview_moveto(1)
    
def select_output_file():
    outfile = asksaveasfilename(initialdir = ".",filetypes =(("text files", ["*.txt"]),("All Files","*.*")),
                           title = "Choose a output file to store the term candidates.")
    E2.delete(0,END)
    E2.insert(0,outfile)
    E2.xview_moveto(1)
    
def go():
    TMX2tabtxt()


top = Tk()
top.title("MTUOC-TMX2tabtxt-GUI")

B1=tkinter.Button(top, text = str("Input file"), borderwidth = 1, command=select_corpus,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Output file"), borderwidth = 1, command=select_output_file,width=14).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E2.grid(row=1,column=1)

L1 = tkinter.Label( top, text="SL codes:")
L1.grid(row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=25, justify="left")
E3.grid(row=2,column=1,sticky="w")

L2 = tkinter.Label( top, text="TL codes:")
L2.grid(row=3,column=0)
E4 = tkinter.Entry(top, bd = 5, width=25, justify="left")
E4.grid(row=3,column=1,sticky="w")


CBnotags=ttk.Checkbutton(top, text="No tags")
CBnotags.state(['!alternate']) 
CBnotags.grid(sticky="W",row=4,column=0)
CBsimpletags=ttk.Checkbutton(top, text="Simple tags")
CBsimpletags.state(['!alternate']) 
CBsimpletags.grid(sticky="W",row=5,column=0)
CBnoentities=ttk.Checkbutton(top, text="No entities")
CBnoentities.state(['!alternate']) 
CBnoentities.grid(sticky="W",row=6,column=0)
CBfixencoding=ttk.Checkbutton(top, text="Fix encoding")
CBfixencoding.state(['!alternate']) 
CBfixencoding.grid(sticky="W",row=7,column=0)

B5=tkinter.Button(top, text = str("Go!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=8,column=0)

top.mainloop()
