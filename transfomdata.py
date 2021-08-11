import os
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw
from shutil import move
import xml.etree.ElementTree as ET  
from random import shuffle

#写好模板，里面的%s与%d  后面文件输入输出流改变   -------转数据集阶段--------
headstr = """        
<annotation>
    <folder>VOC</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = '''
</annotation>
'''

def write_xml(anno_path, head, objs, tail):  #把提取的数据写入到相应模板的地方 
    f = open(anno_path, "w")
    f.write(head)
    for obj in objs:
        f.write(objstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
    f.write(tail)

def input_data(path,origin):
    with open(origin,'r') as f:
        text = f.read()
        root = ET.fromstring(text)
        filename = root.find("filename").text
        width = int(root.find("size").find("width").text)
        height = int(root.find("size").find("height").text)
        depth = int(root.find("size").find("depth").text)
        objects = []
        for obj in root.iter("object"):
            obname = obj.find("name").text
            obxmin = int(obj.find("bndbox").find("xmin").text);
            obymin = int(obj.find("bndbox").find("ymin").text);
            obxmax = int(obj.find("bndbox").find("xmax").text);
            obymax = int(obj.find("bndbox").find("ymax").text);
            objects.append([obname,obxmin,obymin,obxmax,obymax])
        head = headstr%(filename,width,height,depth)
        tail = tailstr
        fs = open(path,"w")
        fs.write(head)
        for obj in objects:
            fs.write(objstr%(obj[0],obj[1], obj[2], obj[3], obj[4]))
        fs.write(tail)
        fs.close()
        
save_xml = "/home/aistudio/work/Pears/Annotations/"
save_img = "/home/aistudio/work/Pears/JPEGImages/"

data_path= "/home/aistudio/datasets/"
index = 0
print(data_path)
for dira in tqdm(os.listdir(data_path)):
    path = data_path+dira
    if dira == "昆虫编号.xlsx":
        os.system(f"mv {path} work/PearsDetection/{dira}")
        continue
    for a in os.listdir(path):
        path_second = f"{path}/{a}/"
        path_xml = path_second+"Annotations/"
        path_img = path_second+"JPEGImages/"
        name_key = {}
        for name in os.listdir(path_xml):
            index+=1
            name_key[name.split('.')[0]] = index
            input_data(f"{save_xml}{index}.xml",path_xml+name)
        for name in os.listdir(path_img):
            temp = cv2.imread(f"{path_img}{name}",-1)
            cv2.imwrite(f"{save_img}{name_key[name.split('.')[0]]}.jpg",temp)
