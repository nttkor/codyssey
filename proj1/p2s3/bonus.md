# bonus
minimal-mistakes 테마를 적용해서 블로그를 아래와 같이 새로 생성한다
계정이름.github.io 저장소를 삭제한다.
Github 사이트에서 minimal-mistakes를 검색한다.
해당 저장소를 Fork해서 계정이름.github.io 저장소를 생성한다.

# 해설
## **GitHub Pages**를 사용하여 **minimal-mistakes** 테마를 적용한 블로그를 만드는 과제를 도와드리겠습니다.
이 작업은 GitHub에서 미리 만들어 놓은 **Jekyll 테마**인 `minimal-mistakes`를 사용하여 블로그를 생성하는 작업입니다.

### **Bonus - minimal-mistakes 테마 적용하여 블로그 생성**

#### 1. **계정이름.github.io 저장소 삭제**

* 먼저, GitHub에서 기존에 만든 `계정이름.github.io` 저장소를 삭제합니다.
* GitHub에서 자신의 프로필로 이동하고, **Repositories** 탭을 클릭합니다.
* `계정이름.github.io` 저장소를 찾아서 들어가세요.
* 저장소의 **Settings** 탭으로 가서 아래로 스크롤하면 **Danger Zone**이 있습니다.
* **Delete this repository** 버튼을 클릭하고, 저장소 이름을 확인한 후 **삭제**합니다.

#### 2. **minimal-mistakes 테마 검색**

* GitHub에서 `minimal-mistakes`를 검색합니다. [minimal-mistakes GitHub 저장소 링크](https://github.com/mmistakes/minimal-mistakes)
* 해당 저장소에서 **Fork** 버튼을 클릭하여 **자신의 GitHub 계정**에 Fork합니다.

#### 3. **계정이름.github.io 저장소 생성**

* `minimal-mistakes` 테마를 Fork한 후, 이 저장소를 **계정이름.github.io**라는 이름으로 **새 저장소**로 만들기 위해 **새 저장소**를 생성해야 합니다.
* **새 저장소**를 생성할 때, 저장소 이름을 반드시 \*\*`계정이름.github.io`\*\*로 지정해야 합니다.
* 이때, 저장소가 GitHub Pages에서 사용할 수 있는 웹사이트 주소를 자동으로 가지게 됩니다.

#### 4. **GitHub Pages 설정**

* `계정이름.github.io` 저장소로 이동합니다.
* **Settings** 탭으로 가서 **Pages** 섹션을 찾습니다.
* **Source** 항목에서 `main` 브랜치를 선택하고 **Save** 버튼을 클릭합니다.
* 저장소 설정 후, 몇 분이 지나면 \*\*[https://계정이름.github.io\*\*에서](https://계정이름.github.io**에서) 웹사이트를 확인할 수 있습니다.

#### 5. **테마 적용 및 커스터마이징**

* Fork한 `minimal-mistakes` 테마의 설정을 변경하고 싶다면, `config.yml` 파일을 수정해야 합니다. 기본적으로 블로그 제목, 설명, 그리고 로고 등의 설정을 여기에 넣습니다.
* 예를 들어, `config.yml` 파일에서 다음과 같은 설정을 할 수 있습니다:

```yaml
title: "나의 기술 블로그"
description: "기술 관련 내용을 공유하는 블로그"
```

#### 6. **최종 결과**

이렇게 하면 `minimal-mistakes` 테마를 적용한 블로그가 `https://계정이름.github.io`로 나타날 것입니다.

### 추가적으로 해야 할 일

* **로컬에서 테스트**:

  * **Jekyll**을 로컬에서 실행하고 싶으면 Ruby와 Jekyll을 설치한 후 로컬 환경에서 블로그를 확인할 수 있습니다.
  * GitHub Pages는 기본적으로 Jekyll을 사용하지만, 로컬에서 미리보기로 확인하고 싶다면, 터미널에서 다음 명령어를 입력합니다:

```bash
bundle exec jekyll serve
```

이렇게 하면 로컬에서 `http://localhost:4000`을 통해 블로그를 미리 확인할 수 있습니다.

### 요약:

1. 기존의 `계정이름.github.io` 저장소를 삭제.
2. GitHub에서 `minimal-mistakes` 테마를 Fork하고, 이를 새로운 `계정이름.github.io` 저장소로 푸시.
3. GitHub Pages에서 `main` 브랜치를 Source로 설정.
4. 몇 분 후 웹에서 확인.

이렇게 하면 **minimal-mistakes** 테마를 사용한 블로그를 GitHub Pages에 배포할 수 있습니다!
