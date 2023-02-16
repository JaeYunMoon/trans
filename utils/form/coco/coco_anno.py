#!/usr/bin/env python
# -*- coding: utf8 -*-
from fpdf import FPDF
import os, yaml

class coco_pdf():
    def __init__(self,opt,company,imgcount,segcount,cfg):
        self.opt = opt
        self.root_path = './utils/form/coco/'
        save_rpath = './result/'
        self.save_direc = os.path.join(save_rpath,company)
        print()
        pdf_path = 'Annotation/'
        self.save_path = os.path.join(self.save_direc,pdf_path)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path) 
        
        self.json_count = 1 # coco label은 하나니깐
        self.img_count = imgcount
        self.seg_count = segcount
        self.company = company
        self.reid = cfg.ReID # ./custom/custom_info/intflow-pig.yaml

    
    def dir_tree(self):
        datafrom_txt='Directory'
        PATH = os.path.join(self.root_path,datafrom_txt+'.txt')
        f = open(PATH,"w",encoding="UTF8")
        f.write('\n')
        f.write('\n')
        f.write(f'┌─{self.company}\n')
        f.write('│      ├─ Annotation\n')
        f.write('│      │      └─Annotation.pdf\n')
        f.write('│      │\n')
        f.write('│      ├─ Image\n')
        f.write('│      │      ├─20230202-124307.354725.jpg\n')
        f.write('│      │      ├─...jpg\n')
        f.write('│      │      └─...jpg\n')
        f.write('│      │\n')
        f.write('│      ├─ Label\n')
        f.write('│      │      └─intflow-coco.json\n')
        f.write('│      │\n')
        if self.opt.seg_bool:
            f.write('│      ├─ Segmentation\n')
            f.write('│      │      ├─20230202-124307.354725.png\n')
            f.write('│      │      ├─...png\n')
            f.write('└─  └─ └─...png\n')
            f.write('\n')
            f.write('\n')
            f.close()
        else:
            f.write('└─  └─ ')
            f.write('\n')
            f.write('\n')
            f.close()

        return PATH , datafrom_txt
    
    def dataformat_txt(self):
        datafrom_txt='Data Fromat'
        PATH = os.path.join(self.root_path,datafrom_txt+'.txt')

        f = open(PATH,"w",encoding="UTF8")
        f.write('\n')
        f.write('{\n    "info" : info,\n    "images": [image],')
        f.write('\n    "annotations": [annotation],')
        f.write('\n    "licenses": [license],\n}\n\n')

        # info 
        f.write('info{\n    "year": int,\n    "version": str,\n    "description": str,\n    "contributor": str,\n    "url": str,\n    "date_created": str,\n}\n\n')
        # image 
        f.write('image{\n    "id" : int,\n')
        f.write('    "width" : int,\n    "height" : int,\n')
        f.write('    "file_name" : str,\n    "license" : int,\n')
        f.write('    "flickr_url" : str,\n')
        f.write('    "coco_url" : str,\n    "date_created": str,\n}\n\n')
        # licenses 
        f.write('licenses{\n    "id": int,\n')
        f.write('    "name": str,\n    "url": str')
        f.write('\n}\n')
        f.write('\n')
    
        f.close()


        return PATH , datafrom_txt
    
    def object_txt(self):
        object_info_txt = 'Object Detection'
        PATH = os.path.join(self.root_path,object_info_txt+'.txt')
        f = open(PATH,"w",encoding="UTF8")
        f.write('\n')
        f.write('\n')
        f.write('annotation{\n    "id": int,\n    "image_id": int,\n    "category_id": int')
        f.write(',\n    "area": float,\n    "bbox": [x,y,width,height]')
        if self.opt.keypoint2d:
            f.write(',\n    "keypoints": [x1,y1,z1,...],\n    "num_keypoints": int,\n    "iscrowd": 0 or 1')
        elif self.opt.keypoint3d:
            f.write(',\n    "keypoints_3D": []')
        elif self.opt.box3DPX:
            f.write(',\n    "box3DPX": []')
        elif self.opt.seg_bool:
            f.write(',\n    "segmentation": [polygon]')
        elif self.opt.rbox:
            f.write(',\n    "rbox": [degree,x_centor,y_centor,w,h]')
        elif self.opt.custom:
            f.write(',\n    "reid": int')
        f.write(',\n}\n')
        f.close() 
        
        x = self.categories_txt()
        return PATH, object_info_txt


    def categories_txt(self):
        object_info_txt = 'Object Detection'
        PATH = os.path.join(self.root_path,object_info_txt+'.txt')
        f = open(PATH,"a",encoding="UTF8")
        f.write('\ncategories[{\n    "id":int')
        f.write(',\n    "name": str,\n    "supercategory": str')
        if self.opt.keypoint2d:
            f.write(',\n    "keypoints":[str],\n    "skeleton":[edge]')

        f.write(',\n}]\n')
        f.write('\n')
        f.write('\n')
        f.close() 


        
    # def info_txt(self):
    #     dpath, dtitle=self.dataformat_txt()
    #     opath, otitle = self.object_txt()

    #     return dpath,dtitle,opath,otitle
        

    def make_pdf(self):
        dirpath, dirtitle=self.dir_tree()
        dpath, dtitle=self.dataformat_txt()
        opath, otitle = self.object_txt()
        pdf = PDFS()
        pdf.print_chapter(dirtitle,dirpath)
        pdf.add_font('nanum','',fname ='ttf/nanum-gothic/NanumGothic.ttf',uni=True)
        pdf.set_font('nanum', '', 10)
        
        pdf.cell(40, 7, 'Annotation Count : 1',ln=2) # border="L" 라인 생성 하는거
        pdf.cell(40, 7, 'Image Count : %d'%self.img_count,ln=2)
        pdf.cell(40, 7, 'Label Count : 1',ln=2)
        
        
        if self.opt.seg_bool:
            pdf.cell(40, 7, 'Image Count : %d'%self.seg_count,ln=2)

        pdf.print_chapter(dtitle,dpath)
        pdf.add_font('nanum','',fname ='ttf/nanum-gothic/NanumGothic.ttf',uni=True)
        pdf.set_font('nanum', '', 10)
        pdf.cell(40, 7, 'image["flickr_url"] : Local path' ,ln=2)

        pdf.print_chapter(otitle,opath)
        pdf.add_font('nanum','',fname ='ttf/nanum-gothic/NanumGothic.ttf',uni=True)
        pdf.set_font('nanum', '', 10)
        pdf.cell(40, 7, 'annotation["id"] : Object-specific id(Tracking)',ln=2)
        #pdf.cell(40, 7, 'annotation["id"] : coco dataset과 차이점 - 다른 이미지에 같은 object 표현',ln=2)
        pdf.cell(40, 7, 'annotation["bbox"] : [xmin, ymin, width, height]',ln=2)
        if self.opt.custom:
            with open(self.reid,'r') as f:
                cars = yaml.load(f, Loader=yaml.FullLoader)
            for i,v in cars.items():
                pdf.cell(40, 7, '%s :  {'%i,ln=2)
                for idx,val in v.items():
                    pdf.cell(40, 7, '    %s : %s'%(val,idx),ln=2)
            pdf.cell(40, 7, '}',ln=2)
                
        
        pdf.output(self.save_path+'/ord_annotation.pdf', 'F')

        return self.save_path+'/ord_annotation.pdf'


