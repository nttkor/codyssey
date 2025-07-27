def quick_sort(arr):
    """
    메모리를 효율적으로 사용하는 퀵소트의 메인 함수입니다.
    배열 전체에 대해 _quick_sort_recursive 함수를 호출합니다.
    """
    _quick_sort_recursive(arr, 0, len(arr) - 1)

def _quick_sort_recursive(arr, low, high):
    """
    퀵소트의 실제 재귀 로직을 담당하는 헬퍼 함수입니다.
    주어진 부분 배열 (low부터 high 인덱스까지)을 정렬합니다.
    """
    if low < high:
        # 1. 파티션 수행: 피봇을 기준으로 배열을 두 부분으로 나눕니다.
        #    파티션 함수는 피봇의 최종 위치를 반환합니다.
        pivot_index = _partition(arr, low, high)

        # 2. 재귀 호출: 피봇의 왼쪽 부분 배열을 정렬합니다.
        _quick_sort_recursive(arr, low, pivot_index - 1)

        # 3. 재귀 호출: 피봇의 오른쪽 부분 배열을 정렬합니다.
        _quick_sort_recursive(arr, pivot_index + 1, high)

def _partition(arr, low, high):
    """
    퀵소트의 파티션 함수입니다. (로무토 파티션 스킴)
    배열의 마지막 원소를 피봇으로 선택하고, 피봇보다 작거나 같은 원소들을
    피봇의 왼쪽으로 이동시킨 후 피봇을 올바른 위치에 배치합니다.
    """
    # 마지막 원소를 피봇으로 선택
    pivot = arr[high]
    
    # i는 피봇보다 작거나 같은 원소들이 들어갈 다음 위치의 인덱스를 추적합니다.
    # 초기에는 부분 배열의 시작 인덱스보다 하나 작게 설정합니다.
    i = low - 1  
    
    # j는 부분 배열을 순회하며 원소들을 검사합니다.
    # 피봇 원소(arr[high])는 제외하고 low부터 high-1까지 순회합니다.
    for j in range(low, high):
        # 현재 원소 arr[j]가 피봇보다 작거나 같으면
        if arr[j] <= pivot:
            # i를 한 칸 증가시켜 작은 원소가 들어갈 공간을 확보합니다.
            i += 1
            # arr[j] (작은 원소)와 arr[i] (현재 i 위치의 원소)를 교환합니다.
            # 이렇게 하면 arr[j]가 작은 원소들의 구역으로 이동합니다.
            arr[i], arr[j] = arr[j], arr[i]
    
    # for 루프가 끝나면 i는 피봇보다 작거나 같은 원소들 중 마지막 원소의 인덱스를 가리킵니다.
    # 이제 피봇을 올바른 위치 (i + 1)에 배치합니다.
    # arr[i + 1] (피봇이 들어갈 자리)와 arr[high] (원래 피봇이 있던 자리)를 교환합니다.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # 피봇이 최종적으로 위치한 인덱스를 반환합니다.
    return i + 1