import glob 
import os 
import shutil
import datetime as dt
from collections import OrderedDict 
from utils.move_shutil import update_config, update_json
from utils.segmenatation import seg
from utils.custom import custom_info

import numpy as np 

from PIL import Image 
from utils.opt import logger


class coco_one_dict():
    def __init__(self,j_path,data_path,rbox = False,
              box3DPX = False,keypoint2d = False,
              keypoint3d = False,seg_bool=False,custom=False):
        self.file = update_json(j_path)
        self.coco_file = OrderedDict() 
        #self.info = OrderedDict() 
        #self.licenses = OrderedDict()
        self.images = OrderedDict()
        self.annotations = OrderedDict()
        self.categories = OrderedDict()
        self.data_path = data_path # ./data/datasets
        
    def images_dict(self):
        images_info = [] 
        
        date_create = dt.datetime.now()
        year = date_create.year
        date_create = transtime(date_create)
        image_name_uniq = [] 
        count = 0
        image_dir = self.data_path
        
        
        img_path = image_dir+'/image/'
        for i in range(len(ann)):
            num_img_dict = OrderedDict()
            count +=1 
            if ann["file_name"][i] not in image_name_uniq:
                #print(ann["file_name"][i])
                num_img_dict["license"] = 1
                num_img_dict["file_name"] = ann["file_name"][i]
                url_name ="https://www.sim2real.co.kr/train/"+ann["file_name"][i]
                
                num_img_dict["coco_url"] = url_name # 미정 -> 알파포즈는 이걸로 train/vaildation 나누긴 함 
                # "http://images.cocodataset.org/val2017/000000397133.jpg",
                num_img_dict["height"] = int(float(str(ann["height"][i])))
                num_img_dict["width"] = int(float(str(ann["width"][i])))
                num_img_dict["date_captured"] = date_create
                num_img_dict["flickr_url"] = './'+img_path +ann["file_name"][i]+'.jpg' # 미정 
                img_id = create_image_id(ann["file_name"][i])
                num_img_dict["id"] = img_id 
                
                image_name_uniq.append(ann["file_name"][i])
                
                images_info.append(num_img_dict)
            
        
# make dictionary 
coco_file = OrderedDict()

# coco annotation order 
info = OrderedDict() 
licenses = OrderedDict()
images = OrderedDict()
annotations = OrderedDict()
categories = OrderedDict()

no_urldata = "no url"      
def coco_dict(ann,category,data_path,rbox = False,
              box3DPX = False,keypoint2d = False,
              keypoint3d = False,seg_bool=False,custom=False):
    save_dir = data_path
    info_dicts = info_dict() 
    licenses_dict = lice_dict()
    imges_ls = images_dict(ann,save_dir) 
    ######## 확인용 #########
    #########################
    
    
    #########################
    anno_ls = anno_dict(ann,category,save_dir,
                        rbox,box3DPX,keypoint2d,keypoint3d,
                        seg_bool,custom)
    category_ls = cate_dict(category,custom)
    
    # print(licenses_dict)
    # print(imges_ls)
    # print('type :',type(imges_ls))
    #print(anno_ls)
    
    coco_file["info"] = info_dicts
    coco_file["licenses"] = [licenses_dict]
    coco_file["images"] = imges_ls
    coco_file["annotations"] = anno_ls
    coco_file["categories"] = category_ls
    
    
    #print(coco_file)
    
    return coco_file # dict
    

def info_dict():
    date_create = dt.datetime.now()
    year = date_create.year
    date_create = transtime(date_create)
    descript = "sim2real virtual dataset"
    urls = "https://www.sim2real.co.kr/"
    version = "1.0"
    contributor = 'sim2real'
    
    info["description"] = descript
    info["url"] = urls
    info["version"] = version
    info["year"] = year
    info["contributor"] = contributor
    info["date_created"] = date_create
    
    return info # dict 
    



def lice_dict():
    urls = "https://www.sim2real.co.kr/"
    ids = 1
    name = "sim2real License"
    
    licenses["url"] = urls
    licenses["id"] = ids
    licenses["name"] = name
    
    return licenses
    
