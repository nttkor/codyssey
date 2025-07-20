import pandas as pd
import os
def read_csv( ):
    dataFrames = []
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
            dataFrames.append([file,csv_data])
            print(f"Head data from {file}:\n\n", csv_data.head(),'\n')
    yn = input("Do you want to see full data? (y/n):")
    if yn.strip().lower() == 'y':
        for file, df in dataFrames:
            print(f"Full data from {file}:\n", df, '\n')
    else:
        print("Exiting without displaying full data.")
    return dataFrames[0][1], dataFrames[1][1], dataFrames[2][1]

if __name__ == "__main__":
    area_map, area_struct, area_catagory = read_csv()
    for v in area_catagory.values:
        print(v.tolist())