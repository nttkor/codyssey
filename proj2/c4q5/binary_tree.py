# 노드 클래스 정의
class Node:
    """트리의 각 노드를 정의하는 클래스"""
    def __init__(self, key):           # 생성자: 노드 생성 시 key 값을 받음
        self.key = key                 # 노드에 저장할 값
        self.left = None               # 왼쪽 자식 노드 초기화
        self.right = None              # 오른쪽 자식 노드 초기화


# 이진 탐색 트리 클래스 정의
class BinarySearchTree:
    """이진 탐색 트리 클래스"""
    def __init__(self):                # 생성자: 트리 초기화
        self.binarytree = None        # 루트 노드를 None으로 초기화

    def insert(self, value):
        """
        트리에 값을 삽입하는 메서드
        - 단일 값(int, float 등): 일반적인 BST 방식으로 삽입
        - 리스트(list): 각 값을 하나씩 삽입하여 기존 트리에 병합 (균형 고려 X)
        """
        def _insert(root, key):       # 내부 재귀 함수: BST 삽입 로직
            if root is None:          # 현재 위치가 비어 있으면
                return Node(key)      # 새 노드를 생성하여 반환
            if key < root.key:        # 삽입할 값이 현재 노드보다 작으면
                root.left = _insert(root.left, key)   # 왼쪽 서브트리에 삽입
            else:                     # 크거나 같으면
                root.right = _insert(root.right, key) # 오른쪽 서브트리에 삽입
            return root               # 현재 노드를 반환

        if isinstance(value, list):   # 리스트가 들어온 경우
            for v in value:           # 리스트의 각 값을 순회하며
                self.binarytree = _insert(self.binarytree, v)  # 하나씩 삽입
        else:                         # 단일 값이 들어온 경우
            self.binarytree = _insert(self.binarytree, value)  # 삽입

    def rebalance_with(self, values):
        """기존 트리와 새 값을 병합하여 균형 잡힌 트리로 재구성"""
        def _build_balanced_tree(sorted_values):  # 내부 재귀 함수
            if not sorted_values:                 # 리스트가 비었으면
                return None                       # 빈 노드 반환
            mid = len(sorted_values) // 2         # 중간 인덱스 계산
            node = Node(sorted_values[mid])       # 중간값으로 노드 생성
            node.left = _build_balanced_tree(sorted_values[:mid])     # 왼쪽 절반으로 왼쪽 서브트리 생성
            node.right = _build_balanced_tree(sorted_values[mid+1:])  # 오른쪽 절반으로 오른쪽 서브트리 생성
            return node                            # 생성된 노드 반환

        combined = sorted(set(self.inorder() + values))  # 기존 + 새 값 병합, 중복 제거, 정렬
        self.binarytree = _build_balanced_tree(combined)  # 균형 트리로 재구성

    def find(self, key):
        """특정 값을 트리에서 탐색"""
        def _find(root, key):         # 내부 재귀 함수
            if root is None:          # 노드가 없으면 False
                return False
            if key == root.key:       # 값을 찾으면 True
                return True
            elif key < root.key:      # 찾는 값이 작으면 왼쪽 탐색
                return _find(root.left, key)
            else:                     # 크면 오른쪽 탐색
                return _find(root.right, key)
        return _find(self.binarytree, key)  # 루트부터 탐색 시작

    def delete(self, key):
        """특정 값을 트리에서 삭제"""
        def _find_min(node):          # 오른쪽 서브트리의 최소값 찾기
            current = node
            while current.left is not None:  # 가장 왼쪽 노드까지 이동
                current = current.left
            return current            # 최소값 노드 반환

        def _delete(root, key):       # 내부 재귀 함수
            if root is None:          # 노드가 없으면 None 반환
                return None
            if key < root.key:        # 삭제할 값이 작으면 왼쪽으로
                root.left = _delete(root.left, key)
            elif key > root.key:      # 크면 오른쪽으로
                root.right = _delete(root.right, key)
            else:                     # 삭제할 노드를 찾은 경우
                if root.left is None:     # 왼쪽 자식이 없으면 오른쪽 반환
                    return root.right
                elif root.right is None:  # 오른쪽 자식이 없으면 왼쪽 반환
                    return root.left
                # 자식이 둘 다 있는 경우
                min_larger_node = _find_min(root.right)  # 오른쪽 서브트리의 최소값
                root.key = min_larger_node.key           # 현재 노드 값을 최소값으로 교체
                root.right = _delete(root.right, min_larger_node.key)  # 중복 제거
            return root              # 수정된 루트 반환

        self.binarytree = _delete(self.binarytree, key)  # 루트부터 삭제 시작

    def inorder(self):
        """중위 순회 결과를 리스트로 반환"""
        def _inorder(root):          # 내부 재귀 함수
            return _inorder(root.left) + [root.key] + _inorder(root.right) if root else []  # 왼쪽 → 현재 → 오른쪽
        return _inorder(self.binarytree)  # 루트부터 순회 시작

    def show_tree(self):
        """트리 구조를 텍스트로 시각화 (/와 \\ 포함)"""
        def _display_aux(node):      # 내부 재귀 함수: 트리를 문자열로 변환
            if node is None:         # 노드가 없으면 공백 반환
                return [" "], 1, 1, 0

            if node.right is None and node.left is None:  # 리프 노드인 경우
                line = f"{node.key}"
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            if node.right is None:   # 왼쪽 자식만 있는 경우
                lines, n, p, x = _display_aux(node.left)
                s = f"{node.key}"
                u = len(s)
                first_line = (x + 1) * " " + (n - x - 1) * "_" + s
                second_line = x * " " + "/" + (n - x - 1 + u) * " "
                shifted_lines = [line + u * " " for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            if node.left is None:    # 오른쪽 자식만 있는 경우
                lines, n, p, x = _display_aux(node.right)
                s = f"{node.key}"
                u = len(s)
                first_line = s + x * "_" + (n - x) * " "
                second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
                shifted_lines = [u * " " + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # 양쪽 자식이 모두 있는 경우
            left, n, p, x = _display_aux(node.left)
            right, m, q, y = _display_aux(node.right)
            s = f"{node.key}"
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s + y * "_" + (m - y) * " "
            second_line = x * " " + "/" + (n - x - 1 + u + y) * " " + "\\" + (m - y - 1) * " "
            if p < q:
                left += [" " * n] * (q - p)  # 높이 맞추기
            elif q < p:
                right += [" " * m] * (p - q)
            zipped_lines = zip(left, right)
            lines = [a + u * " " + b for a, b in zipped_lines]  # 좌우 병합
            return [first_line, second_line] + lines, n + m + u, max(p, q) + 2, n + u // 2

        lines, *_ = _display_aux(self.binarytree)  # 트리 시각화 문자열 생성
        for line in lines:                         # 줄 단위로 출력
            print(line)
bst = BinarySearchTree()
print('bst.insert(37)')
bst.insert(53)
bst.show_tree()  # 편향된 트리
print('bst.insert([10, 20, 30, 40, 50, 60, 70, 80,90,100])')
bst.insert([10, 20, 30, 40, 50, 60, 70, 80,90,100])
bst.show_tree()  # 편향된 트리

bst.rebalance_with([25, 35, 45])  # 기존 값 + 새 값 병합 후 균형 재구성
print(bst.rebalance_with([25, 35, 45]))
bst.show_tree()  # 균형 잡힌 트리 출력
print('bst.delete(30)')
bst.delete(30)
bst.show_tree()  # 균형 잡힌 트리 출력
print('bst.insert(37)')
bst.insert(37)
bst.show_tree()  # 균형 잡힌 트리 출력