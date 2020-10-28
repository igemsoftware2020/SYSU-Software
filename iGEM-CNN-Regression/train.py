
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
batch_size = 200
transform = transforms.Compose([transforms.ToTensor()])

train_data = DatasetFromCSV(r'H:\train_data\DNA\code\data_process\train_file.csv', transform)
test_data = DatasetFromCSV(r'H:\train_data\DNA\code\data_process\test_file.csv', transform)

train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size,drop_last=False)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size,drop_last=False)


net = MyNet().to(torch.device('cuda:0'))
net.load_state_dict(torch.load('model.pth'))
print(net)
loss_fn=MSELoss()
optimizer=torch.optim.Adam(net.parameters(),lr=1e-4)

start = 55
epochs = 300
min_loss = 100000
for epoch in range(start,epochs):
    train_loss=[]
    train_acc=[]
    print('epoch: '+str(epoch)+'/'+str(epochs))
    for data_X, data_tf,data_y in tqdm(train_loader):
        trainData,trainTF,trainLabel=Variable(data_X.cuda()),Variable(data_tf.cuda()),Variable(data_y.cuda())
        out=net(trainData.type(torch.cuda.FloatTensor),trainTF.cuda().type(torch.cuda.FloatTensor))

        loss=loss_fn(out,data_y.type(torch.cuda.FloatTensor))
        train_loss.append(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        acc = np.sum((out.data.cpu().numpy() - data_y.data.cpu().numpy()) ** 2) / len(data_y.data.cpu().numpy())
        train_acc.append(acc)
    mean_loss = np.array(train_loss).mean()
    mean_acc = np.array(train_acc).mean()
    print('Train Loss:%.5f mse: %.5f' % (mean_loss,mean_acc))
    if mean_loss < min_loss:
        min_loss = mean_loss
        print("save model ",mean_loss)
        torch.save(net.state_dict(), './model.pth')