def images_dict(ann,save_dir):
    images_info = [] 
    
    date_create = dt.datetime.now()
    year = date_create.year
    date_create = transtime(date_create)
    image_name_uniq = [] 
    count = 0
    image_dir = save_dir.split('./result/')[-1]
    
    
    img_path = image_dir+'/image/'
    for i in range(len(ann)):
        num_img_dict = OrderedDict()
        count +=1 
        if ann["file_name"][i] not in image_name_uniq:
            #print(ann["file_name"][i])
            num_img_dict["license"] = 1
            num_img_dict["file_name"] = ann["file_name"][i]
            url_name ="https://www.sim2real.co.kr/train/"+ann["file_name"][i]
            
            num_img_dict["coco_url"] = url_name # 미정 -> 알파포즈는 이걸로 train/vaildation 나누긴 함 
            # "http://images.cocodataset.org/val2017/000000397133.jpg",
            num_img_dict["height"] = int(float(str(ann["height"][i])))
            num_img_dict["width"] = int(float(str(ann["width"][i])))
            num_img_dict["date_captured"] = date_create
            num_img_dict["flickr_url"] = './'+img_path +ann["file_name"][i]+'.jpg' # 미정 
            img_id = create_image_id(ann["file_name"][i])
            num_img_dict["id"] = img_id 
            
            image_name_uniq.append(ann["file_name"][i])
            
            images_info.append(num_img_dict)
            
        else : 
            pass 
    
    print('object_count : ',count)
    print('image count :',len(image_name_uniq))
    return images_info

def anno_dict(ann,category,save_dir,
              rbox,box3DPX,keypoint2d,keypoint3d,
              seg_bool,custom):
    """
    _summary_
    segmentation : 
        input : [[100,100],[300,300]]
        output : [[100,100,300,300]]
        if None 
            RLE :  [xmin, ymin, xmin, ymin + ymax, xmin + xmax, ymin + ymax, xmin + xmax, ymax]
            
    num_keypoint : Number of non-zero values of the keypoint
    
    area : width * height 
        2017부터는 seg 영역의 넓이 
    
    iscrowd : 
        keypoint : 0
        none keypoint : 1 
    
    keypoint : x,y,z 
        z - 0 : None visual
        z - 1 : occluded
        z - 2 : visual
    
    image_id : same as id in images
    
    bbox : 
        input: [xmin,xmax,ymin,ymax]
        output : (upper left) xmin, ymin, width, height 
        
    rbbox : 
        input: [degree, x_center, y_center, w, h ]
        output : [degree, x_center, y_center, w, h ]
    

    category_id : same as id in categories 
    
    id : This is a unique identifier that differentiates each object
    
    추가해야 할 것들 
    3D keypoint 

    """
    ann_ls = [] 
    seg_img_pth = save_dir + 'seg/'
    c = category
    
    for i in range(len(ann)):
        num_object = OrderedDict()
        ##############box2d#############
        if not ann['box2d'][i] == []:
            xmin,xmax,ymin,ymax = ann['box2d'][i] 
            
            w = xmax-xmin
            h = ymax-ymin
            num_object["bbox"] = [xmin,ymin,w,h]
            num_object["area"] = (w*h)/2
            # 2017에서는 segmentation 영역 크기로 바뀜 
        elif  ann['box2d'][i] == []: 
            logger.info(f'None bbox info - index : {ann["index"][i]}')
        ################################
        
        if ann["file_name"][i] != None :
            img_id = create_image_id(ann["file_name"][i])
            num_object["image_id"] = img_id

        elif ann["file_name"][i] == None:
            logger.info(f'None label_name or image_id info - index : {ann["index"]}')
        #############unique id ##################
        if ann["unique_id"][i] != None :
            num_object["id"]  = ann["unique_id"][i]
        elif ann["unique_id"][i] == None :
            logger.info(f'None unique_id info - index : {ann["index"]}')

