import pandas as pd
import numpy as np
csv_data = pd.read_csv('all_tf.csv')  # 读取训练数据
result =csv_data.drop_duplicates(subset=None, keep='first', inplace=False)
with open ("tf_txt.txt","w") as f:
    for index in range(0,result.shape[0]):
        f.write(str(result.iloc[index][0])+"\n")
