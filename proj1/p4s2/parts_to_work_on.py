import numpy as np
import os
# 데이터 파일 경로
file_path_1 = 'mars_base_main_parts-001.csv'
file_path_2 = 'mars_base_main_parts-002.csv'
file_path_3 = 'mars_base_main_parts-003.csv'
import numpy as np

# 데이터 파일 경로
file_path_1 = 'mars_base_main_parts-001.csv'
file_path_2 = 'mars_base_main_parts-002.csv'
file_path_3 = 'mars_base_main_parts-003.csv'

def load_and_merge_numpy():
    try:
        # np.genfromtxt로 파일 로드 (dtype=None으로 타입 자동 추론)
        data1 = np.genfromtxt(file_path_1, delimiter=',', names=True, dtype=None, encoding='utf-8')
        data2 = np.genfromtxt(file_path_2, delimiter=',', names=True, dtype=None, encoding='utf-8')
        data3 = np.genfromtxt(file_path_3, delimiter=',', names=True, dtype=None, encoding='utf-8')

        # 세 개의 구조화 배열을 하나로 병합
        combined_data = np.concatenate((data1, data2, data3),axis=0)
        
        return combined_data
    except FileNotFoundError as e:
        print(f"오류: 파일을 찾을 수 없습니다 - {e.filename}")
        return None
    
def load_csv():
    try:
        # 데이터만 읽어 1차원 ndarray로 만들어 준다
        parts_name = np.loadtxt(file_path_1, delimiter=',',usecols=0)
        arr1 = np.loadtxt(file_path_1, delimiter=',', skiprows=1, usecols=1)
        arr2 = np.loadtxt(file_path_2, delimiter=',', skiprows=1, usecols=1)
        arr3 = np.loadtxt(file_path_3, delimiter=',', skiprows=1, usecols=1)

        # 세 개의 구조화 배열을 하나로 병합
        #combined_data = np.concatenate([arr1, arr2, arr3],axis=1)
        #없는 차원을 만들어 합쳐준다

        parts = np.stack([arr1, arr2, arr3],axis=1)
        print("통합된 'parts' 배열:")
        print(parts)
        print("---------------------------------")
        return parts
    
    except FileNotFoundError as e:
        print(f"오류: 파일을 찾을 수 없습니다 - {e.filename}")
        parts = None
def parts_mean(parts):
    # 'parts' 배열이 성공적으로 생성되었을 때만 실행
    if parts is not None:
        # 항목별(열별) 평균값 계산
        column_means = np.mean(parts, axis=0)
        print("항목별 평균값:")
        print(column_means)
        print("---------------------------------")
        
        # 평균값이 50 미만인 항목의 인덱스 찾기
        indices_to_filter = np.where(column_means < 50)
        
        # 조건에 맞는 열만 필터링하여 새로운 배열 생성
        parts_to_work_on = parts[:, indices_to_filter[0]]
        print("'parts_to_work_on' 배열 (평균 < 50):")
        print(parts_to_work_on)
        print("---------------------------------")

# 세 개의 CSV 파일을 NumPy 배열로 로드 (헤더 및 문자열 열 제외)
def main():
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s2')
    # parts = load_csv()
    parts = load_csv()
    parts_mean(parts)

if __name__ == '__main__':
    main()