## midgut_oocyst_segmentation
### Perform oocyst segmentation in mercurochrome stained mosquito midgut
### This oocyst segmentation model also powers the webtool at http://got2findthemall.org/

### Requirements to run locally:

Visual Studio build tools if using Windows:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

Python >3.8  
Python packages:  
&nbsp;&nbsp;  detectron2  
&nbsp;&nbsp;  torch >=1.9.1  
&nbsp;&nbsp;  torchvision >=0.10.0  
&nbsp;&nbsp;  torchaudio >=0.9.1  
&nbsp;&nbsp;  pandas >=1.3.3  
&nbsp;&nbsp;  pycocotools   
&nbsp;&nbsp;  dataclasses  
&nbsp;&nbsp;  typing  
&nbsp;&nbsp;  opencv-python  
&nbsp;&nbsp;  xlsxwriter  

For the detectron2 package, you can git clone the repo and install using:  
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git' --user




### instructions:  
(1) Clone the repository  

(2) unzip the two model weight files in the "model" directory:     
&nbsp;&nbsp;&nbsp;&nbsp; model_0002399.MG.pth  (unzip from model_0002399.MG.zip.001 and model_0002399.MG.zip.002)  
&nbsp;&nbsp;&nbsp;&nbsp; model_0006199.pth  (unzip from model_0006199.zip.001 and model_0006199.zip.002)  

(3) prepare your own jpeg images and place them in a folder, or use the "test_images" folder    

(4) run oocyst segementation with the following command:  
&nbsp;&nbsp;&nbsp;&nbsp;  python oocyst_segmentation.py --dir [path to your folder]  

(5) Four result files with the same prefix will be generated for each image  
  &nbsp;&nbsp; &nbsp;&nbsp;   count_N_size.xlsx   oocyst count, area and coordiate of each oocyst, average area  
 &nbsp;&nbsp;  &nbsp;&nbsp;   [prefix].oocyst.jpg   oocyst annotated on the original image   
 &nbsp;&nbsp;  &nbsp;&nbsp;   [prefix].midgut.jpg   midgut annotated on the original image  
  &nbsp;&nbsp; &nbsp;&nbsp;   [prefix].midgut.MASK.jpg  A full-resolution black-whight MASK of the midgut identified  


