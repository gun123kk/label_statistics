import os, shutil
import pandas as pd

class rank_stcs_data():
#private
    def __collect_name_id_list(self, path_val):
        all_id_name_list_temp = os.listdir(path_val)
        all_list = []
        for i in all_id_name_list_temp:
            temp_list = []
            if os.path.isdir(path_val) and i[0] !='.':
                pos = i.find('_')
                if pos > 0:
                    #self.num_counter = self.num_counter + 1
                    get_id = i[0:pos]
                    get_name = i[pos+1:len(i)]
                    temp_list.append(get_id)
                    temp_list.append(get_name)
                    all_list.append(temp_list)
                    self.__all_id_name_list.append(i)
        #print(self.__all_id_name_list)

    def __search_id(self, val):
        #./file/105AB0048_name
        val = str(val)
        pos0 = val.find('/')
        pos1 = val.find('_')
        id_temp = val[pos0+1:pos1]
        #print(id_temp)
        pos2 = id_temp.find('/')
        get_id = id_temp[pos2+1:pos1]
        #print(get_id)
        return get_id

    def __search_name(self, val):
        #./file/105AB0048_name
        val = str(val)
        pos0 = val.find('_')
        get_name = val[pos0+1:len(val)-1]
        #print(get_name)
        return get_name


    def __deal_with_type3_format(self, val, id_name):
        #type3 format ex:
        #[0]:   ['./file/105340033_name/', 
        #[1]:   ['Drone_002', 'Drone_001'], 
        #[2]:   [], 
        #[3]:   './file/105340033_name/Drone_002', 
        #[4]:   [], 
        #[5]:   ['0a1cedcb9ad2cf5e621240b1ca144d82-asset.json'], 
        #[6]:   './file/105340033_xxx/Drone_001', 
        #[7]:   [], 
        #[8]:   ['0a0cab3e707aae341744df88e9d3fb57-asset.json']],  
        get_id = self.__search_id(id_name)
        get_name = self.__search_name(id_name)
        #print(get_id)
        #print(get_name)
        #print(len(val[1]))
        pitch = 0
        for i in range(len(val[1])):
            temp = []
            #if i > 0:
                #get_id = ''
                #get_name = ''
            temp.append(get_id)
            temp.append(get_name)
            file_name = val[1][i]
            temp.append(str(file_name) + '/')
            self.__id_name_file_list.append(temp)
            for j in range(len(val[5 + pitch])):
                file_name_json = val[5 + pitch][j]
                if self.__filename_extension_check(file_name_json):
                    self.__save_all_file_path.append(str(val[0]) + str(file_name) + '/' + val[5 + pitch][j])
            pitch = pitch + 3

    def __filename_extension_check(self, val):
        c = str(val)
        pos0 = c.find('.json')
        pos1 = c.find('.csv')
        if pos0 > 0 or pos1 >0:
            return True
        else:
            return False


    def __deal_with_type1_2_format(self, val, id_name):
        for i in range(len(val[2])):
            temp = []
            #if i > 0:
                #get_id = ''
                #get_name = ''
            #else:
            get_id = self.__search_id(id_name)
            get_name = self.__search_name(id_name)
            temp.append(get_id)
            temp.append(get_name)
            file_name = val[2][i]
            temp.append(file_name)
            if self.__filename_extension_check(file_name):
                self.__save_all_file_path.append(str(val[0] + str(file_name)))
            self.__id_name_file_list.append(temp) 
        
    def __show_save_all_file_path(self, path_val):
        for i in path_val:
            print(i)

    def __add_id_name_filename_to_pd_data(self, val):
       #ex : ['./file/108314117_name/', [], ['Drone_030-export.csv']]
        for i in val:
            #print(i)
            c = str(i)
            id_name = i[0]
            if len(i[1]) != 0:
                self.__deal_with_type3_format(i, id_name)
            else:
                self.__deal_with_type1_2_format(i, id_name)
            self.__pd_data = pd.DataFrame(self.__id_name_file_list, columns = ['ID', 'NAME', 'FILE_NAME'])
        #self.__show_save_all_file_path(self.__save_all_file_path)

    def __get_file_path_list(self, file_path_val, id_name_list_val):
        #for i in self.pd_data['ID']:
        csv_json_file_path = []
        for i in id_name_list_val:
            temp = []
            path = file_path_val + str(i) + '/'
            for root, dirs, files in os.walk(path):
                #print(root)
                #print(dirs)
                #print(files)
                #print("===============================")
                temp.append(root)
                temp.append(dirs)
                temp.append(files)

            csv_json_file_path.append(temp)
        self.__add_id_name_filename_to_pd_data(csv_json_file_path)

# public 
    def show_all_file_path(self):
        if self.__show_all_file_path_flag:
            for i in self.__save_all_file_path:
                print(i)
        else:
            print('please do run_RSD() first!!')

    def create_final_execl(self, file_name):
        self.__pd_data.to_csv(file_name + ".csv", index=False)   
    
    def run_RSD(self):
        self.__collect_name_id_list(self.__file_path)
        self.__get_file_path_list(self.__file_path, self.__all_id_name_list)
        self.__show_all_file_path_flag = True
        print('show_all_file_path_flag = True!!')

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__all_id_name_list = []
        self.__id_name_file_list = []
        self.__save_all_file_path = []
        self.__show_all_file_path_flag = False
        #print(self.__file_path)




