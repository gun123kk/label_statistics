import pandas as pd
import sys
import os

def run_compare(compare_path, result_path, result_path_for_rs):
    diffFile = pd.read_csv(compare_path)
    diff_image = diffFile['image']
    #print(diff_image)

    diff_xmin = diffFile['xmin']
    #print(diff_xmin)

    diff_ymin = diffFile['ymin']
    #print(diff_ymin)

    diff_xmax = diffFile['xmax']
    #print(diff_xmax)

    diff_ymax = diffFile['ymax']
    #print(diff_ymax)

    diff_label = diffFile['label']
    #print(diff_label)
    
    orgFile = pd.read_csv(org_path)

    org_image = orgFile['image']

    org_xmin = orgFile['xmin']

    org_ymin = orgFile['ymin']

    org_xmax = orgFile['xmax']

    org_ymax = orgFile['ymax']

    org_label = orgFile['label']

    save_all_data = []
    same_flag = 1
    cnt = 0
    for i in range(len(diffFile['image'])):
        save_data = []
        same_flag = 1
        for j in range(cnt, len(orgFile['image'])):
            if diff_image[i] == org_image[j] and \
                diff_xmin[i] == org_xmin[j] and \
                diff_ymin[i] == org_ymin[j] and \
                diff_xmax[i] == org_xmax[j] and \
                diff_ymax[i] == org_ymax[j] and \
                diff_label[i] == org_label[j]:
                cnt = j
                #print("========same==========")
                #print("row:")
                #print(i)
                
                same_flag = 1
                break
            else:
                same_flag = 0

        if same_flag == 0:
            save_data.append(diff_image[i])
            save_data.append(diff_xmin[i])
            save_data.append(diff_ymin[i])
            save_data.append(diff_xmax[i])
            save_data.append(diff_ymax[i])
            save_data.append(diff_label[i])
            save_all_data.append(save_data)
    if not os.path.isdir(result_path):
        os.makedirs(result_path)
    df = pd.DataFrame(save_all_data, columns=['image', 'xmin', 'ymin', 'xmax', 'ymax', 'label'])
    df.to_csv(result_path + compare_name + '.csv', index=False)
    if not os.path.isdir(result_path_for_rs):
        os.makedirs(result_path_for_rs)
    df.to_csv(result_path_for_rs + compare_name + '.csv', index=False)
   
def comapre_and_create_file(file_list, name_id_list):
    result_path = [] 
    result_path_for_rs = []
    for i in name_id_list:
        path = i
        result_path_temp = './result/' + compare_name + '/' + path + '/'
        result_path.append(result_path_temp)
        result_path_for_rs.append('../cfile/' + path + '/')

    for i in range(len(file_list)):
        run_compare(file_list[i], result_path[i], result_path_for_rs[i])
        print(file_list[i])
        print(result_path[i])
    


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

if __name__ == '__main__':
    try:
        folder_name = sys.argv[1]
        folder_name = folder_name.zfill(3)
        compare_name = "Drone_" +  folder_name
        print("compare_name:" + compare_name)
    except:
        print("please typing the correct file name")

    try:
        org_path = './org_file/' + compare_name + '/' + compare_name + '-export.csv'
        print("org_path: " + org_path)
        file_list = []
        name_id_list = []
        file_list, name_id_list = collect_compare_name_id_list('./compare_file/' + compare_name + '/')
        print(file_list)
        print(name_id_list)
        comapre_and_create_file(file_list, name_id_list)
    except NameError:
       print(NameError) 

