import torch
from torch.autograd import Variable
from torch.nn import Conv2d,Module,Sequential,ReLU,MaxPool2d,Linear,Dropout,Softmax,CrossEntropyLoss
from torch.utils.data import DataLoader,TensorDataset
import os
import numpy as np
import struct
from tqdm import tqdm
class Concat(torch.nn.Module):
    def __init__(self, dimension=0):
        super(Concat, self).__init__()
        self.d = dimension

    def forward(self, x):
        return torch.cat(x, self.d)

class MyNet(Module):
    def __init__(self):
        super(MyNet,self).__init__()
        self.conv1=Sequential(Conv2d(in_channels=1,out_channels=96,kernel_size=11,stride=4,padding=0),
                              ReLU(),
                              MaxPool2d(kernel_size=(6,3),stride=(6,2),padding=0))
        self.conv2=Sequential(Conv2d(in_channels=96,out_channels=256,kernel_size=5,stride=1,padding=2),
                              ReLU(),
                              MaxPool2d(kernel_size=(7,3),stride=(6,2),padding=0))
        self.conv3=Sequential(Conv2d(in_channels=256,out_channels=384,kernel_size=3,stride=1,padding=1),
                              ReLU())
        self.conv4 = Sequential(Conv2d(in_channels=384, out_channels=50, kernel_size=3, stride=1, padding=1),
                                ReLU())
        self.fc1=Sequential(Linear(in_features=1300, out_features=4160),
                           ReLU(),
                           Dropout(0.2),
                           Linear(in_features=4160,out_features=698),
                           ReLU(),
                           Dropout(0.2))
        self.fc2 = Linear(in_features=698*2, out_features=100)
        self.concat = Concat(dimension=1)
        self.output = Linear(in_features=100, out_features=1)

    def forward(self, x,tf_feature):
        out_conv1=self.conv1(x)
        out_conv2=self.conv2(out_conv1)
        out_conv3=self.conv3(out_conv2)
        out_conv4=self.conv4(out_conv3)
        out_conv4=out_conv4.view([-1,1300])
        out_fc1=self.fc1(out_conv4)
        out_tf = self.concat((out_fc1,tf_feature))
        out_fc2 = self.fc2(out_tf)
        out = self.output(out_fc2)
        return out