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
(1) prepare your own jpeg images and place them in a folder. Three images are provided for testing, in folder "test_images"  
(2) run the following command:  
&nbsp;&nbsp;&nbsp;&nbsp;  python oocyst_segmentation.py --dir [path to your folder]
(3) Three result files (with the same image name prefix) will be generated for 
