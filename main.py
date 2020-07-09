import rank_statistics_data as RSD
import sys
file_path = './rsfile/'
file_selection = '0'
if len(sys.argv) > 1 :
    if sys.argv[1] == '0':
        print("file selection: file with no comparison")
    elif sys.argv[1] == '1':
        file_path = './cfile/'
        print("file selection: file with comparison")

def run():
    rsd = RSD.rank_stcs_data(file_path)
    rsd.run_RSD()
    #rsd.show_all_file_path()
    rsd.create_final_execl("result_table")

if __name__ == '__main__':
    print('start')
    run()
