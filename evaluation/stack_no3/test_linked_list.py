# test_linked_list.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linked_list import LinkedList, Node

def test_append_and_print():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert str_list(ll) == "1 -> 2 -> 3", "Append failed"

def test_prepend():
    ll = LinkedList()
    ll.prepend(10)
    ll.prepend(5)
    assert str_list(ll) == "5 -> 10", "Prepend failed"

def test_insert_middle():
    ll = LinkedList()
    ll.append(1)
    ll.append(3)
    ll.insert(1, 2)
    assert str_list(ll) == "1 -> 2 -> 3", "Insert middle failed"

def test_insert_head():
    ll = LinkedList()
    ll.append(2)
    ll.insert(0, 1)
    assert str_list(ll) == "1 -> 2", "Insert head failed"

def test_insert_out_of_bounds():
    ll = LinkedList()
    ll.append(1)
    try:
        ll.insert(5, 10)
        assert False, "Insert out of bounds should raise IndexError"
    except IndexError:
        pass

def test_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(2)
    assert str_list(ll) == "1 -> 3", "Delete middle failed"
    ll.delete(1)
    assert str_list(ll) == "3", "Delete head failed"
    ll.delete(3)
    assert str_list(ll) == "", "Delete last failed"
    ll.delete(100)  # 삭제되지 않는 값
    assert str_list(ll) == "", "Delete non-existent should not change list"

def test_find():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    node = ll.find(5)
    assert node is not None and node.data == 5, "Find existing failed"
    assert ll.find(100) is None, "Find non-existing failed"

def test_len():
    ll = LinkedList()
    assert len(ll) == 0, "Length of empty list failed"
    ll.append(1)
    ll.append(2)
    assert len(ll) == 2, "Length after append failed"
    ll.delete(1)
    assert len(ll) == 1, "Length after delete failed"

def test_combined_operations():
    ll = LinkedList()
    ll.append(1)
    ll.append(3)
    ll.insert(1, 2)
    ll.prepend(0)
    assert str_list(ll) == "0 -> 1 -> 2 -> 3", "Combined operations failed"
    ll.delete(2)
    assert str_list(ll) == "0 -> 1 -> 3", "Delete after combined operations failed"

def str_list(ll):
    """연결 리스트를 문자열로 반환"""
    current = ll.head
    elements = []
    while current:
        elements.append(str(current.data))
        current = current.next
    return " -> ".join(elements)

if __name__ == "__main__":
    tests = [
        test_append_and_print,
        test_prepend,
        test_insert_middle,
        test_insert_head,
        test_insert_out_of_bounds,
        test_delete,
        test_find,
        test_len,
        test_combined_operations
    ]

    for test in tests:
        test()
    print("All tests passed successfully!")
