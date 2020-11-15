
import numpy as np
import pandas as pd
from PIL import Image
import torch
from torch import optim, nn
import torch.nn.functional as F
from torchvision import transforms
from torch.utils.data.dataset import Dataset


class DatasetFromCSV(Dataset):
    def __init__(self, csv_path,transforms=None):
        self.data = pd.read_csv(csv_path)
        self.maxlen = np.max(self.data["dna"].str.len()) # test: 3823   ,train :66783
        print(self.maxlen)
        self.transforms = transforms
        self.data_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                      'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                      'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                      'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                      'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                      'y', 'z']
        with open(r"/home/mist/iGEM-CNN-Regression/data_process/tf_txt.txt", "r") as f:
            self.all_tf_txt = [file.strip() for file in f.readlines()]
    def to_categorical(self,y, num_classes=52):
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

    def __getitem__(self, index):
        current = self.data.iloc[index]
        single_label = current[2]
        DNA_IMG = np.zeros((66783,len(self.data_index)))
        DNA = current[1]
        for i,char in enumerate(DNA):
            DNA_IMG[i] = self.to_categorical(self.data_index.index(char),num_classes=len(self.data_index))
        TF = self.to_categorical(self.all_tf_txt.index(current[0]),num_classes=len(self.all_tf_txt))
        DNA_IMG = np.array(DNA_IMG)
        img_as_img = Image.fromarray(DNA_IMG)
        img_as_img = img_as_img.resize((52,2000))
        img_as_tensor = img_as_img.convert('L')
        if self.transforms is not None:
             img_as_tensor = self.transforms(img_as_tensor)
        return (img_as_tensor, TF,single_label)

    def __len__(self):
        return len(self.data)

# batch_size = 64
# transform = transforms.Compose([transforms.ToTensor(),
#                                 transforms.Normalize((0.5,), (0.5,))])
#
# train_data = DatasetFromCSV('./test_file.csv', transform)
# #test_data = DatasetFromCSV("./train_file.csv", transform)
#
# #train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size)
# test_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size)
#
# img, tf,lab = next(iter(test_loader))
# #print(img.shape)
