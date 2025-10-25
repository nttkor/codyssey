1. LinkedList, CirculaList
   0. class Node(self,data):  (문제에는 없지만 구현해야함)
      1. self.data = data 
      2. self.next = None 구현해야함
   1. LinkedList 구현사항
      1. 문제에는 없지만 def __init__(self): self.head = None구현해야함
      2. insert(self,index,value) : 0<= index < last 범위 벗어나는 index, raise IndexError 처리
         1. self.head에 데이터가 없는 경우 있는 경우, index가 범위를 벗어나는 경우를 구분해서 return값및 에러 처리해야함
      3. delete(self,index) : index 범위 벗어 날경우 raise IndexError
      4. to_list(self) : 
      5. __len__(self)->int : 노드수 반환
      6. 문제에는 없지만 디버깅을 위해 disply를 만들자
   2. CircularList 구현 사항, last를 cursor라고 표현
      1. 문제에는 없지만 def __init__(self): self.last = None 구현으로 시작
      2. insert(self,value)
         1. 추가시 self.last가 비었는지, 있는지 마지막인지를 잘 구분해서 처리해야함
      3. delete(self,value)
         1. 지울때도 없을때, 하나 있을때, 없을때 등등 상황 처리를 잘해야함
      4. get_next(self) : 이건 last포인트를 last.next(즉 맨 처음)으로 바꾸고 출력하는것
         1. self.last = self.last.next, return self.last.data(이전의 head data)
      5. search(value) 아까 delete와 비슷 찾아지면 data return 하면 됨
      6. 문제에는 없지만 디버깅을 위해 disply를 만들자
      7. 구현후 모든 경우의 수 체크해보자
2. Stack
   1. 용량 10개로 고정 : 난 고정하지 않고 그때 그때 len(list)로 체크했음
      1. class Stack: def __init__(): self.data = list() #노드 없이 리스트를 이용 구현했음
   2. push(self, value) -> bool
      1. value 추가후 true반환
      2. stack이 가득찬 경우 경고후 False
      3. stack is Full
   3. pop(self)
      1. stack의 마지막을 꺼낸다
      2. 비어있는 empty출력후 None
   4. empty(self) : 비어 있으면 True, 아니면 False
   5.  peek(self) : 스택의 맨위를 반환, 비어 있으면 Stack is Empty 출력후 None반환
3. pandas
   1. abalone_minimax.py로 파일 만들것
   2. 표준라이브러리 pands사용가능 scikitlearn금지
   3. 입출력/인코딩 파일경로 고정
   4. load_attributes(), load_data(), make_label(df), min_max_manual(df) 등으로 함수 분리
   5. 상수열(분모0) 에외처리 로직 포함)
   6. 출력규칙, 위 3개 print()수행 부가 출력 금지, 문자열은 "" , 
   7. zip을 다운 받아 풀면 
   8. abalone data.txt? data 수치만 들어 있음 컴마로 분리됨, 2, M, 0.35, 0.265  ..................
   9. abalone_attribute.txt 헤더가 들어 있음 
      1.  attibute, 
      2.  2.Leighth, 
      3.  3.Diameter
      4.  4.Height
      5.  5.Whole weight
      6.  6.Shucked weight
      7.  7.viscera weight
      8.  8.shell weight
      9.  9.rings
   10. 제공된 두 파일을 읽어 하나의 dataframe으로 구성. 
   11. 전복은 유아기에는 성별이 정해지지 않다가 성장하면서 성별이 정해지는 특성으로 sex컬럼을 별도로 label 컬럼으로 분리후 원본 sex컬럼제거.
   12. 이후 label제외한 모든 수치컬럼에 대해 min max scaling을 직접 수식으로 구현해서 적용
   13. 요구사항 충족하는 프로그램 작성
   14. 데이터 적재
   15. 현재 작업 디렉토리의 abalone_sttribte.txt에서 열이름 목록ㅇㄹ 읽어 (행단위 텍스트->리스트) 같은 디렉토리의 abalon.txt 콤마를 읽어 pandas.dataframe을 생성
   16. 앞서 읽은 열이름을 컴럼명으로 적용
   17. 라벨분리, sex컬럼을 그대로 복사 label컬럼을 만들고 [예 'M','F'] 원본 sex컴럼은 제거한다.
   18. 결과 table에는 label만 남김
   19. 스케일링 대상/ 방법
   20. label을 제외한 모든 수치컬럼에 대해 열별로 min-max scaling (직접수식)을 적용한다
   21. x'=max(x)-min(x)x-min(x)
   22. x'' = x-min(x)max(x)-min(x)
   23. x' = \frac{x-\min(x)|{\max(x)-\min(x)}}
   24. 분모가 0(상수열)인 경우 해달열을 0.0 으로 채워줌
   25. 출력형식 print() 총 3번
   26. 원본 data frame 모양 df.shape <-예(N,9)
   27. 라벨 분포 label value-counts().to_dict()
   28. 스케일결과의 상,하한요약 
   29. scaled.describe().loc[[min,max]].round(6).to_dict]
   30. 대상열들의 상,하한 요약
   31. scaled.describe().loc[[min,max]].round(6).to_dict]
   32. (대상열들의 min=0.0, max=1.0임을 확인)
   33. 예외처리 (우선순위)
       1.  1. 파일열기 실패 File open error
       2.  2. 디코딩 에러 Decoding error
       3.  3. 피싱/스케일링 단계, 기타 오류 - processing error
       4.  각 경우 정확한 문자열을 print()하고 return 으로 종료 (sys,exit()금지)
   34. 다운 받아서 풀면 다음 파일이 있다. 
   35. 