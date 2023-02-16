import os 
import pandas as pd 
from .read_to_path import update_json
from .form.coco import coco, coco_anno
from .opt import logger
from .move_shutil import json_concat,sim2real_df,path_confirm

class dataset_transe():
    def __init__(self,opt,cfg,dataset_form,dataset_ls,save_root_path,seg_ls):
        logger.info(f'transe from dataset {dataset_form}, count {len(dataset_ls)}')
        self.save_path_root = save_root_path
        self.save_label_path = path_confirm(os.path.join(save_root_path,'labels/'))
        self.data_path = opt.data_path
        self.rbox = opt.rbox 
        self.box3dpx = opt.box3DPX 
        self.key2p = opt.keypoint2d
        self.key3p = opt.keypoint3d
        self.seg = opt.seg_bool 
        self.custom = opt.custom 
        self.config_yaml = cfg
        self.seg_path = seg_ls
        
        if opt.concat:
            concat_path = os.path.join(self.save_path_root,'total.json')
            self.j_pth = json_concat(dataset_ls,concat_path)
            self.j_pth = sim2real_df(self.j_pth)
        elif not opt.concat:
            self.j_pth = dataset_ls
    ################# data set 종류 별로 나누기 ################

        if dataset_form == 'coco':
            self.coco() 
            
            
    def coco(self):
        
        assert isinstance(self.j_pth,(pd.core.frame.DataFrame,list)),'json path type error'
        logger.info(f'Dataform : COCO dataset')
        logger.info(f'rbox : {self.rbox}')
        logger.info(f'box3DPX : {self.box3dpx}')
        logger.info(f'kepoint2d : {self.key2p}')
        logger.info(f'kepoint3d : {self.key3p}')
        logger.info(f'segmentation : {self.seg}')
        logger.info(f'custom : {self.custom}')
        
        if isinstance(self.j_pth,list):
            for i in self.j_pth:
                coco.coco_one_dict(j_path=i,
                                   data_path=self.data_path,
                                   rbox=self.rbox,
                                   box3DPX=self.box3dpx,
                                   keypoint2d=self.key2p,
                                   keypoint3d=self.key3p,
                                   seg_bool=self.seg,
                                   custom=self.custom
                                    )
        
        # segmentation 속도 개선 아직 안됨 - 느림 
        elif isinstance(self.j_pth,pd.core.frame.DataFrame):
            coco.coco_dict(ann = self.j_pth,
                           category=self.config_yaml,
                           data_path=self.save_label_path,
                           rbox=self.rbox,
                           box3DPX=self.box3dpx,
                           keypoint2d=self.key2p,
                           keypoint3d=self.key3p,
                           seg_bool=self.seg,
                           custom=self.custom
                           )
            