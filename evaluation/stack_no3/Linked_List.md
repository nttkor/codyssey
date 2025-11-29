요청하신 대로 **단일 연결 리스트(LinkedList)**와 **원형 연결 리스트(CircularList)**의 동작 방식을 쉽게 설명하고, 이어서 텍스트 기반의 다이어그램으로 구조를 시각화해 드리겠습니다.

---

## 🔗 1. 단일 연결 리스트 (LinkedList) 동작 방식 설명

연결 리스트는 데이터를 담는 **노드(Node)**들이 체인처럼 연결된 구조입니다. 배열처럼 연속된 메모리 공간을 사용하지 않고, 각 노드가 다음 노드의 위치를 가리키는 **포인터(Pointer)**를 가지고 연결됩니다.

### 주요 개념

* **노드 (Node):** 실제 데이터(`data`)와 다음 노드를 가리키는 주소(`next`) 두 부분으로 구성됩니다.
* **헤드 (Head):** 리스트의 **가장 첫 번째** 노드를 가리키는 포인터입니다. 리스트의 시작점이죠.
* **삽입 (Insert):** 원하는 위치에 새 노드를 넣을 때는, 새 노드를 그 위치의 **이전 노드**와 **다음 노드** 사이에 연결하는 과정만 필요합니다. 메모리를 이동할 필요가 없어 배열보다 효율적일 수 있습니다.
* **삭제 (Delete):** 노드를 삭제할 때는, **이전 노드**의 `next` 포인터가 삭제될 노드를 건너뛰고 **그 다음 노드**를 가리키도록 연결을 바꾸기만 하면 됩니다.

### LinkedList 텍스트 다이어그램

| **Head 포인터** | **노드 1** | **노드 2** | **노드 3** | **마지막 노드** |
| :-------------: | :--------: | :--------: | :--------: | :-------------: |
| $\downarrow$ | | | | |
| **`self.head`** $\longrightarrow$ | **[Data 1 \| next]** $\longrightarrow$ | **[Data 2 \| next]** $\longrightarrow$ | **[Data 3 \| next]** $\longrightarrow$ | **[Data N \| None]** |

네, 요청하신 대로 그림 문자를 사용하여 `LinkedList`의 `insert` 과정, 특히 `index - 1`만큼 이동하여 삽입하는 과정을 시각적으로 설명해 드릴게요.

-----

## 🔗 LinkedList `insert(index, value)` 다이어그램

**목표:** `index = 2` 위치에 `Value 'C'`를 삽입한다고 가정합니다.

**초기 리스트 상태:**

```
[ Head ]
   |
   V
[Node 'A' | next] --> [Node 'B' | next] --> [Node 'D' | next] --> [Node 'E' | None]
   (idx 0)              (idx 1)              (idx 2)              (idx 3)
```

**1. `new_node = Node('C')` 생성:**

```
[New Node 'C' | next=None]
```

**2. `index - 1` 만큼 이동 (`for _ in range(index - 1)`):**

  * `index = 2` 이므로 `range(2 - 1)` 즉, `range(1)` 만큼 반복합니다.
  * `current` 포인터는 `self.head` (`Node 'A'`)에서 시작합니다.
  * `current = current.next`를 1회 실행합니다.

<!-- end list -->

```
[ Head ]
   |
   V
[Node 'A' | next] --> [Node 'B' | next] --> [Node 'D' | next] --> [Node 'E' | None]
   (idx 0)              (idx 1)              (idx 2)              (idx 3)
                        ^
                        |
                       [current]  <-- current가 Node 'B'를 가리키게 됨 (삽입 위치의 이전 노드)
```

**3. 포인터 재배치 (`new_node.next = current.next`):**

  * `current.next`는 현재 `Node 'D'`를 가리키고 있습니다.
  * `new_node`의 `next`가 `Node 'D'`를 가리키도록 변경합니다.

<!-- end list -->

```
[ Head ]
   |
   V
[Node 'A' | next] --> [Node 'B' | next] --> [Node 'D' | next] --> [Node 'E' | None]
   (idx 0)              (idx 1)              (idx 2)              (idx 3)
                        ^                      ^
                        |                      |
                       [current]  [New Node 'C' | next] 

                                       

```

**4. 포인터 재배치 (`current.next = new_node`):**

  * `current` (`Node 'B'`)의 `next`가 `new_node` (`Node 'C'`)를 가리키도록 변경합니다.

<!-- end list -->

```
[ Head ]
   |
   V
[Node 'A' | next] --> [Node 'B' | next] --> [New Node 'C' | next] --> [Node 'D' | next] --> [Node 'E' | None]
   (idx 0)              (idx 1)                                        (idx 3)              (idx 4)
                        ^
                        |
                       [current]
```

**최종 리스트 상태:**

```
[ Head ]
   |
   V
[Node 'A' | next] --> [Node 'B' | next] --> [Node 'C' | next] --> [Node 'D' | next] --> [Node 'E' | None]
   (idx 0)              (idx 1)              (idx 2)              (idx 3)              (idx 4)
```

이제 `Value 'C'`를 가진 새로운 노드가 `index 2` 위치에 성공적으로 삽입되었습니다\!http://googleusercontent.com/image_generation_content/0

---

## 🔄 2. 원형 연결 리스트 (CircularList) 동작 방식 설명

원형 연결 리스트는 단일 연결 리스트와 구조는 같지만, **마지막 노드**의 포인터가 `None`을 가리키는 대신 **다시 리스트의 첫 번째 노드**를 가리키며 원을 만듭니다.

### 주요 개념

* **Last 포인터 (Cursor):** 원형 리스트에서는 리스트의 시작점인 `head` 대신 **마지막 노드**를 가리키는 `self.last` 포인터를 주로 사용합니다.
* **특징:** `self.last`의 다음 노드(`self.last.next`)는 **항상 리스트의 첫 번째 노드(Head)**가 됩니다. 이 구조를 통해 리스트의 삽입과 삭제 연산을 `O(1)`의 시간 복잡도로 빠르게 처리할 수 있습니다.
* **삽입 (Insert):** 새로운 노드를 `self.last` 뒤에 추가한 후, 새 노드를 새로운 `self.last`로 지정하면 됩니다. 이는 리스트의 시작점(Head)을 변경하지 않고도 효율적으로 끝에 추가하는 방법입니다.
* **회전 (Rotation):** `get_next()` 메서드를 사용해 `self.last = self.last.next`와 같이 포인터를 한 칸 이동시키면, 리스트 전체가 회전하는 효과를 얻을 수 있습니다.

### CircularList 텍스트 다이어그램

| **Last 포인터** | **노드 (Last)** | **노드 (Head)** | **노드 2** |
| :-------------: | :--------------: | :---------------: | :---------: |
| $\downarrow$ | | | |
| **`self.last`** $\longrightarrow$ | **[Data N \| next]** | **[Data 1 \| next]** $\longrightarrow$ | **[Data 2 \| next]** |
| | $\uparrow$ $\text{---------------------------------------------------------}$ $\downarrow$ | | |
| | $\text{<-----------------------}$ $\text{순환 연결}$ $\text{------------------------>}$ | | |

