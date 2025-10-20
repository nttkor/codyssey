## 1.새브런치를 만들고 즉시 그 브랜치로 전환
- git checkout -b new 
## 2. 가장 최근 커밋의 커밋메세지만 수정하는 명령어
- git commit --amend
## 3. 병합도중 충돌이 발생 병함이 중단된 상황에서 이를 되돌리는 명령어
- git merge --abort
4,5,6, 한묶음 function이름도 q4, q5, q6으로 해야함
## 4. 원격저장소의 최신 커밋 정보를 가져오기만하고 자동병합하지 않는 명령어
- git fetch
## 5. 현재 브랜치를 원격브랜치 origin/new_feature와 upstream 추적만 설정하는 명령어
- git branch -u origin/new-feature
# 6. 최근 커밋은 취소하돼 변경내용은 스테이징 상태유지
- git reset --soft HEAD^