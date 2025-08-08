# Git 저장소 clone하기

```bash
git clone [복사한 URL] [DIR]
```

#4. clone한 저장소의 원격 저장소 위치 확인하기
GitHub에서 저장소를 클론하면 origin remote에 GitHub 저장소 주소가 저장됩니다. 이후에는 저장소 주소를 지정하지 않더라도 origin이라는 이름으로 원격 저장소의 내용을 fetch해오거나, 로컬 변경사항을 push할 수 있습니다. 
아래 명령어를 통해 클론한 저장소의 remote 정보를 확인할 수 있습니다. 

```bash
git remote -v
```