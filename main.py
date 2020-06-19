import rank_statistics_data as RSD
file_path = './file/'


def run():
    rsd = RSD.rank_stcs_data(file_path)
    rsd.run_RSD()
    #rsd.show_all_file_path()
    rsd.create_final_execl("table")

if __name__ == '__main__':
    print('start')
    run()
