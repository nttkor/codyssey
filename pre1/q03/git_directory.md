# 📁 버전 관리 시스템의 종류

버전 관리 시스템(Version Control System, VCS)은 소스 코드나 문서의 변경 사항을 관리하고 추적하는 도구입니다. 대표적인 종류는 다음과 같습니다.

## 1. 로컬 버전 관리 시스템 (Local VCS)

- **설명:** 파일의 변경 이력을 로컬 컴퓨터에만 저장하는 방식입니다.
- **예시:** RCS(Revision Control System)
- **장점:** 빠른 속도, 외부 연결 불필요
- **단점:** 다른 사람과의 협업이 어려움

---

## 2. 중앙 집중식 버전 관리 시스템 (Centralized VCS)

- **설명:** 버전 이력을 중앙 서버에서 관리하고, 사용자는 서버에서 코드를 내려받아 사용합니다.
- **예시:** CVS, Subversion(SVN), Perforce
- **장점:** 중앙 관리로 협업 용이
- **단점:** 서버 장애 시 전체 작업 중단 가능

---

## 3. 분산 버전 관리 시스템 (Distributed VCS)

- **설명:** 각 사용자가 전체 저장소를 복제(clone)하여 로컬에서 작업 가능하며, 중앙 서버 없이도 독립적으로 작업할 수 있습니다.
- **예시:** Git, Mercurial, Bazaar
- **장점:** 오프라인에서도 작업 가능, 백업 용이
- **단점:** 초기 학습 곡선이 있음

---

## Git 주요 저장소 구조


Git 프로젝트를 관리할 때, 원격 저장소(Remote Repository)를 제외하고, 저장소는 크게 세 부분으로 나뉩니다.

- Working Directory (작업 디렉토리, 워킹트리)
- Staging Area (스테이징 영역)
- Local Repository (로컬 저장소)
- Working Directory는 실제 코드 파일이 있는 공간이고, Staging Area와 Local Repository는 이와 연결된 Git 내부의 개념적인 저장소입니다.

| 영역           | 설명              |
|---------------------------|-------------------------|
| Working Directory (작업 디렉터리, 워킹트리) | 실제 파일이 존재하는 공간 (사용자가 직접 작업하는 영역)               |
| Staging Area (스테이징 영역)             | 커밋할 파일을 임시 저장하는 공간 (git add 시 반영됨)                  |
| Local Repository (로컬 저장소)           | 커밋된 파일들이 저장되는 공간 (git commit 시 반영됨)                  |
| Remote Repository (원격 저장소)          | GitHub, GitLab 등에 위치한 원격 저장소 (git push로 업로드)            |

##  Working Directory(작업 디렉토리)와 Working Tree(워킹 트리)는 같은 개념을 의미합니다.

우리가 편집하고 수정하는 모든 파일이 존재하는 공간이며, Git이 관리하는 .git 폴더를 제외한 나머지 영역이 워킹트리에 해당됩니다.
Git이 변경 사항을 추적하고 있지만, 아직 Git 저장소(로컬 저장소)에 기록되지 않은 상태입니다.

Git이 관리하지 않는 폴더를 워킹트리로 만들기
Git이 관리하지 않는 폴더를 Git 저장소로 만들고, 워킹트리로 전환하려면 git init 명령어를 실행해야 합니다.

예시
mkdir my-project
cd my-project
git init
출력 예시
Initialized empty Git repository in /Users/username/my-project/.git/
위 예시의 my-project 폴더는 Git이 추적하는 워킹트리가 됩니다. 기존 파일이 있다면 그대로 유지되며, 새로운 .git 폴더가 생성됩니다.
즉, Git이 관리하지 않던 프로젝트(폴더)를 워킹트리로 변경하는 과정이 git init입니다.


Git 저장소 내부 구조
Git이 관리하는 프로젝트에는 .git 디렉터리가 있으며, 이 내부에서 Git의 주요 데이터가 저장됩니다. 이 .git 디렉터리가 중요한 역할을 합니다.

Git의 내부 파일 구조를 보면, Staging Area와 Local Repository는 .git 디렉터리 내부에 따로 존재합니다.

-- Git 프로젝트 디렉터리 (Working Directory) 예시
```
/my-git-project  (Working Directory)
├── .git/        (Git 저장소, Local Repository + Staging Area 포함)
│   ├── objects/         (모든 커밋, 블롭, 트리 저장)
│   ├── refs/            (브랜치 및 태그 정보)
│   ├── HEAD             (현재 체크아웃된 브랜치)
│   ├── index            (Staging Area 정보 저장)
│   ├── config           (Git 설정 파일)
│   ├── logs/            (브랜치 변경 이력)
│   └── ... (다른 Git 내부 파일들)
│
├── src/        (소스 코드, Working Directory)
└── README.md   (일반 파일, Working Directory)
```
# 📂 `.git` 디렉토리의 역할

