FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu18.04
# use an older system (18.04) to avoid opencv incompatibility (issue#3524)

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y ca-certificates python3.8 python3-opencv python3-pip git wget sudo ninja-build nano bash-completion zip openjdk-11-jre
RUN ln -sv /usr/bin/python3 /usr/bin/python

#Add python 3.6 & python 3.8 to update-alternatives
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2

#Update python 3 to point to python 3.8
RUN rm /usr/bin/python3
RUN ln -s python3.8 /usr/bin/python3

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser

# update pip
# RUN python3 -m pip install --upgrade pip

ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/pip/get-pip.py && \
	python3 get-pip.py --user && \
	rm get-pip.py

# install dependencies
# See https://pytorch.org/ for other options if you use a different version of CUDA
RUN pip install --user tensorboard cmake onnx   # cmake from apt-get is too old
RUN pip install --user torch==1.10 torchvision==0.11.1 -f https://download.pytorch.org/whl/cu111/torch_stable.html

RUN pip install --user 'git+https://github.com/facebookresearch/fvcore'
# install detectron2
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
# set FORCE_CUDA because during `docker build` cuda is not accessible
ENV FORCE_CUDA="1"
# This will by default build detectron2 for all common cuda architectures and take a lot more time,
# because inside `docker build`, there is no way to tell which architecture will be used.
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"

# fix broken numpy
RUN sudo python -m pip uninstall -y numpy
RUN pip install numpy==1.24.4

# install other dependencies
RUN pip install opencv-python
RUN pip install Pillow==8.4.0
RUN pip install pandas==1.3.3
RUN pip install openpyxl
RUN pip install xlsxwriter

# install ImageJ
RUN wget https://wsr.imagej.net/distros/linux/ij153-linux64-java8.zip
RUN unzip ij153-linux64-java8.zip

# install detectron2 from source
#RUN pip install --user -e detectron2_repo

# install pre-built detectron2
RUN python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.10/index.html

# install preprocessing
RUN git clone https://github.com/duopeng/image_merge-z-stack_and_stitch
# place the IJ macro in the correct folder
RUN cp image_merge-z-stack_and_stitch/stitch.ijm ImageJ/macros/stitch.ijm
RUN cp image_merge-z-stack_and_stitch/focusstack.ijm ImageJ/macros/focusstack.ijm

# install oocyst segementation
RUN git clone https://github.com/duopeng/midgut_oocyst_segmentation
# unzip modle file
RUN cd midgut_oocyst_segmentation/model && \
    cat model_0002399.MG.zip.* > model_0002399.MG.zip && \
	unzip model_0002399.MG.zip

RUN cd midgut_oocyst_segmentation/model && \
	cat model_0006199.zip.* > model_0006199.zip && \
	unzip model_0006199.zip
	
# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"
WORKDIR /home/appuser/


# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# run detectron2 under user "appuser":
# wget http://images.cocodataset.org/val2017/000000439715.jpg -O input.jpg
# python3 demo/demo.py  \
	#--config-file configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml \
	#--input input.jpg --output outputs/ \
	#--opts MODEL.WEIGHTS detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl