# Git 주요 명령어 (git help)

아래는 다양한 상황에서 사용되는 일반적인 Git 명령어들입니다:

---

## 작업 영역 시작 (참고: git help tutorial)

* **`clone`**: 저장소를 새 디렉터리로 복제합니다.  git clone https://github.com/nttkor/david
* **`init`**: 비어 있는 Git 저장소를 생성하거나 기존 저장소를 다시 초기화합니다.

---

## 현재 변경 사항 작업 (참고: git help everyday)

* **`add`**: 파일 내용을 인덱스(스테이징 영역)에 추가합니다.
* **`mv`**: 파일, 디렉터리 또는 심볼릭 링크(symlink)를 이동하거나 이름을 변경합니다. commit -m "message" 휴에 사용합니다.
* **`restore`**: 작업 트리(working tree) 파일을 복원합니다.
* **`rm`**: 작업 트리와 인덱스에서 파일을 제거합니다.

---

## 히스토리 및 상태 확인 (참고: git help revisions)

* **`bisect`**: 이진 탐색을 사용하여 버그를 유발한 커밋을 찾습니다.
* **`diff`**: 커밋 간, 커밋과 작업 트리 간의 변경 사항 등을 보여줍니다.
* **`grep`**: 패턴과 일치하는 줄을 출력합니다.
* **`log`**: 커밋 로그를 보여줍니다.
* **`show`**: 다양한 유형의 객체들을 보여줍니다.
* **`status`**: 작업 트리의 상태를 보여줍니다.

---

## 공통 히스토리 확장, 표시 및 조정

* **`backfill`**: 부분 클론에서 누락된 객체를 다운로드합니다.
* **`branch`**: 브랜치를 나열, 생성 또는 삭제합니다.
* **`commit`**: 저장소에 변경 사항을 기록합니다.
* **`merge`**: 두 개 이상의 개발 히스토리를 하나로 합칩니다.
* **`rebase`**: 다른 베이스 팁 위에 커밋을 다시 적용합니다.
* **`reset`**: 현재 HEAD를 지정된 상태로 되돌립니다.
* **`switch`**: 브랜치를 전환합니다.
* **`tag`**: GPG로 서명된 태그 객체를 생성, 나열, 삭제 또는 확인합니다.

---

## 협업 (참고: git help workflows)

* **`fetch`**: 다른 저장소에서 객체와 참조(refs)를 다운로드합니다.
* **`pull`**: 다른 저장소 또는 로컬 브랜치에서 가져와 통합합니다.
* **`push`**: 관련 객체와 함께 원격 참조(remote refs)를 업데이트합니다.

---

`git help -a`와 `git help -g`는 사용 가능한 하위 명령어와 일부 개념 가이드를 나열합니다. 특정 하위 명령어나 개념에 대해 읽으려면 `git help <command>` 또는 `git help <concept>`를 참조하세요. 시스템의 전체 개요를 보려면 `git help git`을 참조하세요.

# Git Commit 명령어 옵션 (git commit -h)

---

## 일반 옵션

* `-q`, `--[no-]quiet`: 성공적인 커밋 후 요약 메시지를 **표시하지 않습니다**.
* `-v`, `--[no-]verbose`: 커밋 메시지 템플릿에 **diff(변경 내용)**를 표시합니다.

---

## 커밋 메시지 옵션

* `-F`, `--[no-]file <file>`: **파일**에서 메시지를 읽어옵니다.
* `--[no-]author <author>`: 커밋의 **작성자**를 재정의합니다.
* `--[no-]date <date>`: 커밋의 **날짜**를 재정의합니다.
* `-m`, `--[no-]message <message>`: **커밋 메시지**를 직접 입력합니다.
* `-c`, `--[no-]reedit-message <commit>`: 지정된 **커밋의 메시지를 재사용하고 편집**합니다.
* `-C`, `--[no-]reuse-message <commit>`: 지정된 **커밋의 메시지를 재사용**합니다.
* `--[no-]fixup [(amend|reword):]commit`: `autosquash` 형식의 메시지를 사용하여 지정된 커밋을 **수정(fixup)하거나 변경/재작성(amend/reword)**합니다.
* `--[no-]squash <commit>`: `autosquash` 형식의 메시지를 사용하여 지정된 커밋을 **병합(squash)**합니다.
* `--[no-]reset-author`: ( `-C`/`-c`/`--amend`와 함께 사용될 때) 커밋의 작성자를 **현재 사용자**로 설정합니다.
* `--trailer <trailer>`: 사용자 정의 **트레일러(trailer)**를 추가합니다.
* `-s`, `--[no-]signoff`: `Signed-off-by` **트레일러**를 추가합니다.
* `-t`, `--[no-]template <file>`: 지정된 **템플릿 파일**을 사용합니다.
* `-e`, `--[no-]edit`: 커밋 **편집을 강제**합니다.
* `--[no-]cleanup <mode>`: 메시지에서 공백과 `#` 주석을 **제거하는 방법**을 지정합니다.
* `--[no-]status`: 커밋 메시지 템플릿에 **상태 정보**를 포함합니다.
* `-S`, `--[no-]gpg-sign[=<key-id>]`: 커밋에 **GPG 서명**을 합니다.

---

## 커밋 내용 옵션

* `-a`, `--[no-]all`: 변경된 **모든 파일**을 커밋합니다.
* `-i`, `--[no-]include`: 지정된 파일을 인덱스에 **추가하여 커밋**합니다.
* `--[no-]interactive`: 파일을 **대화형으로 추가**합니다.
* `-p`, `--[no-]patch`: 변경 사항을 **대화형으로 추가**합니다.
* `-o`, `--[no-]only`: 지정된 파일만 **커밋**합니다.
* `-n`, `--no-verify`: `pre-commit` 및 `commit-msg` **훅(hook)을 우회**합니다.
* `--verify`: `--no-verify`의 **반대**입니다.
* `--[no-]dry-run`: **무엇이 커밋될지** 보여줍니다. (실제 커밋은 하지 않음)
* `--[no-]short`: 상태를 **간결하게** 보여줍니다.
* `--[no-]branch`: 브랜치 **정보**를 보여줍니다.
* `--[no-]ahead-behind`: 완전한 앞서감/뒤처짐 **값**을 계산합니다.
* `--[no-]porcelain`: **기계가 읽을 수 있는** 형식으로 출력합니다.
* `--[no-]long`: 상태를 **긴 형식**으로 보여줍니다 (기본값).
* `-z`, `--[no-]null`: 항목을 **NUL 문자**로 종료합니다.
* `--[no-]amend`: 이전 커밋을 **수정(amend)**합니다.
* `--no-post-rewrite`: `post-rewrite` **훅을 우회**합니다.
* `--post-rewrite`: `--no-post-rewrite`의 **반대**입니다.
* `-u`, `--[no-]untracked-files[=<mode>]`: **추적되지 않는 파일**을 보여줍니다. (선택 모드: `all`, `normal`, `no`. 기본값: `all`)
* `--[no-]pathspec-from-file <file>`: **파일**에서 pathspec을 읽어옵니다.
* `--[no-]pathspec-file-nul`: `--pathspec-from-file`과 함께 사용할 때, pathspec 요소가 **NUL 문자**로 구분됩니다.