`.git` 디렉토리는 Git 저장소의 핵심 정보를 담고 있는 숨김 디렉토리입니다. 프로젝트 루트에 생성되며, Git이 이 디렉토리를 기준으로 저장소로 인식합니다.

## 주요 역할

- **버전 이력 저장:** 커밋 정보, 브랜치, 태그 등의 모든 변경 기록을 저장합니다.
- **객체 데이터 관리:** Git 객체(Blob, Tree, Commit, Tag 등)를 저장하는 `objects` 디렉토리를 포함합니다.
- **설정 정보:** 저장소에 대한 설정(`config` 파일), 사용자 정보 등을 포함합니다.
- **HEAD 파일:** 현재 체크아웃된 브랜치 정보를 포함합니다.
- **Ref 정보:** 브랜치와 태그의 포인터를 관리합니다 (`refs/heads/`, `refs/tags/`).

### Git 저장소 설명
Git 저장소에는 .git/index 파일과 .git/objects/ 폴더가 있습니다.

.git/index
Staging Area(스테이징 영역) 정보가 저장되는 곳
git add를 실행하면, 변경된 파일의 체크섬(SHA-1 해시값)과 파일 정보가 기록됨
하지만 실제 파일의 내용이 저장되는 것은 아니고, 해당 Blob 객체를 가리키는 ID만 저장됨
즉, .git/index는 Git이 어떤 파일이 스테이징 되었는지 기억하는 “목록” 같은 역할을 합니다.

git add <파일명>
위 명령어를 실행하면, 파일이 Staging Area에 추가되며 .git/index에 정보가 저장됩니다.

.git/objects/ (Git 객체 저장소)
Git이 저장하는 모든 객체(Blob, Tree, Commit)가 보관됨
Git은 파일을 직접 저장하지 않고, 파일의 내용을 스캔한 후 SHA-1 해시값으로 변환하여 저장
이 폴더 내부에는 Blob(파일 내용), Tree(파일 구조), Commit(커밋 정보) 객체가 저장됨
Git 객체(Blob, Tree, Commit) - objects 폴더 내부에 위치
Git은 내부적으로 3가지 주요 객체(Blob, Tree, Commit)를 이용해 변경 사항을 추적합니다.

###  objects 폴더 구조 예시:
```
.git/objects/
├── e6/
│   └── 9de29bb2d1d6434b8b29ae775ad8c2e48c5391  # Blob 객체
├── d1/
│   └── abcdef1234567890abcdef1234567890abcdef  # Tree 객체
└── 21/
    └── fedcba0987654321fedcba0987654321fedcba  # Commit 객체
```

.git/objects/ 내부에는 폴더명(2글자) + 파일명(38글자)로 된 파일이 있으며, 이 조합이 SHA-1 해시값(객체 ID)
Git은 이 해시값을 기반으로 파일 내용을 관리하며, 같은 내용이면 중복 저장하지 않음
1. Blob (파일 내용 저장)
git add 실행 시, 파일 자체가 아닌, 파일 내용을 SHA-1 해시값으로 변환한 후 Blob 객체로 저장
같은 내용의 파일은 같은 Blob 객체를 사용하여 중복 저장 방지
index 파일에는 Blob 객체의 ID(체크섬)가 저장됨
object 폴더 내의 폴더명(2글자)과 그 폴더 안의 파일명(38글자)을 합친 40자리 SHA-1 해시값(체크섬)이 Blob 객체의 ID입니다. index 파일에는 이 Blob 객체의 ID(체크섬)가 올라갑니다.

2. Tree (폴더 및 파일 구조 저장)
파일과 디렉터리의 구조를 저장하는 객체
git commit을 실행하면, 현재 스테이징된 파일들의 Blob ID, 파일명, 디렉토리 정보를 하나로 묶어 Tree 객체를 생성
Tree 객체는 특정 커밋 시점에서 어떤 파일이 어디에 있는지를 기록하는 역할
3. Commit (커밋 정보 저장)
git commit 실행 시, 현재 Tree 객체를 가리키는 Commit 객체가 생성됨
Commit 객체는 이전 커밋과의 관계(부모 커밋), 작성자 정보, 커밋 메시지 등 포함
해당 커밋이 어떤 트리(Tree) 객체를 참조하는지 확인 가능


Git 워크플로와 저장소 관계
Git은 다음과 같은 과정을 통해 파일을 저장하고 관리합니다.


git add → Staging Area
작업 디렉토리에서 변경된 파일을 Staging Area(스테이징 영역)에 추가
.git/index 파일이 업데이트됨 (Blob 객체의 ID가 저장됨)
git commit → Local Repository
Staging Area에 있는 변경 사항을 Local Repository에 기록
Git은 Tree 객체를 생성하고, 이 Tree를 가리키는 Commit 객체를 생성
.git/objects/ 내부에 Commit & Tree 객체가 저장됨
git push → Remote Repository
Local Repository의 변경 사항을 GitHub, GitLab 등의 원격 저장소에 업로드
git pull을 실행하면 원격 저장소의 최신 변경 사항을 가져옴