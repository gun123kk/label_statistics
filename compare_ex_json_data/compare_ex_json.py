import pandas as pd
import sys
import os
import json

def run_compare(compare_path, name_id, result_path, result_path_for_rs, org_file):
    diff_file = []
    diff_file, fail = read_from_ex_json(compare_path)
    if fail == True:
        print(compare_path)
        print("read json failed")
    #print(compare_path)
    df = pd.DataFrame(diff_file, columns=['id', 'id_reg', 'label'])
    temp_file_path = './temp/'
    if not os.path.isdir(temp_file_path): 
        os.mkedirs(temp_file_path)
    df.to_csv(temp_file_path + name_id + '.csv', index=False)

    save_all_data = []
    same_flag = 1
    cnt = 0
    for i in range(len(diff_file)):
#        print(diff_file[i][0])
#        print(diff_file[i][1])
#        print(diff_file[i][2])
        for j in range(cnt, len(org_file)):
            save_data = []
            same_flag = 1
#            print(org_file[i][0])
#            print(org_file[i][1])
#            print(org_file[i][2])
            if diff_file[i][0] == org_file[j][0] and \
                diff_file[i][1] == org_file[j][1] and \
                diff_file[i][2] == org_file[j][2]:
                cnt = j
#                print("========same==========")
#                print("row:")
#                print(i)
                
                same_flag = 1
                break
            else:
                same_flag = 0

        if same_flag == 0:
            save_data.append('0')   
            save_data.append('0')
            save_data.append('0')
            save_data.append('0')
            save_data.append('0')
            save_data.append(diff_file[i][2])  #2 = label
            save_all_data.append(save_data)
    if not os.path.isdir(result_path):
        os.makedirs(result_path)
    df = pd.DataFrame(save_all_data, columns=['image', 'xmin', 'ymin', 'xmax', 'ymax', 'label'])
    df.to_csv(result_path + compare_name + '.csv', index=False)
    if not os.path.isdir(result_path_for_rs):                                                                                                           
        os.makedirs(result_path_for_rs)   
    df.to_csv(result_path_for_rs + compare_name + '.csv', index=False)


def comapre_and_create_file(file_list, name_id_list, org_file):
    result_path = [] 
    result_path_for_rs = [] 
    for i in name_id_list:
        path = i
        result_path_temp = './result/' + compare_name + '/' + path + '/'
        #print(result_path)
        result_path.append(result_path_temp)
        result_path_for_rs.append('../cfile/' + path + '/')

    for i in range(len(file_list)):
        run_compare(file_list[i], name_id_list[i], result_path[i], result_path_for_rs[i], org_file)
        #print(file_list[i])
        #print(result_path[i])
    


def collect_compare_name_id_list(path_val):
    all_id_name_list_temp = os.listdir(path_val)                                                                                                       
    name_id_list = []
    compare_file_list = []

    for i in all_id_name_list_temp:
        name_id_list.append(i)

    for i in name_id_list:
        path = path_val + i + '/'
        file_name = os.listdir(path)
        file_name_str = file_name[0]    
        #print(file_name_str)
        path = path + str(file_name_str)
        compare_file_list.append(path)
    return compare_file_list, name_id_list



def read_from_ex_json(file_path):
    org_file = []
    print(file_path)
    try:                                                                                                                                                    
        with open(file_path, 'r') as reader:
            jf = json.loads(reader.read())
        data_temp = []        
        for i in jf['assets']:
            try:          
                for j in jf['assets'][i]['regions']:
                    for k in j['tags']:
                        data_temp = []        
                        data_temp.append(i)
                        data_temp.append(j['id'])
                        data_temp.append(k)
                        org_file.append(data_temp)
                        #print(k)
            except:
                print('   wrong format2: ' + file_path)
        #print(org_file) 
        return org_file, False
    except:
        print('   wrong format 3: ' + file_path)
        return '', True

if __name__ == '__main__':
    
    try:                    
        folder_name = sys.argv[1]
        folder_name = folder_name.zfill(3)
        compare_name = "Drone_" +  folder_name
        print("compare_name:" + compare_name)
    except:    
        print("please typing the correct file name")

    try: 
        org_path = './org_file/' + compare_name + '/' + compare_name + '-export.json'
        file_list = []
        name_id_list = []
        file_list, name_id_list = collect_compare_name_id_list('./compare_file/' + compare_name + '/')
        print(file_list)
        print(name_id_list)
    
        org_file = []
        org_file ,fail = read_from_ex_json(org_path)
        if fail == False:
            temp_file_path = './temp/'
            if not os.path.isdir(temp_file_path):
                os.makedirs(temp_file_path)
            df = pd.DataFrame(org_file, columns=['id', 'id_reg', 'label'])
            df.to_csv(temp_file_path + compare_name + '.csv', index=False)

        comapre_and_create_file(file_list, name_id_list, org_file)

    except NameError:
        print(NameError)


