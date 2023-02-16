import os
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as img
import pandas as pd 
from pandas import DataFrame
import re

from .make_name import create_name
from .make_df import path_make_df

class graph_analysis():
    def __init__(self,df,com_pth,opt):
        # df = sim2real에서 뽑느 df 
        # com_pth = company(intflow) 
        
        self.df = df 
        self.opt = opt
        save_path = os.path.join('./result/'+com_pth,'Annotation/')
        if not os.path.exists(save_path):
            os.makedirs(save_path) 
        
        pdf_name = os.path.join(save_path,'DataAnalysis.pdf')
        self.pdf_save = save_path
        self.graph_path = pdf_name
        
        #print('save_pdf :',pdf_name)
        self.mypdf = PdfPages(pdf_name) # pdf 쓰기 
        #print('opt.custom_label :',opt.custom_label)
        self.example_merge_image('./20230208-165053.451975_origin.jpg')
        self.example_merge_image('./20230208-165053.451975_bbox.jpg')
        self.example_merge_image('./20230208-165053.451975_seg.jpg')
        self.example_merge_image('./20230208-165053.451975_key2.jpg')
        self.example_merge_image('./20230208-165053.451975_rbox.jpg')
        
        if opt.custom_label and opt.custom:
            data = DataFrame(list(df["custom_info"]))
            data['label_name'] = data['label_name'].str.lower()

            self.label_count_make_bar(data,'label_name')
        else : 
            self.label_count_make_bar(df,'category_name')
            
        self.coordinate_scatter(df,"box2d")
        
        if opt.rbox :
            rbox = self.coordinate_scatter(df,"rbox2d")
            
            
        else:
            pass 
        
        if opt.custom : #!!!
            custom = DataFrame(list(df["custom_info"]))
            for i in custom.columns:
                if i == 'label_name':
                    pass 
                else: 
                    self.make_bar(custom,i)
            #self.make_bar(custom,"reid")

        else:
            print("reid none")
        
        #self.merge_image("./intflow.jpg")
        self.example_merge_image('./000018_yolov5-virtual10000-train.jpg')
        self.mypdf.close() # pdf 닫기
        
        
    def example_merge_image(self,path):
        image = img.imread(path)
        plt.axis()
        name = os.path.basename(path)
        plt.title('[White,Jeju]_'+name.split('_')[-1])
        plt.imshow(image)
        self.mypdf.savefig()
        plt.close()
        
    def merge_image(self,path):
        image = img.imread(path)
        plt.axis('off')
        plt.imshow(image)
        self.mypdf.savefig()
        plt.close()
        
    def label_count_make_bar(self,df,x):# 범주형 
        #fig = plt.figure(figsize=(8, 8), dpi=100) # dpi = 해상도
        name = 'label_name'
        df[x].value_counts().plot.bar()
        plt.title(name + '-'+'count')
        plt.ylabel('count')
        
        plt.xlabel(name)
        plt.xticks(rotation=0)
        #plt.yticks(range(0,(df[x].value_counts().max())+1),10)
        
        self.mypdf.savefig()
        plt.close()

    def reid(self,df,x): 
        
        pass 
        
    def make_bar(self,df,x):# 범주형 
        #fig = plt.figure(figsize=(8, 8), dpi=100)
        df[x].value_counts().plot.bar()
        plt.title(x + '-'+'count')
        plt.ylabel('count')
        
        plt.xlabel(x)
        plt.xticks(rotation=0)
        #plt.yticks(range(0,(df[x].value_counts().max())+1),10)
        self.mypdf.savefig()
        plt.close()
    
    def coordinate_scatter(self,df,x):
        #fig = plt.figure(figsize=(8,8),dpi = 100)
        name = x + '-' +'location'
        if x == "box2d":
            box_area = name + '-'+'area'
            bbox = pd.DataFrame(df[x].tolist(),columns = ["xmin","xmax","ymin","ymax"])
            bbox["x_centor"] = bbox["xmin"]+((bbox["xmax"] - bbox["xmin"]) /2)
            bbox["y_centor"] = bbox["ymin"]+((bbox["ymax"] - bbox["ymin"]) /2)
            bbox["box_area"] = (bbox["xmax"] - bbox["xmin"]) * (bbox["ymax"] - bbox["ymin"])
            ndf = pd.concat([df,bbox], axis=1)
            ndf.plot(kind = "scatter",x = "x_centor", y="y_centor",c = "box_area",
                     colorbar = True,colormap = "jet",title = box_area,alpha=0.5) 
            #plt.savefig('savefig_default.png') # image 저장
            
            self.mypdf.savefig()
            plt.close()
        elif self.opt.rbox and x == "rbox2d":
            rb_dgree = name +'-'+'dgree'
            rb_area = name +'-'+'area'
            bbox = pd.DataFrame(df[x].tolist(),columns = ["rb_degree","rb_xcentor","rb_ycentor","rb_w","rb_h"])
            bbox["rb_area_1"] = (bbox["rb_w"] * bbox["rb_h"])
            bbox["rb_area"] = (bbox["rb_area_1"] -bbox["rb_area_1"].min()) / (bbox["rb_area_1"].max()-bbox["rb_area_1"].min())
            
            bbox["rb_area"] = ((bbox["rb_area"]+1)*3)**2 # size
            ndf = pd.concat([df,bbox],axis=1)
            #print(ndf)
            
            ndf.plot(kind = "scatter",x = "rb_xcentor", y="rb_ycentor",c = "rb_degree",s ="rb_area",
                     colorbar = True,colormap = "jet",title = rb_dgree,alpha=0.5,subplots= True) 
            # ndf.plot(kind = "scatter",x = "rb_xcentor", y="rb_ycentor",c = "rb_area",
            #          colorbar = True,colormap = "jet",title = rb_dgree,alpha=0.5,subplots= True) 
            
            
            self.mypdf.savefig()
            plt.close()
 
        

    
        