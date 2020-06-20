import os, shutil
import pandas as pd
import json

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
        if pos0 > 0 or pos1 > 0:
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

    def __which_filename_extension(self, val):
        if val.find('.csv') != -1:
            return "csv"
        elif val.find('-export.json') != -1:
            return "ex-json"
        elif val.find('-asset.json') != -1:
            return "as-json"

    def __init_label_qty(self, table, init_flag):
        if init_flag == False:
            table = {'stand':0, 'walk':0, 'sit':0,'watchphone':0, 'basketball':0, 'baseball':0, 'riding':0, 'block25':0, 
                    'block50':0,'block75':0, 'jump':0, 'push':0, 'skateboard':0, 'handstand':0, 'soccer':0, 'fishing':0}
            init_flag = True
            print('basic parameter updated ok')
        else:
            for i in self.__table:
                #i expresses that is key(stand walk ....)
                table[i] = 0
            init_flag = True

        return table, init_flag

    def __label_not_found_check(self, table, label):
        return label in table


    def __read_from_ex_json_data(self, file_path):
        try:
            #print(file_path)
            with open(file_path, 'r') as reader:
                jf = json.loads(reader.read())
            label = []
            for i in jf['assets']:
                try:
                    for j in jf['assets'][i]['regions']:
                        try:
                            for k in range(len(jf['assets'][i]['regions'])):
                                try:
                                    for l in range(len(jf['assets'][i]['regions'][k]['tags'])):
                                        label.append(jf['assets'][i]['regions'][k]['tags'][l])
                                except:
                                    print('   wrong format0: ' + file_path) 
                        except:
                            print('   wrong format1: ' + file_path) 
                except:
                    print('   wrong format2: ' + file_path) 
                
            return label, False
        except:
            print('   wrong format 3: ' + file_path) 
            return '', True

    def __read_from_as_json_data(self, file_path):
        try:
            #print(file_path)
            with open(file_path, 'r') as reader:
                jf = json.loads(reader.read())
            label = jf['regions'][0]['tags']
            return label, False
        except:
            print('   wrong format: ' + file_path) 
            return '', True

    def __read_from_data(self, format_type, file_path):
        label = []
        if format_type == 'csv':
            try:
                ft = pd.read_csv(file_path)
                label = ft['label']
                wrong_format = False
            except:
                print('   wrong format: ' + str(file_path)) 
                wrong_format = True
        elif format_type =='ex-json':
                label, wrong_format = self.__read_from_ex_json_data(file_path)
        elif format_type =='as-json':
                label, wrong_format = self.__read_from_as_json_data(file_path)
        return label,wrong_format

    def __create_label_table(self, file_path):
        # label:
        # stand, walk, sit, watchphone, basketball, baseball, riding, 
        # block25, block50, block75, jump, push, skateboard, handstand, soccer, fishing
        # and others

        #reads all file to update table
        self.__table = {}
        init_flag = False
        self.__table, init_flag = self.__init_label_qty(self.__table, init_flag)
        print(self.__table)
        print('   check others label... ') 
        for i in file_path:
            fp = str(i)
            fe = self.__which_filename_extension(fp)
            #label = []
            wrong_format = False
            label, wrong_format =  self.__read_from_data(fe, i)
            
            if wrong_format == False:
                for j in label:
                    j = j.lower()
                    if self.__label_not_found_check(self.__table, j) == False:
                        print('   ' + j + ' not found so update it to table!!')
                        self.__table[j] = 0
        print(self.__table) 

    def __count_label_qty(self, table, label):
        for i in label:
            i = i.lower()
            table[i] = table[i] + 1
    
    def __show_count_info(self,fp, ctr, now_id, now_name, now_file_name, table):
        print("-------------------------------------------")
        print(fp)
        print(ctr)
        print(now_id)
        print(now_name)
        print(now_file_name)
        print(table)
        print("-------------------------------------------")


    def __read_file_content_and_statistics(self, file_path):
        # label:                
        # stand, walk, sit, watchphone, basketball, baseball, riding, 
        # block25, block50, block75, jump, push, skateboard, handstand, soccer, fishing

        get_id = []             
        for _id in self.__pd_data['ID']:
            get_id.append(_id)  
        
        get_name = []             
        for _name in self.__pd_data['NAME']:
            get_name.append(_name)  
                       
        get_file_name = []      
        for file_name in self.__pd_data['FILE_NAME']:
            get_file_name.append(file_name)
        ctr = 0                 
        
        table = {}
        content_list = []       
        init_flag = True
        table, init_flag = self.__init_label_qty(table, init_flag)                                                                                  
        length = len(file_path)
        #print(length)
        for i in range(length):
            fp = str(file_path[i])
            #print(fp)
            now_id = str(get_id[ctr]) 
            now_name = str(get_name[ctr]) 
            now_file_name = str(get_file_name[ctr]) 
            fe = self.__which_filename_extension(fp)
            wrong_format = False
            
            label, wrong_format =  self.__read_from_data(fe, fp)
            if wrong_format == False:
                self.__count_label_qty(table, label)
           

            if i+1 < length:
                if file_path[i+1].find(now_id) == -1 or (file_path[i+1].find(now_id) != -1 and file_path[i+1].find(now_file_name) == -1): 
                    content_list.append(table)
                    table = {}
                    #self.__show_count_info(fp, ctr, now_id, now_name, now_file_name, table)
                    table, init_flag = self.__init_label_qty(table, init_flag)
                    ctr = ctr + 1
            elif i+1 == length:
                content_list.append(table)
                table = {}
                #self.__show_count_info(fp, ctr, now_id, now_name, now_file_name, table)

        #print(len(content_list)) 
        #print(content_list)

        self.__count_and_total_result_to_pandas(content_list)

    def __count_and_total_result_to_pandas(self, val):
        stcs_column = []
        for i in self.__table:
            #i expresses that is key(stand walk ....)
            stcs_column.append(i)

        # creates total item 
        for i in val:
            #print(i)
            total = 0
            for j in stcs_column:
                total = total + int(i[j])
            i['total'] = total
            
        stcs_column.append('total')
        self.__pd_stcs = pd.DataFrame(val, columns = stcs_column)                                                                                           
        #self.__pd_stcs.to_csv("./stcs_result.csv", index=False)   
        #print(self.__pd_stcs)  
    
    def __combind_count_result_to_pd_data(self):
        self.__pd_data = pd.concat([self.__pd_data, self.__pd_stcs],sort=False, axis=1)

    def __rank_function(self):
        self.__pd_data = self.__pd_data.sort_values(by = 'total', ascending=False)
        rank = []
        prev = 0
        cal_rank = 0
        
        for i in self.__pd_data['total']:
            now = i
            if now != prev:
                cal_rank = cal_rank + 1
            prev = now
            rank.append(cal_rank)

        self.__pd_rank = pd.DataFrame(rank, columns = ['rank'])         
        
        self.__pd_data.insert(0, 'rank', rank, True)

        #print(self.__pd_data)
        
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
        print('(1)show_all_file_path_flag = True!!')
        print('(2)updating label table...')
        self.__create_label_table(self.__save_all_file_path)
        print('updated label table!!!')
        print('(3)count label qty...')
        self.__read_file_content_and_statistics(self.__save_all_file_path)
        self.__combind_count_result_to_pd_data()
        print('count finished!!!')
        print('(4)rank...')
        self.__rank_function()
        print('rank ok!!!')


    def __init__(self, file_path):
        self.__file_path = file_path
        self.__all_id_name_list = []
        self.__id_name_file_list = []
        self.__save_all_file_path = []
        self.__show_all_file_path_flag = False
        self.__table = {}
        #print(self.__file_path)




