#    MTUOC-TMX2tabtxtDIR
#    Copyright (C) 2024  Antoni Oliver
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
import os

import html
import re
from ftfy import fix_encoding

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

def TMX2tabtxtDIR(direntrada, fsortida, l1, l2):
    sortida=codecs.open(fsortida,"w",encoding="utf-8")
    parser = ET.XMLParser(recover=True)
    for root, dirs, files in os.walk(direntrada):
        for file in files:
            if file.endswith(".tmx"):
                try:
                    fentrada=os.path.join(root, file)
                    print(fentrada)
                    
                    tree = ET.parse(fentrada, parser=parser)
                    rootT = tree.getroot()


                    for tu in rootT.iter('tu'):
                        sl_text=""
                        tl_text=""
                        for tuv in tu.iter('tuv'):
                            try:
                                lang=tuv.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                            except:
                                lang=tuv.attrib['lang']
                            for seg in tuv.iter('seg'):
                                try:
                                    text=ET.tostring(seg).decode("'utf-8").strip()
                                    text=lreplace("<seg>","",text)
                                    text=rreplace("</seg>","",text)
                                    if args.noEntities:
                                        text=html.unescape(text)
                                    if args.simpleTags:
                                        text=FT2ST(text)
                                    if args.noTags:
                                        text=FT2NT(text)
                                    if args.fixencoding:
                                        text=fix_encoding(text)
                                    if lang in l1: sl_text=text.replace("\n"," ")
                                    elif lang in l2: tl_text=text.replace("\n"," ")
                                except:
                                    sl_text=""
                                    tl_text=""
                        
                            
                        if not sl_text=="" and not tl_text=="":
                            try:
                                cadena=sl_text+"\t"+tl_text
                                sortida.write(cadena+"\n")
                            except:
                                pass
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
    TMX2tabtxtDIR(direntrada, fsortida, l1, l2)


