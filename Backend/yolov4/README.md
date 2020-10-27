# YoloV4_Promoter
This is for identifying the promoter inside the genetic path.


1. 配置
    pip install tensorflow==1.14.0 keras opencv-python Pillow matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple

2. 训练数据
    解压缩整理的数据到特定文件夹（不包含中文路径）
    2.1 修改 train_data/data_config.py中的 get_train_parent ，为上述路径
    2.2 运行 voc_annotation.py 生成训练数据需要的文件：train.txt test.txt。
    2.3 训练前需要修改model_data里面的voc_classes.txt文件，需要将classes改成你自己的classes
    2.4 运行train.py开始训练


3. 测试
    3.1 运行 predict.py 输出结果在img_out文件夹中
        注：如果使用第2步自己训练的模型进行预测，需要修改yolo.py中的model_path 为 logs/目录下的.h5文件

4. 数据位置
    数据位于all_data