def solution(park, routes):
    h = len(park)
    w = len(park[0])
    
    # 1. 시작 위치 찾기
    for i in range(h):
        for j in range(w):
            if park[i][j] == 'S':
                start_x, start_y = j, i
                break

    x, y = start_x, start_y
    
    # 2. 명령 처리
    for route in routes:
        direction, distance_str = route.split()
        distance = int(distance_str)
        
        nx, ny = x, y
        is_valid_move = True
        
        # 2.1. 이동 경로 유효성 검사
        for _ in range(distance):
            if direction == 'E':
                nx += 1
            elif direction == 'W':
                nx -= 1
            elif direction == 'N':
                ny -= 1
            elif direction == 'S':
                ny += 1
            
            # 2.1.1. 공원 경계 확인
            if not (0 <= nx < w and 0 <= ny < h):
                is_valid_move = False
                break
            
            # 2.1.2. 장애물 확인
            if park[ny][nx] == 'X':
                is_valid_move = False
                break
        
        # 2.2. 위치 업데이트
        if is_valid_move:
            x, y = nx, ny

    # 3. 최종 위치 반환
    return [y, x]
