import os
import platform
import datetime as dt

class create_name():
    def __init__(self,path):
        date_create = dt.datetime.now()
        self.time_name = str(date_create.hour)+'h'+str(date_create.minute)+'m' + str(date_create.second)+'s'
        self.path = path # "custom/coco/intflow-pig.yaml"
        self.log_name = str(self.creat_save_name()) + '_'+self.time_name
        

    def creat_save_name(self):
        date_create = dt.datetime.now()
        year = date_create.year
        
        if os.path.exists(self.path):
            if platform.system() == "Windows":
                file_name = self.path.split('/')[-1].split('.')[0]
                # print(self.path)
                # print(file_name)
                self.dataset = self.path.split('/')[-2]
            else : 
                file_name = self.path.split('/')[-1].split('.')[0] 
                self.dataset = self.path.split('/')[-2]
        else : 
            raise Exception("please confirm of config paht")
        
        co = file_name
        # self.dataset = coco
        # co = intflow
        save_name = self.dataset + '-'+co # coco-intflow
        path = os.path.join("./result/",co)
        
        return self.dataset, co
    


