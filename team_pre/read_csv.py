import pandas as pd
import os
def read_csv( ):
    dataFrame = []
    print("read_csv\n")
    base_dir = os.path.dirname(__file__) 
    # 'D:\\git\\Codyssey\\team_pre'
    filelist = ['area_map.csv', 'area_struct.csv','area_category.csv']
    for i,file in enumerate(filelist) :
        csv_path = os.path.join(base_dir, 'data', file)
        if not os.path.exists(csv_path):
            print(f"File not found: {csv_path}")
            return None
        else:
            csv_data = pd.read_csv(csv_path)
            dataFrame.append([file,csv_data])
            print(f"Head data from {file}:\n\n", csv_data.head(),'\n')
    yn =input("Do you want to see full data? (y/n):")
    if yn.strip().lower() == 'y':
        for file, df in dataFrame:
            print(f"Full data from {file}:\n", df, '\n')
    else:
        print("Exiting without displaying full data.")
    return dataFrame

if __name__ == "__main__":
    read_csv()
    
#     def os_test():
#     print("os_test")
#     print(f'os.path.realpath(__file__) : {os.path.realpath(__file__)}')
#     print(f'os.path.abspath(__file__) : {os.path.abspath(__file__)}')
#     print(f"os.getcwd() : {os.getcwd()}")
#     print(f'os.path.dirname(__file__) : {os.path.dirname(__file__)}')
#     real_path = os.path.realpath(__file__)
#     print(f'os.path.dirname(real_path) : {os.path.dirname(real_path)}')
#     abs_path = os.path.abspath(__file__)
#     print(f'os.path.dirname(abs_path) : {os.path.dirname(abs_path)}')
#     # 현재 스크립트의 디렉토리 경로
#     path = r"team_pre\data\area_structure.csv"
#     abs_path = os.path.abspath(path)
#     print("찾으려는 절대경로:", abs_path)
#     file_path = r"D:\git\Codyssey\team_pre\data\area_struct.csv"
#     print("파일 존재 여부:", os.path.exists(file_path))