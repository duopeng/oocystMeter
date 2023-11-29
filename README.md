## Segment oocyst from images of mosquito images stained with mercurochrome

![image](https://github.com/duopeng/midgut_oocyst_segmentation/assets/4129442/7c7db07d-b5ea-4555-83f2-9899b546fcb7)

- Generate oocyst count data each image (in Excel format)
- Generate area data for each oocyst (in Excel format)
- Fast runtime (even on CPU)

<br>

## Installation using docker (recommended):

#### (1) Clone the repository  
`git clone https://github.com/duopeng/midgut_oocyst_segmentation`

#### (2) Build docker image
```
cd midgut_oocyst_segmentation/docker

docker build --build-arg USER_ID=1000 -t pengxunduo/oocyst:d2_v0.6_py38 .
```
### (3) Run docker image
```
docker run -it --shm-size=8gb --name=oocyst_container pengxunduo/oocyst:d2_v0.6_py38
```
adjust the image name and tag accordingly if you pulled the ARM64 variant of the image
### (4) Run example to verify installation
from inside a container started by (3), execute the following commands:
```
cd midgut_oocyst_segmentation

python oocyst_segmentation.py --dir test_images
```
### Notes:
- Warnings can be ignored, e.g.: "...image_list.py:88: UserWarning: __floordiv__ is deprecated..." .
- Instead of building the Docker image, a pre-built image can be pulled using the following command:
  
Intel CPUs:  
```
docker pull pengxunduo/oocyst:d2_v0.6_py38
```
Apple silicon:
```
docker pull pengxunduo/oocyst:d2_v0.6_py38_ARM
```
- The docker image is based on Ubuntu 18.04, with Python 3.8.10, PyTorch 1.9.1, and Detectron2 v0.6.1


<br>

## Manual installation (not recommended):  
#### (1) Clone the repository  
`git clone https://github.com/duopeng/midgut_oocyst_segmentation`

#### (2) Create conda environment and install python dependencies
```
cd midgut_oocyst_segmentation
conda create -y -n oocyst python=3.9 && conda activate oocyst
pip install -r requirements.txt
```

#### (3) Install detectron2 v0.5  
MacOS and Linux:  
`python -m pip install 'git+https://github.com/facebookresearch/detectron2/tree/v0.5.git' --user`  
Windows:  
`python -m pip install git+https://github.com/facebookresearch/detectron2/tree/v0.5.git --user`  

#### (4) Model file preparation
- unzip the two model weight files and keep it in the "model" directory:     
&nbsp;&nbsp;&nbsp;<1> model_0002399.MG.pth (unzip from model_0002399.MG.zip.001 and model_0002399.MG.zip.002)  
&nbsp;&nbsp;&nbsp;<2> model_0006199.pth (unzip from model_0006199.zip.001 and model_0006199.zip.002)  

<br>

## Usage:
- prepare your own jpeg images and place them in a folder, for example "test_images" folder    

- Run oocyst segementation with the following command:  
`python oocyst_segmentation.py --dir [path to your folder]`  

-  Results
Four result files with the same prefix will be generated for each image  
  &nbsp;&nbsp; &nbsp;&nbsp;   count_N_size.xlsx     &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;   &nbsp;&nbsp; &nbsp;&nbsp;  oocyst count, area and coordiate of each oocyst, average area  
 &nbsp;&nbsp;  &nbsp;&nbsp;   [prefix].oocyst.jpg   &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp;   &nbsp;&nbsp; &nbsp;&nbsp; oocyst annotated on the original image   
 &nbsp;&nbsp;  &nbsp;&nbsp;   [prefix].midgut.jpg    &nbsp;&nbsp;  &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; midgut annotated on the original image  
  &nbsp;&nbsp; &nbsp;&nbsp;   [prefix].midgut.MASK.jpg  &nbsp;&nbsp; &nbsp;&nbsp;   A full-resolution black-whight MASK of the midgut identified  

   
<br><br>
## Installation issues

- Make sure the verion of your Python >=3.7. Versions 3.8.10 and 3.9.7 are tested. 
- Try manully install the following packages with pip:
```
pip install torch==1.9.1  
pip install torchvision==0.10.0  
pip install torchaudio==0.9.1  
pip install pandas==1.3.3  
pip install pycocotools==2.0.2   
pip install dataclasses==0.6  
pip install typing==3.7.4.3  
pip install opencv-python==4.5.3.56  
pip install xlsxwriter==3.0.1  
pip install scipy==1.7.1  
pip install detectron2==0.5  
```
- For the detectron2 package, you need build tools to compile it from source code.
  - MacOS: install `Xcode` from App store  
  - Windows: install [Visual Studio build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

