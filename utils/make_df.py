import os 
import platform # 코드 실행 시 os 파악 할때 
import glob
import numpy as np 
import pandas as pd 
import datetime as dt
import json 
from .read_to_path import update_config
from .opt import opt,logger

class path_make_df():
    def __init__(self,sim2real_path):
        if os.path.exists(sim2real_path):
            jspth = os.path.join(sim2real_path,'s2rJson/')
        self.jspath = glob.iglob(jspth + '*.json')

        
    def make_df(self):
        count = 0 
        for i in self.jspath:
            if platform.system() == 'Windows':
                json_fname = i.split('//')[-1].split('.')[0]
                
            else :
                json_fname = i.split('/')[-1].split('.')[0]
            
            js_f = update_config(i) # ['img_name', 'height', 'width', 'annotations']
            
            _ann = self.json_to_df(js_f)
        
            if count ==0:
                ann_df = _ann
            else: 
                ann_df = pd.concat([ann_df,_ann],ignore_index=True)
            count +=1 
        print('json_count :',count) 
        #print('column name :',ann_df.columns[0]) # category_name
        new_column_name = [] 
        for i in range(len(ann_df.columns)):
            new_column_name.append(str(ann_df.columns[i]).lower().replace(' ',''))
            
        ann_df.columns = new_column_name
        ann_df = ann_df.reset_index()
        return ann_df
        

            
    def json_to_df(self,js):
        ann_ls = js.annotations 
        if isinstance(ann_ls,list):
            for i in ann_ls:
                i["file_name"] = js.img_name
                i["width"] = js.width
                i["height"] = js.height
                
            df = pd.DataFrame(data = ann_ls)
            
        else:
            lsd = [] 
            lsd.append(ls)
            for i in lsd:
                i["file_name"] = js.img_name
                i["width"] = js.width
                i["height"] = js.height
            df = pd.DataFrame(data = ann_ls)
        
        return df
    
