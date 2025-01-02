#    MTUOC-TMX2tabtxtDIR
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
import sys
import codecs
import os

import html
import re
from ftfy import fix_encoding

import xml.etree.ElementTree as ET


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

def TMX2tabtxt(fentrada,fsortida,l1,l2,noTags=False,simpleTags=False,noEntities=False,fixencoding=False):
    try:
        sortida = codecs.open(fsortida, "a", encoding="utf-8")
        
        # Iteratively parse the XML file
        context = ET.iterparse(fentrada, events=("start", "end"))
        _, root = next(context)  # Get the root element

        sl_text = ""
        tl_text = ""
        
        for event, elem in context:
            if event == "end" and elem.tag == "tu":
                sl_text = ""
                tl_text = ""

                for tuv in elem.findall("tuv"):
                    try:
                        lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', 
                                              tuv.attrib.get('lang', ''))
                        for seg in tuv.findall("seg"):
                            text = ET.tostring(seg, encoding="unicode").strip()
                            text = text.replace("<seg>", "").replace("</seg>", "")

                            if noEntities:
                                text = html.unescape(text)
                            if simpleTags:
                                text = FT2ST(text)
                            if noTags:
                                text = FT2NT(text)
                            if fixencoding:
                                text = fix_encoding(text)

                            if lang in l1:
                                sl_text = text.replace("\n", " ")
                            elif lang in l2:
                                tl_text = text.replace("\n", " ")

                    except Exception as e:
                        print("ERROR processing tuv/seg:", e, sys.exc_info())
                        sl_text = ""
                        tl_text = ""

                if sl_text and tl_text:
                    try:
                        cadena = f"{sl_text}\t{tl_text}"
                        sortida.write(cadena + "\n")
                    except Exception as e:
                        print("ERROR writing line:", e, sys.exc_info())

                # Clear the element to free up memory
                root.clear()

        sortida.close()
    except Exception as e:
        print("ERROR processing file:", e, sys.exc_info())

def TMX2tabtxtDIR(direntrada, fsortida, l1, l2,noTags,simpleTags,noEntities,fixencoding):
    sortida=codecs.open(fsortida,"w",encoding="utf-8")
    for root, dirs, files in os.walk(direntrada):
        for file in files:
            if file.endswith(".tmx"):
                try:
                    fentrada=os.path.join(root, file)
                    print(fentrada)
                    TMX2tabtxt(fentrada,fsortida,l1,l2,noTags=False,simpleTags=False,noEntities=False,fixencoding=False)
                except:
                    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MTUOC program for converting all the TMX files in a given directory into a tab text.')
    parser.add_argument('-d','--dir', action="store", dest="inputdir", help='The input directory where the TMX files are located.',required=True)
    parser.add_argument('-o','--out', action="store", dest="outputfile", help='The output text file.',required=True)
    parser.add_argument('-s','--sl', nargs='+', action="store", dest="slcode", help='The codes for the source language.',required=True)
    parser.add_argument('-t','--tl', nargs='+', action="store", dest="tlcode", help='The codes for the target language.',required=True)
    parser.add_argument('--noTags', action='store_true', default=False, dest='noTags',help='Removes the internal tags.')
    parser.add_argument('--simpleTags', action='store_true', default=False, dest='simpleTags',help='Replaces tags with <t>, </t> or <t/>.')
    parser.add_argument('--noEntities', action='store_true', default=False, dest='noEntities',help='Replaces html/xml entities by corresponding characters.')
    parser.add_argument('--fixencoding', action='store_true', default=False, dest='fixencoding',help='Tries to restore errors in encoding.')

    args = parser.parse_args()
    direntrada=args.inputdir
    fsortida=args.outputfile
    l1=args.slcode
    l2=args.tlcode
    noTags=args.noTags
    simpleTags=args.simpleTags
    noEntities=args.noEntities
    fixencoding=args.fixencoding
    TMX2tabtxtDIR(direntrada, fsortida, l1, l2,noTags,simpleTags,noEntities,fixencoding)


