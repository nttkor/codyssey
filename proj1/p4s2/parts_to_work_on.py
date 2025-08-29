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
    #parts를 이용하여 항목별 평균값 계산
    parts_mean = np.mean(parts, axis=1)

    #평균값이 50보다 작은 항목만 필터링
    mask = parts_mean < threshold

    masked_list = parts_list[mask]
    masked_mean = parts_mean[mask]
    #CSV를 위해 헤더+리스트+값을 병합
    combined_arr = np.stack([masked_list, masked_mean.astype(str)], axis=1)  # 숫자 → 문자 변환 필수

    rows = [header.tolist()] + combined_arr.tolist()
    
    #CSv 파일로 병합
    with open(output_file, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(','.join(row) + '\n')
    print(f"필터링 결과 {len(masked_list)}개 항목이 '{output_file}'에 성공적으로 저장되었습니다.")

def read_and_transpose_parts(input_file='parts_to_work_on.csv'):
    # CSV 파일에서 데이터 로드 (첫 줄은 헤더, 그 이후는 데이터)
    data = np.loadtxt(input_file, delimiter=',', dtype=str, skiprows=1, encoding='utf-8')
    print(f'\n보너스 과제 수행을 위해 {input_file}파일을 읽었습니다.')
    # parts2 = [부품 이름, 평균값] 으로 저장됨
    parts2 = data
    print("="*100)
    print(parts2)

    # parts3: 전치 행렬 (2 x N → N x 2 → 2행 N열 → N행 2열)
    parts3 = parts2.T

    print("\n[전치된 parts3 출력]")
    print("="*100)
    print(parts3)

    return parts2, parts3
    
def main():
    try:
        os.chdir('/home/mpeg4/Codyssey/proj1/p4s2')
        #다음 세 개의 CSV 파일을 NumPy로 읽어 각각 arr1, arr2, arr3 배열로 만든다
        header, parts_list, parts = load_csv()

        # 평균값이 50보다 작은 항목만 필터링하여 parts_to_work_on.csv로 저장
        filter_and_save(header, parts_list, parts)
        # 추가: 저장된 파일을 다시 읽고 전치 행렬 구하기
        # parts2	parts_to_work_on.csv에서 불러온 [부품명, 평균값] 데이터
        # parts3	parts2를 전치(transpose)한 결과 (형태가 행/열 바뀜)
        parts2, parts3 = read_and_transpose_parts()
        print('프로그램을 종료합니다.')
    except Exception as e:
        print(f"오류 발생: {e}")
        return
if __name__ == '__main__':
    main()