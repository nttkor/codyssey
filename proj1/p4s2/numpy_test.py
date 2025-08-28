import numpy as np
import os


# 데이터 파일 경로
file_path_1 = 'mars_base_main_parts-001.csv'
file_path_2 = 'mars_base_main_parts-002.csv'
file_path_3 = 'mars_base_main_parts-003.csv'

def load_and_merge_numpy():
    try:
        # 각 파일에서 'strength' 값만 로드 (skiprows=1로 헤더 제외, usecols=1로 두 번째 열만)
        arr1 = np.loadtxt(file_path_1, delimiter=',', skiprows=1, usecols=1, encoding='utf-8')
        arr2 = np.loadtxt(file_path_2, delimiter=',', skiprows=1, usecols=1, encoding='utf-8')
        arr3 = np.loadtxt(file_path_3, delimiter=',', skiprows=1, usecols=1, encoding='utf-8')

        # 각 파일의 'parts' 이름만 로드 (dtype='U'로 문자열 타입 지정)
        parts_names = np.loadtxt(file_path_1, delimiter=',', skiprows=1, usecols=0, dtype='U', encoding='utf-8')
        
        # 세 개의 value 배열을 수평으로 합치기 (각 행이 3개의 값을 갖게 됨)
        combined_values = np.hstack((arr1.reshape(-1, 1), arr2.reshape(-1, 1), arr3.reshape(-1, 1)))

        print("통합된 'strength' 값 배열:")
        print(combined_values)
        print("---------------------------------")
        
        return parts_names, combined_values
    except FileNotFoundError as e:
        print(f"오류: 파일을 찾을 수 없습니다 - {e.filename}")
        return None, None
    
def load_csv():
    try:
        arr1 = np.loadtxt(file_path_1, delimiter=',', skiprows=1, usecols=1)
        arr2 = np.loadtxt(file_path_2, delimiter=',', skiprows=1, usecols=1)
        arr3 = np.loadtxt(file_path_3, delimiter=',', skiprows=1, usecols=1)

                # 세 개의 구조화 배열을 하나로 병합
        combined_data = np.concatenate((arr1, arr2, arr3),axis=0)
        print("통합된 'parts' 배열:")
        print(combined_data)
        print("---------------------------------")
        return combined_data
    
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
    parts = load_and_merge_numpy()
    parts_mean(parts)

if __name__ == '__main__':
    main()