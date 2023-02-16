import cv2 
import numpy as np 
from .read_to_path import update_json

def seg(img_pth,num):
    seg_coor_dict ='./utils/refer/img_coor.json'
    img = cv2.imread(img_pth)
    coor_dict = update_json(seg_coor_dict)
    # print('coor_dict :',coor_dict)
    coor_bgr=list(coor_dict[str(num)]) # list 
    coor = [coor_bgr[2],coor_bgr[1],coor_bgr[0]]
    # print('coor : ',coor)
    coor = np.array(coor,dtype = 'int64')
    coor_uper= coor + 2 
    coor_lower = coor - 2 
    
    img_mask = cv2.inRange(img,coor_lower,coor_uper)
    
    #img_seg = np.transpose(np.nonzero(img_mask))
    contours, hierachy = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    
    #seg_contours = seg_flatten(contours)
    total = [] 
    for i in contours:
        z= seg_flatten(i)
        total.append(z)
    #coor_1c = coor_seg(img_seg)
    
    return total#[seg_contours]
    
    
def coor_seg(trans):
    poly = [] 
    for i in trans:
        if i[2] == 0:
            f = np.delete(i,2) 
            poly.append(f)
    return poly 
        
def seg_flatten(poly):
    seg = [] 
    for i in poly:
        a = i.flatten()
        for j in a:
            seg.append(j)
    
    return list(map(int, seg))
            