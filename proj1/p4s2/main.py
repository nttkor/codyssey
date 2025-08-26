import os
import json


def step1():
    # Mars_Base_Inventory_List.csv의 내용을 읽어서 화면에 출력한다.
    try:
        with open('Mars_Base_Inventory_List.csv','r',encoding='utf-8') as csv:
            file = csv.read()
            print(file)
    except (FileNotFoundError, IOError,ValueError, UnicodeDecodeError) as e :
        # 모든 예외를 한번에 처리
        print(f"예외 발생: {str(e)}")
        raise  # 예외를 다시 발생시켜 호출한 곳에서 처리하게끔 함

def step2():
    # CSV의 각 항목(콤마로 구분)을 파싱하여 Python List 객체로 변환한다.
    return
def step3():
    # 리스트를 인화성 지수(flammability index)를 기준으로 내림차순 정렬한다.
    return
def step4():
    # 인화성 지수가 0.7 이상인 항목만 필터링하여 별도로 출력한다.
    return
def step5():
    # 해당 필터링 결과를 Mars_Base_Inventory_danger.csv로 CSV 형식 저장한다.
    return
def main():
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s2')
    step1()
    return
if __name__ == '__main__':
    main()
    