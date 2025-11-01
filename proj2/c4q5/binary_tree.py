class Node:  # 트리의 각 노드를 정의하는 클래스
    def __init__(self, key):  # 노드 생성자
        self.key = key        # 노드에 저장할 값
        self.left = None      # 왼쪽 자식 노드
        self.right = None     # 오른쪽 자식 노드

class BinarySearchTree:  # 이진 탐색 트리 클래스
    def __init__(self):  # 트리 생성자
        self.binarytree = None  # 루트 노드를 초기화

    def insert(self, key):  # 새로운 값을 트리에 삽입하는 함수 (중복 허용)
        def _insert(root, key):  # 재귀적으로 삽입을 수행하는 내부 함수
            if root is None:  # 현재 위치가 비어있으면
                return Node(key)  # 새 노드를 생성하여 반환
            if key < root.key:  # 삽입할 값이 현재 노드보다 작으면
                root.left = _insert(root.left, key)  # 왼쪽 서브트리에 삽입
            else:  # 삽입할 값이 현재 노드보다 크거나 같으면
                root.right = _insert(root.right, key)  # 오른쪽 서브트리에 삽입 (중복 포함)
            return root  # 변경된 루트 노드를 반환

        self.binarytree = _insert(self.binarytree, key)  # 루트부터 삽입 시작

    def find(self, key):  # 특정 값을 트리에서 찾는 함수
        def _find(root, key):  # 재귀적으로 탐색을 수행하는 내부 함수
            if root is None:  # 노드가 없으면
                return False  # 값을 찾지 못함
            if key == root.key:  # 값이 일치하면
                return True  # 값을 찾음
            elif key < root.key:  # 찾을 값이 현재 노드보다 작으면
                return _find(root.left, key)  # 왼쪽 서브트리에서 탐색
            else:  # 찾을 값이 현재 노드보다 크면
                return _find(root.right, key)  # 오른쪽 서브트리에서 탐색

        return _find(self.binarytree, key)  # 루트부터 탐색 시작

    def delete(self, key):  # 특정 값을 트리에서 삭제하는 함수
        def _delete(root, key):  # 재귀적으로 삭제를 수행하는 내부 함수
            if root is None:  # 노드가 없으면
                return None  # 아무 것도 삭제하지 않음
            if key < root.key:  # 삭제할 값이 현재 노드보다 작으면
                root.left = _delete(root.left, key)  # 왼쪽 서브트리에서 삭제
            elif key > root.key:  # 삭제할 값이 현재 노드보다 크면
                root.right = _delete(root.right, key)  # 오른쪽 서브트리에서 삭제
            else:  # 삭제할 노드를 찾은 경우
                if root.left is None:  # 왼쪽 자식이 없으면
                    return root.right  # 오른쪽 자식을 반환
                elif root.right is None:  # 오른쪽 자식이 없으면
                    return root.left  # 왼쪽 자식을 반환
                min_larger_node = self._find_min(root.right)  # 오른쪽 서브트리에서 최소값 노드 찾기
                root.key = min_larger_node.key  # 현재 노드 값을 최소값으로 교체
                root.right = _delete(root.right, min_larger_node.key)  # 최소값 노드를 삭제
            return root  # 변경된 루트 노드를 반환

        self.binarytree = _delete(self.binarytree, key)  # 루트부터 삭제 시작

    def _find_min(self, node):  # 서브트리에서 최소값 노드를 찾는 함수
        current = node  # 현재 노드를 시작점으로 설정
        while current.left is not None:  # 가장 왼쪽 노드까지 이동
            current = current.left
        return current  # 최소값 노드를 반환

    def inorder(self):  # 중위 순회 결과를 리스트로 반환하는 함수
        def _inorder(root):  # 재귀적으로 중위 순회를 수행하는 내부 함수
            return _inorder(root.left) + [root.key] + _inorder(root.right) if root else []  # 왼쪽 → 현재 → 오른쪽 순서
        return _inorder(self.binarytree)  # 루트부터 순회 시작



def main():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)

    print("Find 60:", bst.find(60))  # True
    print("Find 25:", bst.find(25))  # False

    bst.delete(70)
    print("Inorder traversal after deleting 70:", bst.inorder())

if __name__ == "__main__":
    main()