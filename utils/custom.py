import os 

from .read_to_path import update_config

class custom_info():
    def __init__(self,custom_info_path): 
        self.path = custom_info_path # 미리 적은 
        #self.anno = anno # 객체 하나의 모든 정보   
        if os.path.exists(self.path):
            self.custom_config_dict=update_config(self.path)
            # 파일 확인용 확인 햇으면 그 파일 딕셔너리 
        else : 
            raise Exception("path confirm")
 
    def dict_info_add(self,anno,custom_info):
        # custom_info = dataframe에서 들어오는 정보 
        value = 0
        for i in custom_info.keys(): # reid , label_name
            if i == "label_name":
                value = custom_info["label_name"].split('_')[0]
                
            elif i!="label_name" and self.custom_config_dict[i]: 
                inf = custom_info[i].lower()
                #print(inf)
                input_info = self.custom_config_dict[i][inf]
                anno[i] = input_info
            else : 
                raise ValueError
        return anno ,value

                
                
    def categories_info(self):
        custom_dict = dict()
        for i in self.custom_config_dict.keys():
            x = {v:k for k,v in self.custom_config_dict[i].items()}
            custom_dict[i] = x 
        return custom_dict
    