#coding:utf-8
import codecs
import json
from lxml import etree
lines=[]
file=codecs.open('quan_prov_city_area.txt',encoding='utf-8')
for line in file:
    lines.append(line.split('\t')[1])
file.close()

root=etree.Element('root')
lay1cell=None
lay2cell=None
for one in lines:
    spacecount=0
    for c in one:
        if c==' ':
            spacecount+=1
        else:
            break
    if spacecount==0:
        lay1cell=etree.Element('p')
        lay1cell.text=one.strip()
        root.append(lay1cell)
    elif spacecount==4:
        lay2cell=etree.Element('c')
        lay2cell.text=one.strip()
        lay1cell.append(lay2cell)
    elif spacecount==8:
        cell=etree.Element('z')
        cell.text=one.strip()
        lay2cell.append(cell)
file=open('china_prov_city_area.xml','w')
file.write(etree.tostring(root,encoding='utf-8',xml_declaration=True))
file.close()