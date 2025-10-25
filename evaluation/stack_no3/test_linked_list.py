# test_linked_list_ultra_strict.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linked_list import LinkedList, Node

def check_node(node, expected_data=None, next_expected_type=Node):
    """Node 내부 구조와 연결 검사"""
    assert isinstance(node, Node), f"Object {node} is not Node"
    assert hasattr(node, "data"), "Node missing 'data'"
    assert hasattr(node, "next"), "Node missing 'next'"
    if expected_data is not None:
        assert node.data == expected_data, f"Expected {expected_data}, got {node.data}"
    if node.next is not None:
        assert isinstance(node.next, next_expected_type), "Next node type incorrect"

def check_list_sequence(ll, expected_values):
    """LinkedList 전체 연결 구조 확인"""
    assert isinstance(ll, LinkedList), "Object is not LinkedList"
    current = ll.head
    for val in expected_values:
        assert current is not None, f"Missing node for value {val}"
        check_node(current, val)
        current = current.next
    assert current is None, "Extra nodes exist after expected elements"

def test_append():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    # 초엄격 검사: 각 노드가 올바르게 연결되어 있는지
    current = ll.head
    expected = [1,2,3]
    for i, val in enumerate(expected):
        assert current is not None
        check_node(current, val)
        if i < len(expected)-1:
            assert current.next is not None
        else:
            assert current.next is None
        current = current.next
    check_list_sequence(ll, expected)

def test_insert_and_pointers():
    ll = LinkedList()
    ll.append(10)
    ll.append(30)

    # insert 중간
    ll.insert(1, 20)
    current = ll.head
    # 초엄격: insert 후 포인터가 올바르게 연결되었는지 확인
    assert current.data == 10
    assert current.next.data == 20
    assert current.next.next.data == 30
    assert current.next.next.next is None
    check_list_sequence(ll, [10,20,30])

    # insert head
    ll.insert(0, 5)
    assert ll.head.data == 5
    check_list_sequence(ll, [5,10,20,30])

def test_delete_and_pointers():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)

    # delete middle
    ll.delete(2)
    current = ll.head
    assert current.data == 1
    assert current.next.data == 3
    assert current.next.next is None
    check_list_sequence(ll, [1,3])

    # delete head
    ll.delete(1)
    assert ll.head.data == 3
    assert ll.head.next is None
    check_list_sequence(ll, [3])

    # delete last
    ll.delete(3)
    assert ll.head is None
    check_list_sequence(ll, [])

def test_find_and_node_integrity():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    node = ll.find(5)
    check_node(node, 5)
    node = ll.find(100)
    assert node is None

def test_len_and_structure():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    ll.append(2)
    assert len(ll) == 2
    ll.delete(1)
    assert len(ll) == 1

def test_combined_operations_strict():
    ll = LinkedList()
    ll.append(1)
    ll.append(3)
    ll.insert(1,2)
    ll.prepend(0)
    ll.delete(2)

    # 최종 구조 점검
    expected = [0,1,3]
    current = ll.head
    for val in expected:
        assert current is not None
        check_node(current, val)
        current = current.next
    assert current is None
    check_list_sequence(ll, expected)
    assert len(ll) == 3
    node = ll.find(1)
    check_node(node, 1)

if __name__ == "__main__":
    tests = [
        test_append,
        test_insert_and_pointers,
        test_delete_and_pointers,
        test_find_and_node_integrity,
        test_len_and_structure,
        test_combined_operations_strict
    ]
    for test in tests:
        test()
    print("All ultra-strict tests passed successfully!")
