import numpy as np
import os

# 데이터 파일 경로
file_path_1 = 'mars_base_main_parts-001.csv'
file_path_2 = 'mars_base_main_parts-002.csv'
file_path_3 = 'mars_base_main_parts-003.csv'


def main():
    # 세 개의 CSV 파일을 NumPy 배열로 로드
    try:
        arr1 = np.loadtxt(file_path_1, delimiter=',')
        arr2 = np.loadtxt(file_path_2, delimiter=',')
        arr3 = np.loadtxt(file_path_3, delimiter=',')

        # 세 배열을 하나로 병합 (수직으로 쌓기)
        parts = np.vstack((arr1, arr2, arr3))
        print("통합된 'parts' 배열:")
        print(parts)
        print("---------------------------------")
    except FileNotFoundError as e:
        print(f"오류: 파일을 찾을 수 없습니다 - {e.filename}")
        parts = None

if __name__ == '__main__':
    main()