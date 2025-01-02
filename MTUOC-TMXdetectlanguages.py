#    MTUOC-TMXdetectlanguages
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MTUOC program for detecting the language codes of a TMX file.')
    parser.add_argument('-i','--in', action="store", dest="inputfile", help='The input TMX file.',required=True)
    args = parser.parse_args()
    fentrada=args.inputfile
    detectlanguages(fentrada)

