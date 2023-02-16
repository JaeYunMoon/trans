import os 
import sys
# 상위 폴더에 있는 폴더 import 할 때 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# import platform # 코드 실행 시 os 파악 할때 
import glob

# import numpy as np 
import pandas as pd 
from PyPDF2 import PdfMerger 
# import cv2 
# import matplotlib.pyplot as plt 
from utils.opt import opt,logger,cfg
from utils.make_df import path_make_df
from utils.move_shutil import dir_preprocessing
from utils.form.coco.coco import coco_dict
from utils.form.coco.coco_anno import coco_pdf,PDFS
from utils.make_name import create_name
from utils.graph import graph_analysis
from utils.dataset_confirm import dataset_transe


def main():
    logger.info('******************************')
    logger.info(opt)
    logger.info('******************************')
    logger.info(cfg)
    logger.info('******************************')
    
    cn = create_name(opt.config) 
    dataset,company = cn.creat_save_name() 
    
    # input = "./custom/coco/intflow.yaml"
    # output = (dataset = coco , company = intflow )
    
    dp = dir_preprocessing(opt,company)
    save_root = dp.save_root
    #dp =path_make_df(opt.data_path)
    ########
    json_file = dp.json_ls
    ######################################################
    img_count = len(dp.img_ls)
    seg_count = len(dp.seg_ls)

    dt = dataset_transe(opt,dataset_form = dataset,
                        dataset_ls = json_file,
                        save_root_path = save_root)
    
    #transform_path,pdf_path = df_transform(company,dataset,_ann,cfg,img_count,seg_count)
   ######################################### 그래프 만들기 위한 ##############################
    # graph_pdf_path = graph_analysis(_ann,company,opt)
    # pdfsave_path = graph_pdf_path.pdf_save
    # graph_pth = graph_pdf_path.graph_path

    #########################################
    # pdf merge 
 
    pdf_dir = pdfsave_path 
    print(pdf_dir)
    pdfmerger = PdfMerger()
    pdflist = [pdf_path,graph_pth]
    

    for pdf in pdflist:
        pdfmerger.append(pdf)
    
    pdf_path_total = pdf_dir+'Annotation.pdf'
    pdfmerger.write(pdf_path_total)
    pdfmerger.close() 
    
    if os.path.exists(pdf_path_total):
        for i in pdflist:
            os.remove(i)
    ##########################################
    print(f'\nDataFrame save path : {csv_path}')
    print(f'Json save Diretory : {transform_path}')
    
def df_transform(com_pth,dt,df,cfg,img_count,seg_count):
    """
    com_pth = 'intflow', 
    dt = 'coco'
    _ann = DataFrame 
    cfg = 
    img_count = image count 
    seg_count = seg count 
    """
    # json 통합 라벨링 / IMAGE 당 JSON 이걸 어떻게 처리할 것인가?
    if dt == 'coco':
        mscoco = coco_dict(
            df,cfg,data_path=com_pth,
            rbox=opt.rbox,box3DPX=opt.box3DPX, keypoint2d=opt.keypoint2d,
            keypoint3d=opt.keypoint3d, seg_bool = opt.seg_bool,
            custom = opt.custom
            )
        
        save_dir = save_json(mscoco,com_pth) # 이 함수 json 파일 하나 만들때
        ####
        root_path = opt.data_path
        # 파일을 옮기면서 count 세자 
        ####
        pdf = coco_pdf(opt,com_pth,img_count,seg_count,cfg).make_pdf()

        return save_dir ,pdf
    elif dt == 'aimo':
        pass
        
    else :
        print('None Dataset')
    
   
    
    
    

if __name__ == "__main__":
    main()