
#숫자를 입력받는 함수
def inputnums():
    try: 
        # 입력값은 반드시 터미널에서 input()을 사용하고, 공백으로 나누어 처리(split())한다.
        #숫자 변환은 반드시 float()로 처리한다.
        nums = list(map(float,input("Enter number: ").split()))
        return nums
    except:
        print('Invalid input.')
        exit()
# Python 내장 함수인 sorted() 와 리스트 메서드인 .sort() 사용을 금지한다. (자동 채점에서 확인됨)
# 반드시 직접 정렬 알고리즘을 구현해야 한다. (버블 정렬, 선택 정렬 등 자유롭게 구현 가능)
def bubbleSort(nums):
    end = len(nums)
    for i in range(end-1,0,-1):
        for j in range(i):
            if(nums[j] > nums[j+1]):
                nums[j] , nums[j+1] = nums[j+1], nums[j]

def main():
    nums = inputnums()
    if len(nums) == 0:  # 입력이 없을경우 에러처리
        print('Invalid input.')
        return
    bubbleSort(nums)
    #정렬된 숫자들을 오름차순으로 다음과 같은 형식으로 출력한다:
    print("Sorted:",end='')
    for num in nums:
        print(f"<{num}>",end='')  #output format Sorted: <숫자1> <숫자2> <숫자3> ...
    print()
#프로그램은 다음의 형태로 작성하여 실행된다:
if __name__ == "__main__":
    main()



