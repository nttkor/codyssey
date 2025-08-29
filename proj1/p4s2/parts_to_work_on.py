import numpy as np
import os

# 데이터 파일 경로 (필요시 절대/상대 경로 조정)
file_path_1 = 'mars_base_main_parts-001.csv'
file_path_2 = 'mars_base_main_parts-002.csv'
file_path_3 = 'mars_base_main_parts-003.csv'


def load_csv():
    header = np.loadtxt(file_path_1, delimiter=',', dtype=str, max_rows=1, encoding='utf-8-sig')
    parts_list = np.loadtxt(file_path_1, delimiter=',', skiprows=1, usecols=0, dtype=str, encoding='utf-8-sig')
    arr1 = np.loadtxt(file_path_1, delimiter=',', skiprows=1, usecols=1)
    print(f"{file_path_1}을 성공적으로 열었습니다.")
    arr2 = np.loadtxt(file_path_2, delimiter=',', skiprows=1, usecols=1)
    print(f"{file_path_2}을 성공적으로 열었습니다.")
    arr3 = np.loadtxt(file_path_3, delimiter=',', skiprows=1, usecols=1)
    print(f"{file_path_3}을 성공적으로 열었습니다.")


    parts = np.stack([arr1, arr2, arr3], axis=1)
    return header, parts_list, parts


def filter_and_save(header, parts_list, parts, threshold=50, output_file='parts_to_work_on.csv'):
    parts_mean = np.mean(parts, axis=1)
    mask = parts_mean < threshold

    masked_list = parts_list[mask]
    masked_mean = parts_mean[mask]

    combined_arr = np.stack([masked_list, masked_mean.astype(str)], axis=1)  # 숫자 → 문자 변환 필수

    rows = [header.tolist()] + combined_arr.tolist()

    with open(output_file, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(','.join(row) + '\n')
    print(f"필터링 결과 {len(masked_list)}개 항목이 '{output_file}'에 성공적으로 저장되었습니다.")

def main():
    try:
        os.chdir('/home/mpeg4/Codyssey/proj1/p4s2')
        header, parts_list, parts = load_csv()
        filter_and_save(header, parts_list, parts)
    except Exception as e:
        print(f"오류 발생: {e}")
        return