nums = [v for v in range(10)]
seed = 3
for i in range(10):
    nums[i],nums[seed] = nums[seed], nums[i]
    seed += i
    seed %= len(nums)

def bubble_sort():
    for i in range(len(nums)-1):
        for j in range(len(nums)-1-i):
            if(nums[j]>nums[j+1]):
                nums[j], nums[j+1] = nums[j+1] , nums[j]
    return nums

def quick_sort

print(f'nums before sort {nums}')
sort_list  = bubble_sort()
print(sort_list)
print(f'nums after sort {nums}')