class PDFS(FPDF):
    def header(self) -> None:
        self.set_font('Arial','B',15)
        title = "SIM2REAL"
        w = self.get_string_width(title) + 6 
        self.set_x(10)
        self.set_text_color(150,150,150) # 연한 회색 
        
        self.cell(w, 5, title, ln = 1)
        self.ln(10)
    
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        
        self.cell(0, 10, 'Sim2Real_Annotation',0, 0, 'L')
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'R')
        
        
    def chapter_title(self,label):
        # Arial 12
        
        self.set_font('Arial', 'B', 24)
        # Title
        self.cell(0, 6, '%s' % (label), 0, 1, 'L')
        # Line break
        self.ln(5)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode("utf-8")# latin-1 cp1252 utf8
        # Times 12
        
        self.set_font('Times', '', 12)
        self.set_draw_color(211,211,211)
        self.set_fill_color(240,240,240)#204, 255, 204
        self.set_line_width(.5)
        # Output justified text
        self.add_font('nanum','',fname ='./ttf/Noto_Sans_KR/NotoSansKR-Regular.otf',uni=True)
        self.set_font('nanum', '', 10)
        self.multi_cell(0, 5, txt,1,'L',True)
        # Line break
        self.ln()

    def print_chapter(self,title, name):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(name)
        
        

if __name__ =="__main__":
    # 예시 - 확인용 
    title = "SIM2REAL"
    pdf = PDFS() 
    pdf.set_title(title)
    pdf.print_chapter('Data format', './utils/form/coco/DataFormat2.txt')
    pdf.add_font('nanum','',fname ='ttf/nanum-gothic/NanumGothic.ttf',uni=True)
    pdf.set_font('nanum', '', 10)
    pdf.write(8,u'id : 이미지 정보')
    pdf.output('sim2real_demo2.pdf', 'F')
    