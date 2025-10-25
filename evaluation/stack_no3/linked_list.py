# test_linked_list_strict.py

from linked_list import LinkedList, Node

def check_node_structure(node):
    """Node 내부 구조 검사"""
    assert isinstance(node, Node), "Object is not Node"
    assert hasattr(node, "data"), "Node missing 'data'"
    assert hasattr(node, "next"), "Node missing 'next'"

def check_linked_list_structure(ll, expected_values):
    """LinkedList 내부 구조 검사"""
    assert isinstance(ll, LinkedList), "Object is not LinkedList"
    current = ll.head
    for val in expected_values:
        assert current is not None, "Node missing in list"
        check_node_structure(current)
        assert current.data == val, f"Expected {val}, got {current.data}"
        current = current.next
    assert current is None, "Extra nodes exist after expected elements"

def test_append():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    check_linked_list_structure(ll, [1,2,3])

def test_prepend():
    ll = LinkedList()
    ll.prepend(10)
    ll.prepend(5)
    check_linked_list_structure(ll, [5,10])

def test_insert():
    ll = LinkedList()
    ll.append(1)
    ll.append(3)
    ll.insert(1, 2)  # 1 -> 2 -> 3
    ll.insert(0, 0)  # 0 -> 1 -> 2 -> 3
    ll.insert(4, 4)  # 0 -> 1 -> 2 -> 3 -> 4
    check_linked_list_structure(ll, [0,1,2,3,4])

def test_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(2)
    check_linked_list_structure(ll, [1,3])
    ll.delete(1)
    check_linked_list_structure(ll, [3])
    ll.delete(3)
    check_linked_list_structure(ll, [])

def test_find():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    node = ll.find(5)
    check_node_structure(node)
    assert node.data == 5
    assert ll.find(100) is None

def test_len():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    ll.append(2)
    assert len(ll) == 2
    ll.delete(1)
    assert len(ll) == 1

def test_combined():
    ll = LinkedList()
    ll.append(1)
    ll.append(3)
    ll.insert(1,2)
    ll.prepend(0)
    ll.delete(2)
    check_linked_list_structure(ll, [0,1,3])
    assert len(ll) == 3
    node = ll.find(1)
    check_node_structure(node)

if __name__ == "__main__":
    tests = [
        test_append,
        test_prepend,
        test_insert,
        test_delete,
        test_find,
        test_len,
        test_combined
    ]
    for test in tests:
        test()
    print("All strict tests passed successfully!")
