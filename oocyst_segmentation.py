# Some basic setup:
import argparse
import sys
import gc
import statistics

# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random
#from google.colab.patches import cv2_imshow

import xlsxwriter
import pandas as pd

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def parse_args():
    parser= MyParser(description='This script does perform inference on jpg files in a directory')
    parser.add_argument('--dir', default="", type=str)
    config = parser.parse_args()
    if len(sys.argv)==1: # print help message if arguments are not valid
        parser.print_help()
        sys.exit(1)
    return config

config = vars(parse_args())

#load pretrained *oocyst* model
cfg = get_cfg()
cfg.merge_from_file("model/cfg.yaml")
cfg.MODEL.WEIGHTS = "model/model_0006199.pth"
cfg.MODEL.DEVICE='cpu'
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5
predictor = DefaultPredictor(cfg)


#load pretrained *midgut* model
cfg2 = get_cfg()
cfg2.merge_from_file("model/cfg.MG.yaml")
cfg2.MODEL.WEIGHTS = "model/model_0002399.MG.pth"
cfg2.MODEL.DEVICE='cpu'
cfg2.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg2.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5
predictor2 = DefaultPredictor(cfg2)

for filename in os.listdir(config["dir"]):

    #read image
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.tif') or filename.endswith('.tiff'):
        im_path= os.path.join(config["dir"],filename)
        im = cv2.imread(im_path)
        print(f"processing {im_path}\n")

        ########
        #midgut#
        ########

        #predict
        outputs = predictor2(im)
        #get midgut pred instances
        midgut_pred_idx = (outputs["instances"].pred_classes == 0).nonzero(as_tuple=True)[0].tolist()
        midgut_instances = outputs["instances"][midgut_pred_idx]
        #get the highest-scoring midgut
        best_midgut_idx = midgut_instances.scores.argmax().tolist()

        del outputs
        gc.collect() #free up memory, the AWS instance only has 8G memory

        #get midgut mask
        midgut_mask = midgut_instances[best_midgut_idx].pred_masks[0].numpy().astype('uint8')*255
        #dilate midgut to accomodate oocysts hanging just outside of the midgut 
        kernel = np.ones((10,10), np.uint8)  #this kernel roughly dilates the midgut about the radius of an typical oocyst
        dilated_midgut_mask = cv2.dilate(midgut_mask, kernel, iterations=1)
        #save dilated mask to file
        cv2.imwrite(f"{im_path.rstrip('jpg')}midgut.MASK.tiff",midgut_mask,) 

        del midgut_mask
        gc.collect() #free up memory, the AWS instance only has 8G memory

        #Draw midgut predictions on the image.
        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg2.DATASETS.TRAIN), scale=1.0)
        v.metadata.thing_classes=["midgut","oocyst"]
        out = v.draw_instance_predictions(midgut_instances[best_midgut_idx])
        cv2.imwrite(f"{im_path.rstrip('jpg')}midgut.jpg",out.get_image()[:, :, ::-1]) 
        del v
        del out
        del midgut_instances
        gc.collect()  #free up memory, the AWS instance only has 8G memory

        ########
        #oocyst#
        ########

        #predict
        outputs = predictor(im)
        #get oocyst pred instances
        oocyst_pred_idx = (outputs["instances"].pred_classes == 0).nonzero(as_tuple=True)[0].tolist()
        oocyst_instances = outputs["instances"][oocyst_pred_idx]

        del outputs
        gc.collect() #free up memory, the AWS instance only has 8G memory

        #check if each oocyst overlaps with the dilated midgut
        oocyst_in_midgut_idx = []
        for i in range(0,len(oocyst_instances.pred_classes)):
            an_oocyst_mask = oocyst_instances[i].pred_masks[0].numpy().astype('uint8')*255
            in_midgut_bool = np.logical_and(an_oocyst_mask,dilated_midgut_mask).any()
            if in_midgut_bool:
                oocyst_in_midgut_idx.append(i)

        #get the oocyst in midgut
        midgut_oocyst_instances = oocyst_instances[oocyst_in_midgut_idx]
        midgut_conf_oocyst_instances = midgut_oocyst_instances[midgut_oocyst_instances.scores > 0.97]

        del oocyst_instances
        del midgut_oocyst_instances
        gc.collect()  #free up memory, the AWS instance only has 8G memory

        # Draw oocysts that are in the midgut
        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN), scale=1.0) #need to change cfg.yaml->DATASETS->TRAIN: dataset_train-> dataset_MG_train
        v.metadata.thing_classes=["oocyst","midgut"]
        out = v.draw_instance_predictions(midgut_conf_oocyst_instances)
        cv2.imwrite(f"{im_path.rstrip('jpg')}oocyst.jpg",out.get_image()[:, :, ::-1]) 
        del v
        del out
        del dilated_midgut_mask
        del im
        gc.collect()  #free up memory, the AWS instance only has 8G memory

        #get oocyst count and size 
        areas=[]
        for i in range(0,midgut_conf_oocyst_instances.pred_masks.shape[0]): #go through all confident-midgut-oocyst instances
            area = np.count_nonzero(midgut_conf_oocyst_instances.pred_masks[i]) #calculate area 
            areas.append(area)

        count = len(areas)
        #calculate some statistics of the distriubtion of oocyst area
        Avg_area = 0
        Median_area = 0
        variance = 0
        std_var_area = 0

        if count>0:
            Avg_area = sum(areas)/len(areas)
            Median_area = statistics.median(areas)
            variance = sum([((x - Avg_area) ** 2) for x in areas]) / len(areas)
            std_var_area = variance ** 0.5

        #get oocyst center coordinate
        center_X=[]
        center_Y=[]
        for i in range(0,midgut_conf_oocyst_instances.pred_masks.shape[0]): #go through all confident-midgut-oocyst instances
            oocyst_mask=midgut_conf_oocyst_instances.pred_masks[i].numpy().astype('uint8')*255
            M=cv2.moments(oocyst_mask)
            center_X.append(round(M['m10'] / M['m00']))
            center_Y.append(round(M['m01'] / M['m00']))

        #write xlxs file
        df = pd.DataFrame({"Oocyst_area":areas,"center_X":center_X, "center_Y":center_Y})
        df.index+=1 #make index start from 1
        df2 = pd.DataFrame({"Oocyst_count":[count],  "Average_oocyst_area":[Avg_area], "Median_oocyst_area":[Median_area], "Standard_deviation_of_oocyst_area":[std_var_area]})
        writer = pd.ExcelWriter(f"{im_path.rstrip('jpg')}count_N_size.xlsx", engine='xlsxwriter')
        df2.to_excel(writer, sheet_name='Oocyst_count', index=False)
        df.to_excel(writer, sheet_name='Oocyst_area', index_label="Oocyst_instance")

        #format xlxs
        workbook=writer.book
        center = workbook.add_format({'align': 'center'})
        worksheet= writer.sheets['Oocyst_count']
        worksheet.set_column('A:E', None, center)
        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 33)
        worksheet= writer.sheets['Oocyst_area']
        worksheet.set_column('A:B', None, center)
        worksheet.set_column(0, 2, 15)
        writer.save()

        del writer
        del midgut_conf_oocyst_instances
        gc.collect()
        ##done
        print("completed oocyst recognition")



        
del predictor
del predictor2
del cfg
del cfg2
del config
gc.collect()