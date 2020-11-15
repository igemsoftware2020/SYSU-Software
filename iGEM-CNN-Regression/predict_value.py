
import numpy as np
import pandas as pd
from PIL import Image
import torch
from torch import optim, nn
import torch.nn.functional as F
from torchvision import transforms
from torch.utils.data.dataset import Dataset
from data_process.read_data import DatasetFromCSV
import torch
from torch.autograd import Variable
from torch.nn import Conv2d,Module,Sequential,ReLU,MaxPool2d,Linear,Dropout,Softmax,MSELoss
from torch.utils.data import DataLoader,TensorDataset
import os
import numpy as np
import struct
from tqdm import tqdm
from model.mdel import MyNet
import matplotlib.pyplot as plt
transform = transforms.Compose([transforms.ToTensor()])
batch_size = 1


def to_categorical(y, num_classes=52):
    y = np.array(y)
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes))
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical


with open(r"H:\train_data\DNA\code\data_process\tf_txt.txt", "r") as f:
    all_tf_txt = [file.strip() for file in f.readlines()]
data_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                      'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                      'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                      'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                      'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                      'y', 'z']
DNA_IMG = np.zeros((66783,len(data_index)))
DNA = ""
TF= ""
for i,char in enumerate(DNA):
    DNA_IMG[i] = to_categorical(data_index.index(char),num_classes=len(data_index))
TF = to_categorical(all_tf_txt.index(TF),num_classes=len(all_tf_txt))
DNA_IMG = np.array(DNA_IMG)
img_as_img = Image.fromarray(DNA_IMG)
img_as_img = img_as_img.resize((52,2000))
img_as_tensor = img_as_img.convert('L')

net = MyNet()
net.load_state_dict(torch.load('model.pth'))
list_output = []
list_real = []
trainData, trainTF = Variable(torch.from_numpy(img_as_tensor)), Variable(torch.from_numpy(TF))
output = net(trainData.type(torch.FloatTensor), trainTF.cuda().type(torch.FloatTensor))
print("predict_ reuslt : " ,output.data.cpu().numpy()[-1][0])
