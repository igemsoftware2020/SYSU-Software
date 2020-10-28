import os
from glob import glob
import csv
import numpy as np

root_path = r"H:\train_data\DNA"
folde=["jiaomu_result","Rattus_norvegicus_result"]
all_file = []
for root, dirs, files in os.walk(root_path):
    for dir in dirs:
        if dir not in folde:
            continue
    all_file += glob(os.path.join(root,dir,"*.txt"))

for root, dirs, files in os.walk(os.path.join(root_path,"Chip_result")):
    for dir in dirs:
        all_file += glob(os.path.join(root,dir,"*.txt"))


train_file = open("train_file.csv", "w", newline='')
writer_train = csv.writer(train_file)
writer_train.writerow((str("tf"),"dna","score"))

test_file = open("test_file.csv", "w", newline='')
writer_test = csv.writer(test_file)
writer_test.writerow((str("tf"),"dna","score"))

tf_file = open("all_tf.csv", "w", newline='')
writer_tf = csv.writer(tf_file)
writer_tf.writerow((str("tf"),))

k = 0
index = 0
for file in all_file:
    print("current file: " ,k,len(all_file))
    k+=1
    with open(file,"r") as ff:
        for line in ff.readlines()[:30]:
            if len(line.split("\t")) != 4:
                continue
            index +=1
            writer_tf.writerow((str(line.split("\t")[1]),))
            if index % 20 == 0:
                writer_test.writerow((str(line.split("\t")[1]),line.split("\t")[2],line.split("\t")[3].strip()))
            else:
                writer_train.writerow((str(line.split("\t")[1]), line.split("\t")[2], line.split("\t")[3].strip()))
