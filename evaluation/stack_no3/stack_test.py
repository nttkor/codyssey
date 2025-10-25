import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stack_adt import Stack
# VS Code 등에서 상대경로 문제 방지


def check_stack(stack_class):
    print("=== Stack Test ===")
    s = stack_class()

    # 1. empty() 체크
    try:
        assert s.empty() == True
        print("empty() OK")
    except AssertionError:
        print("ERROR: empty() failed")

    # 2. push / overflow 체크
    print("Push 12 items (capacity=10)")
    for i in range(12):
        result = s.push(i)
        if i >= 10:
            if result is not False:
                print(f"ERROR: push overflow at {i}, expected False, got {result}")
        else:
            if result is not True:
                print(f"ERROR: push failed at {i}, expected True")

    # 3. peek 체크
    try:
        top = s.peek()
        assert top == 9
        print("peek() OK, top =", top)
    except AssertionError:
        print(f"ERROR: peek() returned {top}, expected 9")

    # 4. pop / LIFO 체크
    print("Pop all items")
    expected = list(range(9, -1, -1))
    for val in expected:
        popped = s.pop()
        if popped != val:
            print(f"ERROR: pop() returned {popped}, expected {val}")

    # 5. underflow 체크
    print("Pop from empty stack")
    under = s.pop()
    if under is not None:
        print(f"ERROR: pop() on empty stack should return None, got {under}")

    # 6. peek on empty
    empty_peek = s.peek()
    if empty_peek is not None:
        print(f"ERROR: peek() on empty stack should return None, got {empty_peek}")

    # 7. empty() 체크
    if s.empty() != True:
        print("ERROR: empty() should return True after all pops")
    else:
        print("empty() OK after all pops")


if __name__ == "__main__":
    check_stack(Stack)
