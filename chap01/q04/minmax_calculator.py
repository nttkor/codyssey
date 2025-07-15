import math
def main():
    #스페이스를 이용해 문자를 분리하고
    numbers = input("IPlease enter numbers separated by spaces.: ").split()
    arr = []
    #분리된 문자가 실수형이라면 추가해준다 문제가 있다면 메세지를 출력하고 프로그램을 멈춘다.
    for v in numbers:
        try:
            arr.append(float(v))
        except:
            print(f"{v} is Invalid input.")
            exit()
    # math 라이브러리의 상수값
    max = float('-inf')
    min = float('inf')
    # 모든 숫자를 최소 최대값과 비교하면서 갱신해준다. 
    for v in arr:
        if v > max:
            max = v
        if v < min:
            min = v
    print(f'minimum = {min}, maximum = {max}')

if __name__ == "__main__":
    main()