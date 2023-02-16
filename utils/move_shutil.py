import os, platform
import shutil
import glob, json, yaml
import pandas as pd
from .read_to_path import update_json
from easydict import EasyDict as edict

def json_concat(dataset_ls,save_path):
    data = []
    for f in dataset_ls:
        with open(f, encoding="utf-8") as infile:
            data.append(json.load(infile))
                    
    with open(save_path,'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent="\t")
    
    return save_path

def path_confirm(path):
    if not os.path.exists(path):
        os.makedirs(path) 
    
    return path

def json_to_df(js):
    ann_ls = js.annotations
    ls = [] 
    for i,v in enumerate(ann_ls):
        #print(i)
        if len(v) == 0:
            ls.append(i)
        
        v["file_name"] = js.img_name
        v["width"] = js.width
        v["height"] = js.height
    
    connt = 0
    for n in ls:

        n -= connt
        del(ann_ls[n])
        connt += 1
    ls = [] 
    df = pd.DataFrame(data = ann_ls)
    return df
        
def sim2real_df(total_json):
    with open(total_json) as f:
        js = json.loads(f.read()) ## json 라이브러리 이용
    
    for i in range(len(js)):
        edf = edict(js[i]) # 하나의 이미지를 읽는다.
        dfs= json_to_df(edf)
        
        if i == 0:
            tdf = dfs
        elif i!=0:
            tdf = pd.concat([tdf,dfs],ignore_index=True)
        
    new_column_name = [] 
    for i in range(len(tdf.columns)):
        new_column_name.append(str(tdf.columns[i]).lower().replace(' ',''))
        
    tdf.columns = new_column_name
    tdf = tdf.reset_index()
    
    #os.remove(self.total_json)
    return tdf

def update_config(config_file):
    with open(config_file) as f:
        config = edict(yaml.load(f, Loader=yaml.FullLoader))
        return config
     
def update_json(json_file):
    with open(json_file,'r',encoding='cp949') as f:
        js_file = edict(json.load(f))
        return js_file
def path_confirm(path):
    if not os.path.exists(path):
        os.makedirs(path) 
        
    return path
    
def save_df(df,root_pth = './result'):
    df_save_path = os.path.join(root_pth,"log/")
    path_confirm(df_save_path)
    
    _csv = df_save_path+'dataframe.csv'
    df.to_csv(_csv)
    return _csv
    
    
def save_json(data_dict,save_name,root_pth = './result/'):
    save_pth = os.path.join(root_pth,save_name)
    
    json_save_path = os.path.join(save_pth,'label/')
    path_confirm(json_save_path)
    json_name = json_save_path + '/' + save_name +'.json'
    with open(json_name,'w',encoding='cp949') as f:
        json.dump(data_dict,f,indent=4)
        
    return json_save_path

        
class dir_preprocessing():
    def __init__(self,opt,company) -> None:
        self.image = os.path.join(opt.data_path,'img/')
        #self.debug = os.path.join(opt.data_path,'debug/')
        self.label = os.path.join(opt.data_path,'s2rJson/')
        self.seg = os.path.join(opt.data_path,'seg/')
      
        save_root = './result/'+company+'/'
        self.save_root = path_confirm(save_root)
        
        # self.move_img = os.path.join(save_root,'image/')
        # #self.move_debug = os.path.join(save_root,'debug/')
        # self.move_label = os.path.join(save_root,'label/')
        # move_seg = os.path.join(save_root,'segmentation/')
        
        self.seg_count = 'None'
        if opt.seg_bool:
            self.seg_ls = self.dir_shutil(self.seg)
        
        self.img_ls = self.dir_shutil(self.image)
        self.json_ls = self.dir_shutil(self.label)
        
    def dir_shutil(self,ord_path):
        ls = [] 
        for (root,directories,files) in os.walk(ord_path):
            for file in files:
                file_path = os.path.join(root,file)
                ls.append(file_path)
        return ls 
    
##############################################################################
        
    
