def quicksort_iterative(arr):
    """while문을 사용한 퀵소트 구현"""
    if len(arr) <= 1:
        return arr
    
    # 원본 배열을 복사해서 작업
    result = arr.copy()
    
    # 스택으로 정렬할 구간들을 관리
    stack = [(0, len(result) - 1)]
    
    while stack:
        left, right = stack.pop()
        
        if left < right:
            # 파티션 수행 pivot을 얻어온다
            pivot_pos = partition(result, left, right)
            
            # 분할된 두 구간을 스택에 추가
            stack.append((left, pivot_pos - 1))    # 왼쪽 구간
            stack.append((pivot_pos + 1, right))   # 오른쪽 구간
    
    return result

def partition(arr, left, right):
    """퀵소트의 파티션 함수"""
    # 마지막 원소를 피봇으로 선택
    pivot = arr[right]
    i = left - 1  # 작은 원소들의 마지막 인덱스
    
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # 피봇을 올바른 위치에 배치
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1

def mergesort_recursive(arr):
    """재귀를 사용한 분할 정렬 구현"""
    if len(arr) <= 1:
        return arr
    
    # 분할: 배열을 반으로 나누기
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # 재귀적으로 각 절반을 정렬
    left_sorted = mergesort_recursive(left_half)
    right_sorted = mergesort_recursive(right_half)
    
    # 정렬된 두 절반을 합치기
    return merge(left_sorted, right_sorted)

def merge(left, right):
    """두 정렬된 배열을 합치는 함수"""
    result = []
    i = j = 0
    
    # 두 배열을 비교하면서 작은 것부터 결과에 추가
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # 남은 원소들을 모두 추가
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

# 테스트 예제
if __name__ == "__main__":
    test_array = [64, 34, 25, 12, 22, 11, 90, 5]
    
    print("원본 배열:", test_array)
    print()
    
    # 퀵소트 (while문)
    quick_result = quicksort_iterative(test_array)
    print("퀵소트 (while문) 결과:", quick_result)
    
    # 분할 정렬 (재귀)
    merge_result = mergesort_recursive(test_array)
    print("분할 정렬 (재귀) 결과:", merge_result)
    
    print()
    print("=== 실행 과정 시뮬레이션 ===")
    
    # 퀵소트 실행 과정 (스택 상태 출력)
    print("\n퀵소트 스택 변화:")
    arr = [5, 2, 8, 1, 9]
    print(f"초기 배열: {arr}")
    
    stack = [(0, len(arr) - 1)]
    step = 1
    
    while stack:
        print(f"Step {step}: 스택 = {stack}")
        left, right = stack.pop()
        
        if left < right:
            pivot_pos = partition(arr, left, right)
            print(f"  파티션 후: {arr}, 피봇 위치: {pivot_pos}")
            
            stack.append((left, pivot_pos - 1))
            stack.append((pivot_pos + 1, right))
        
        step += 1
    
    print(f"최종 결과: {arr}")