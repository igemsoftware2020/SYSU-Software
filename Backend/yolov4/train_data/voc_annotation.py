import xml.etree.ElementTree as ET
from os import getcwd
from train_data.data_config import get_train_data
import glob
import os
import numpy as np

classes =['PRO','Promoter','promoter']
def convert_annotation(file, list_file):
    in_file = open(file,encoding="utf-8")
    tree=ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes :
            continue
        #cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(0))


all_file = []
for root, dirs, files in os.walk(get_train_data()):
    for file in files:
        if file.endswith(".xml"):
            all_file.append(root+"/"+file)


tmp = open('tmp.txt', 'w')
for file in all_file:
    image_id = str(file).split("/")[-1].strip().split(".")[0]
    fold = str(file).split("\\")[0].strip().split("/")[-2]
    tmp.write(file.replace(".xml",".jpg"))
    convert_annotation(file, tmp)
    tmp.write('\n')

tmp.close()
ass =[]
k = 0
train = open('train1.txt', 'w')
test = open('test1.txt', 'w')
with open("tmp.txt",'r') as f:
    ass = f.readlines()
    np.random.shuffle(ass)
    for file in ass:
        if k<5:
            test.write(file)
        else:
            train.write(file)
        k+=1
train.close()
test.close()
os.remove("tmp.txt")



