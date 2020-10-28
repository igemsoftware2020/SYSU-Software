# Maloadis
http://maloadis.sysu-software.com

## Environment
- OS: Ubuntu 18.04
- SDKs & Softwares: MySQL 8.0.22, Python 3.7, .NET 5 RC2 SDK, gcc-10, g++-10
- Important Notes: Please make sure your MySQL installation has a user named `root` with no password.

## Install Packages
```bash
sudo apt install libboost-dev libboost-all-dev libmysqlcppconn-dev libjsoncpp-dev cmake git build-essential
python -m pip install keras==2.3.1 tensorflow==1.15.4 opencv-python Pillow matplotlib numpy==1.18.5 flask flask-cors mysql-connector-python Bayesian-Optimization scikit-learn==0.22.2 sh pySBOL fuzzywuzzy scipy 
```

## Build Software
```bash
cd Search/roadmapSearch
mkdir build && cd build
cmake .. -DCMAKE_CXX_FLAGS=-std=c++2a
make -j8

cd ../GenenetSearch
mkdir build && cd build
cmake .. -DCMAKE_CXX_FLAGS=-std=c++2a
make -j8
cp genenet_search ../../Backend/genenet/search
```

## Import Database
```bash
cd Database/genenetDB
unzip genenetDB-dumps.zip
mysql -u root < genenetDB-dumps.sql

cd ../
unzip roadmapDB-dumps.zip
mysql -u root < roadmapDB-dumps.sql
```

## Run Server
### Run Backend
```bash
cd Backend
dotnet run -c Release --urls http://0.0.0.0:5000
```

### Run Search Service
```bash
cd Search/SearchAPI/src
python app.py
```

### Run Object Detection Service
```bash
cd Backend/yolov4
python predict.py
```

### Configure Designer
In `Designer/src/config.ts`, please replace the following lines with your actual server http address:
```typescript
const Config = {
    searchUri: '<your server http address>:5001',
    regonUri: '<your server http address>:5000'
};

export default Config;
```

Assuming your server address is `http://123.123.123.123`, you should modify the file to:
```typescript
const Config = {
    searchUri: 'http://123.123.123.123:5001',
    regonUri: 'http://123.123.123.123:5000'
};

export default Config;
```

If you are doing above things on your local computer, you can use `http://localhost` as your server http address hence your config file should be:
```typescript
const Config = {
    searchUri: 'http://localhost:5001',
    regonUri: 'http://localhost:5000'
};

export default Config;
```

### Run Designer
```bash
cd Designer
yarn
yarn start
```

Congratulations! Now you are ready to go, to use the software, you can access `http://localhost:3000`.

## iGEM-CNN-Regression: Deep Learning: TF & Binding Sites Affinity Prediction.
Make prediction within one line!

```bash
python predict.py YOUR_TF YOUR_DNA
```

We've made it a sepreated open-source project, source codes in `iGEM-CNN-Regression` directory of this repository is the first version and may be relatively old. 

For the latest version, please refer to our project repository [iGEM-CNN-Regression](https://github.com/sysu-software-2020/iGEM-CNN-Regression).
    
Our deep learning frame is shown below:  
![CNN_pic](https://github.com/sysu-software-2020/iGEM-CNN-Regression/blob/main/imgs/CNN.png)  
