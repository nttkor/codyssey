
#숫자를 입력받는 함수
def inputnums():
    try: 
        nums = list(map(float,input("Enter number: ").split()))
        return nums
    except:
        print('Invalid number input.')
        exit()

def bubbleSort(nums):
    end = len(nums)
    for i in range(end-1,0,-1):
        for j in range(i):
            if(nums[j] > nums[j+1]):
                nums[j] , nums[j+1] = nums[j+1], nums[j]

def main():
    nums = inputnums()
    bubbleSort(nums)
    print("Sorted:",end='')
    for num in nums:
        print(f"<{num}>",end='')
    print()
if __name__ == "__main__":
    main()



