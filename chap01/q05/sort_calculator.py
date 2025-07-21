
#숫자를 입력받는 함수
def inputnums():
    try: 
        nums = list(map(float,input("Enter number: ").split()))
        return nums
    except:
        print('Invalid input.')
        exit()

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
    print("Sorted:",end='')
    for num in nums:
        print(f"<{num}>",end='')  #output format Sorted: <숫자1> <숫자2> <숫자3> ...
    print()
if __name__ == "__main__":
    main()



