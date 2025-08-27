import os
import json


def step1():
    '''
    Mars_Base_Inventory_List.csv의 내용을 읽어서 화면에 출력한다.
    '''

    print('\n1. # Mars_Base_Inventory_List.csv의 내용을 읽어서 화면에 출력한다')
    try:
        with open('Mars_Base_Inventory_List.csv','r',encoding='utf-8') as csv:
            file = csv.read()
            print(file)
            return file
    except (FileNotFoundError, IOError,ValueError, UnicodeDecodeError) as e :
        # 모든 예외를 한번에 처리
        print(f"예외 발생: {str(e)}")
        raise  # 예외를 다시 발생시켜 호출한 곳에서 처리하게끔 함

def step2(file):
    print('\n2. CSV의 각 항목(콤마로 구분)을 파싱하여 Python List 객체로 변환한다.')
    parsing = []
    for line in file.split('\n'):
        if line.strip():  # skip empty lines
            elements = [
                float(v) if v.replace('.', '', 1).isdigit() else v
                for i, v in enumerate(line.split(','))
            ]
            parsing.append(elements)
    return parsing
        
def step3(parsing):
    print('\n3. 리스트를 인화성 지수(flammability index)를 기준으로 내림차순 정렬한다.')
    # 인화성 지수는 index=4
    return sorted(parsing, key = lambda x : x[4], reverse=True)

def step4(my_list):
    print('\n4.# 인화성 지수가 0.7 이상인 항목만 필터링하여 별도로 출력한다.')
    return [ line for line in my_list if line[4] >= 0.7]

def step5(filtered_list, header):
    '''
    해당 필터링 결과를 Mars_Base_Inventory_danger.csv로 CSV 형식 저장한다.
    헤더도 함께 포함된다.
    '''
    print('\n5. # 필터링된 리스트를 Mars_Base_Inventory_danger.csv로 저장한다.')
    try:
        with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8') as csv_file:
            # 헤더 먼저 저장
            csv_file.write(','.join(map(str, header)) + '\n')
            
            # 필터링된 데이터 저장
            for row in filtered_list:
                line = ','.join(map(str, row))
                csv_file.write(line + '\n')
                
        print('저장이 완료되었습니다.')
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {str(e)}")

def step5(filtered_list, header):
    '''
    해당 필터링 결과를 Mars_Base_Inventory_danger.csv로 CSV 형식 저장한다.
    헤더도 함께 포함된다.
    '''
    print('\n5. # 필터링된 리스트를 Mars_Base_Inventory_danger.csv로 저장한다.')
    try:
        with open('Mars_Base_Inventory_danger.csv', 'wb', encoding='utf-8') as csv_file:
            # 헤더 먼저 저장
            csv_file.write(','.join(map(str, header)) + '\n')
            
            # 필터링된 데이터 저장
            for row in filtered_list:
                line = ','.join(map(str, row))
                csv_file.write(line + '\n')
                
        print('저장이 완료되었습니다.')
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {str(e)}")
    
def main():
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s2')

    # 1. Mars_Base_Inventory_List.csv의 내용을 읽어서 화면에 출력한다.
    file = step1()

    # 2. CSV의 각 항목(콤마로 구분)을 파싱하여 Python List 객체로 변환한다.
    parsing = step2(file)
    print(parsing)

    # 3. 리스트를 인화성 지수(flammability index)를 기준으로 내림차순 정렬한다.
    sorted_list = step3(parsing[1:])     # 해더를 제외한다
    print(sorted_list)

    # 인화성 지수가 0.7 이상인 항목만 필터링하여 별도로 출력한다.'
    filtered_list = step4(sorted_list)
    print(filtered_list)

    # 해당 필터링 결과를 Mars_Base_Inventory_danger.csv로 CSV 형식 저장한다.
    step5(filtered_list, parsing[0])
    return
if __name__ == '__main__':
    main()
    