###################################### 옵션 ########################################################  
        ########## keypoint2d ###############
        height = int(str(ann["height"][i]))
        width = int(str(ann["width"][i]))
        
        if ann['keypoint2d'][i] != [] and ann['keypoint2d_visible'][i] !=None and keypoint2d:
            kls,count,crowd= concat_keypoint(ann['keypoint2d'][i],ann['keypoint2d_visible'][i],width ,height)
            num_object["iscrowd"] = crowd
            num_object["num_keypoints"] = count
            num_object["keypoints"] = kls
            
        elif ann['keypoint2d'][i] == [] and keypoint2d:  
            logger.info(f'None keypoint2d info - index : {ann["index"][i]}')
        elif not keypoint2d:
            pass 
        ########## rotation bbox  ############
        if ann['rbox2d'][i] != [] and rbox:
            num_object["rbbox"] = ann['rbox2d'][i]
            #print(ann['rbox2d'][i])
            
        elif ann['rbox2d'][i] == [] and rbox: 
            logger.info(f'None RBox info - index : {ann["index"][i]}')
        # bbox 데이터가 비어 있으면 빈 딕셔너리로 반환하고, 파일 명이랑 고유 id 출력해주기
        elif not rbox:
            pass 
        ########## box3dpx ############
        if box3DPX and ann['box3dpx'][i] != []:
            num_object["box3dpx"] = ann['box3dpx'][i]

        elif ann['box3dpx'][i] == [] and box3DPX:
            logger.info(f'None box3DPX info - index : {ann["index"][i]}')
        elif not box3DPX :
            pass 
        ######### keypoint 3d ###########
        if keypoint3d and ann['keypoint3d'][i] != []:
            num_object["keypoint3d"] = ann["keypoint3d"][i]
   
        elif ann['keypoint3d'][i] == [] and keypoint3d:  
            logger.info(f'None keypoint3d info - index : {ann["index"][i]}')
            
        elif not keypoint3d: 
            pass
        ######### keypoint 2d ###########
        if seg_bool and ann['segmentation_id'][i] != None:
            num = int(ann['segmentation_id'][i])
            
            # 임시 # num_object["segmentation"] = int(ann['segmentation_id'][i])
            seg_file = os.path.join(seg_img_pth,ann["file_name"][i]+'.png')
            if not os.path.exists(seg_file):
                print(seg_file)
                raise Exception("seg image nonexists")
            elif os.path.exists(seg_file):
                seg_coordi = seg(seg_file,num)
                #print(seg_coordi)
                
                
                # print('seg_file_path :',seg_file)
                # print("seg_coordi : ",seg_coordi)
                num_object["segmentation"] = seg_coordi
        elif seg_bool and ann['segmentation_id'][i] == None:
            logger.info(f'None segmentation info - index : {ann["index"][i]}')
            
        elif not seg_bool:
            pass 
            
        
        if custom :
            custinfo = custom_info(c.ReID) 
            #print('df custom_inf :',ann["custom_info"])
            num_object,label_name = custinfo.dict_info_add(num_object,ann["custom_info"][i])
            if isinstance(label_name,str):
                cate_id = create_cate_id(label_name,c)
                num_object["category_id"] = cate_id
            elif isinstance(label_name,int): 
                cate_id = create_cate_id(ann["category_name"][i],c)
                num_object["category_id"] = cate_id
            # input category.ReID, ann["reid"]

        elif not custom :
            pass 

 ####################################################################################################       
        ann_ls.append(num_object)
        
    return ann_ls
        
            

def cate_dict(category,custom):
    catego = [] 
     
    c = category
    for i in c.CATEGORIES:
        supc = i.supercategory.upper()
        i['skeleton'] = c.SUPERCATEGORY[supc].skeleton
        i['keypoints'] = c.SUPERCATEGORY[supc].keypoints
        # if custom :
        #     custinfo = custom_info(c.ReID)
        #     x = custinfo.categories_info()
            
        
        catego.append(i)
        
    return catego

def transtime(times):
    ls = list(map(str,(times.year,times.month,times.day)))
    time_data = ls[0] + '/' + ls[1] + '/' + ls[2]
    return time_data     

def concat_keypoint(kp,vkp,w,h):
    kp_ls = [] 
    count = 0
    
    for i in range(len(vkp)):
        x,y = kp[i]
        vk = vkp[i]
        if vk == 1 or x < 0 or y < 0 or x > w or y > h : # 0
            z = 0 #2 
            
        elif vk == 0: # 1
            z = 2  # 0
            count +=1 
        kp_ls.append(x)
        kp_ls.append(y)
        kp_ls.append(z)
        
    if count == 0: 
        crowd = 1
    else:
        crowd = 0
        
    return kp_ls, count, crowd      

def create_image_id(file_name):
    img_id_ls = file_name.split('-')
    img_id_1 = img_id_ls[0][1:]
    img_id_2 = img_id_ls[1].split('.')
    img_id = img_id_1 + img_id_2[0] +img_id_2[1]
    
    return int(img_id)

def create_cate_id(label_name,category):
    cate_ls = category.CATEGORIES # list 
    for i in cate_ls:
        if label_name.upper() == i.name.upper():
            return int(i.id)

        
    
if __name__ == "__main__":
    coco_dict()