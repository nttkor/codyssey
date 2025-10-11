올바른 경로에서 PortAudio 설치 재개하기
다음 단계를 따라 PortAudio 소스 컴파일 설치를 진행하세요.
홈 디렉터리로 이동: ~ 또는 $HOME은 현재 로그인한 사용자의 홈 디렉터리를 가리킵니다.
sh
cd ~
# 또는
cd
코드를 사용할 때는 주의가 필요합니다.

local 폴더 생성: 홈 디렉터리 아래에 local 폴더를 만듭니다.
sh
mkdir -p $HOME/local/lib
mkdir -p $HOME/local/include
코드를 사용할 때는 주의가 필요합니다.

PortAudio 소스 다운로드 및 컴파일: 이제 홈 디렉터리 내에서 나머지 단계를 진행합니다.
sh
# PortAudio 소스코드 다운로드
wget http://www.portaudio.com/archives/pa_stable_v190700_20210729.tgz
tar -zxf pa_stable_v190700_20210729.tgz
cd portaudio

# configure 스크립트 실행. --prefix로 설치 경로 지정.
./configure --prefix=$HOME/local

# 컴파일 및 설치
make
make install
코드를 사용할 때는 주의가 필요합니다.

환경 변수 설정: .bashrc 파일에 환경 변수 설정을 추가합니다.
sh
echo 'export CFLAGS="$CFLAGS -I$HOME/local/include"' >> ~/.bashrc
echo 'export LDFLAGS="$LDFLAGS -L$HOME/local/lib"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc
source ~/.bashrc
코드를 사용할 때는 주의가 필요합니다.

sounddevice 재설치: 마지막으로 sounddevice를 재설치합니다.
sh
pip uninstall sounddevice
pip install sounddevice
코드를 사용할 때는 주의가 필요합니다.

위 단계를 따르면 관리자 권한 없이도 PortAudio를 설치하고 sounddevice를 정상적으로 사용할 수 있습니다.
AI 대답에는 오류가 있을 수 있습니다. 자세히 알아보기



c4r3s5% wget http://www.portaudio.com/archives/pa_stable_v190700_20210729.tgz --2025-10-07 21:29:13-- http://www.portaudio.com/archives/pa_stable_v190700_20210729.tgz Resolving www.portaudio.com (www.portaudio.com)... 3.229.105.207 Connecting to www.portaudio.com (www.portaudio.com)|3.229.105.207|:80... connected. HTTP request sent, awaiting response... 301 Moved Permanently Location: https://www.portaudio.com/archives/pa_stable_v190700_20210729.tgz [following] --2025-10-07 21:29:14-- https://www.portaudio.com/archives/pa_stable_v190700_20210729.tgz Connecting to www.portaudio.com (www.portaudio.com)|3.229.105.207|:443... connected. HTTP request sent, awaiting response... 404 Not Found 2025-10-07 21:29:15 ERROR 404: Not Found.
URL이 변경되거나 파일이 이동되어 404 Not Found 오류가 발생했습니다. 최신 버전의 PortAudio 소스코드 다운로드 링크를 다시 확인해야 합니다. 
가장 좋은 방법은 PortAudio 공식 웹사이트에서 다운로드 페이지로 이동하여 최신 안정화 버전의 링크를 찾는 것입니다.
PortAudio 최신 소스코드 다운로드하기
PortAudio 다운로드 페이지 방문: 웹 브라우저를 열고 다음 URL로 이동합니다.
https://www.portaudio.com/download.html
안정화 버전 링크 확인: 페이지에 있는 "Download PortAudio" 링크를 찾아 클릭하거나, 해당 링크의 URL을 복사합니다.
예시: pa_stable_v190700_20210729.tgz는 2021년에 릴리스된 버전이므로, 더 최신 버전이 있을 수 있습니다.
VS Code 터미널에서 다운로드: wget 명령어를 사용하여 새로운 URL로 파일을 다운로드합니다.
sh
# 이전 파일이 있다면 삭제
rm pa_stable_v190700_20210729.tgz

# 홈 디렉터리로 이동
cd ~

# 새로 찾은 URL로 다운로드
wget [새로운_다운로드_링크]
코드를 사용할 때는 주의가 필요합니다.

 
예시: GitHub에서 PortAudio 소스 받기
만약 공식 웹사이트에서 링크를 찾기 어렵다면, PortAudio의 GitHub 저장소를 통해 최신 소스를 다운로드할 수 있습니다.
sh
# GitHub에서 소스 클론 (git 필요)
git clone https://github.com/PortAudio/portaudio.git
cd portaudio

# (다음 단계로 진행)
코드를 사용할 때는 주의가 필요합니다.

이후 configure, make, make install 단계를 동일하게 진행하면 됩니다.
AI 대답에는 오류가 있을 수 있습니다. 자세히 알아보기







사이트 3개
서버에서 HTTP 오류 404 파일을 찾을 수 없음 - Internet Information ...
2025. 2. 10. — 원인 웹 서버는 요청된 페이지를 검색할 수 없는 경우 HTTP 404 - 파일을 ...
파비콘
Microsoft Learn
404 not found 에러의 의미와 해결 방법 : 네이버 블로그 - Naver Blog
2019. 9. 5. — 홈페이지 관리자 측에서도 여러 가지 사항을 점검해보아야 합니다. 우선 도메인 네임서...
파비콘
NAVER

New Page 1
2009. 8. 14. — 1) Download the source code of the portaudio ...
파비콘
Queen Mary University of London

https://files.portaudio.com/download.html Download PortAudio You can download PortAudio source code in a single archive file below. It contains the complete code for all supported platforms, eg. Windows, Linux, Mac OS X, etc. Stable Releases Release Notes April 6, 2021 - tag v19.7.0 This is the new v19.7.0 stable release. We encourage developers to use this because it has many important bug fixes and works with the latest Mac OS and PipeWire. pa_stable_v190700_20210406.tgz <== You probably want this!! pa_stable_doxydocs_20210406.tgz , stable user documentation (Doxygen)
최신 다운로드 링크 https://files.portaudio.com/download.html와 안정화 버전 pa_stable_v190700_20210406.tgz를 확인했습니다. 이전 wget 명령어가 404 오류를 발생시킨 이유는 URL 경로가 www.portaudio.com/archives/...에서 files.portaudio.com/...로 변경되었기 때문입니다.
관리자 권한 없이 PortAudio를 소스 컴파일로 설치하는 전체 절차를 최신 링크에 맞게 다시 안내해 드리겠습니다.
1단계: 컴파일 도구 및 의존성 확인 (관리자에게 요청)
wget 또는 curl: 소스 다운로드용
gcc: C 컴파일러
make: 빌드 자동화 도구
libasound2-dev: ALSA 개발 라이브러리 (PortAudio의 Linux용 오디오 의존성)
2단계: PortAudio 소스코드 다운로드 및 폴더 생성
홈 디렉터리(~ 또는 $HOME)에서 아래 명령어를 실행하세요.
sh
# 개인 라이브러리 설치를 위한 디렉터리 생성
mkdir -p $HOME/local/lib
mkdir -p $HOME/local/include

# 홈 디렉터리로 이동
cd ~

# PortAudio 소스코드 다운로드 (최신 링크 사용)
wget https://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz

# 다운로드한 파일 압축 해제
tar -zxf pa_stable_v190700_20210406.tgz

# PortAudio 소스 디렉터리로 이동
cd portaudio
코드를 사용할 때는 주의가 필요합니다.

3단계: 소스코드 컴파일 및 설치
소스 디렉터리에서 아래 명령어를 실행하여 컴파일 및 설치를 진행합니다.
sh
# configure 스크립트 실행. --prefix로 설치 경로 지정.
./configure --prefix=$HOME/local

# 컴파일
make

# 지정된 경로에 설치
make install
코드를 사용할 때는 주의가 필요합니다.

make install은 sudo 없이도 $HOME/local 경로에 파일들을 설치합니다. 
4단계: 환경 변수 설정
새로 설치한 라이브러리를 파이썬과 다른 프로그램들이 찾을 수 있도록 환경 변수를 설정해야 합니다.
sh
echo 'export CFLAGS="$CFLAGS -I$HOME/local/include"' >> ~/.bashrc
echo 'export LDFLAGS="$LDFLAGS -L$HOME/local/lib"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc
source ~/.bashrc
코드를 사용할 때는 주의가 필요합니다.

5단계: sounddevice 재설치
설정된 환경 변수가 적용된 후, sounddevice를 제거하고 재설치합니다. 가상 환경(ml-env)이 활성화된 상태에서 진행해야 합니다.
sh
pip uninstall sounddevice
pip install sounddevice
코드를 사용할 때는 주의가 필요합니다.

6단계: 스크립트 실행
이제 javis.py 스크립트를 실행하면 sounddevice가 사용자 계정 내에 설치된 PortAudio 라이브러리를 찾아 녹음이 정상적으로 동작해야 합니다.
sh
/home/mpeg4/Codyssey/ml-env/bin/python /home/mpeg4/Codyssey/proj1/p5s3/javis.py
코드를 사용할 때는 주의가 필요합니다.

AI 대답에는 오류가 있을 수 있습니다. 자세히 알아보기





사이트 1개
[Error] sudoers 설정 파일에 없습니다. 이 시도를 보고합니다. - velog
2021. 4. 11. — sudoers 파일 해당 파일 안에 sudo 명령어를 사용할 수 있는 계정을 지...
파비콘
velog

install은 잘된것 같은데 c4r3s5% make install /usr/bin/install -c -d /home/mpeg4/local/lib /bin/bash ./libtool --mode=install /usr/bin/install -c lib/libportaudio.la /home/mpeg4/local/lib libtool: install: /usr/bin/install -c lib/.libs/libportaudio.so.2.0.0 /home/mpeg4/local/lib/libportaudio.so.2.0.0 libtool: install: (cd /home/mpeg4/local/lib && { ln -s -f libportaudio.so.2.0.0 libportaudio.so.2 || { rm -f libportaudio.so.2 && ln -s libportaudio.so.2.0.0 libportaudio.so.2; }; }) libtool: install: (cd /home/mpeg4/local/lib && { ln -s -f libportaudio.so.2.0.0 libportaudio.so || { rm -f libportaudio.so && ln -s libportaudio.so.2.0.0 libportaudio.so; }; }) libtool: install: /usr/bin/install -c lib/.libs/libportaudio.lai /home/mpeg4/local/lib/libportaudio.la libtool: install: /usr/bin/install -c lib/.libs/libportaudio.a /home/mpeg4/local/lib/libportaudio.a libtool: install: chmod 644 /home/mpeg4/local/lib/libportaudio.a libtool: install: ranlib /home/mpeg4/local/lib/libportaudio.a libtool: finish: PATH="/home/mpeg4/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin:/sbin" ldconfig -n /home/mpeg4/local/lib ---------------------------------------------------------------------- Libraries have been installed in: /home/mpeg4/local/lib If you ever happen to want to link against installed libraries in a given directory, LIBDIR, you must either use libtool, and specify the full pathname of the library, or use the `-LLIBDIR' flag during linking and do at least one of the following: - add LIBDIR to the `LD_LIBRARY_PATH' environment variable during execution - add LIBDIR to the `LD_RUN_PATH' environment variable during linking - use the `-Wl,-rpath -Wl,LIBDIR' linker flag - have your system administrator add LIBDIR to `/etc/ld.so.conf' See any operating system documentation about shared libraries for more information, such as the ld(1) and ld.so(8) manual pages. ---------------------------------------------------------------------- /usr/bin/install -c -d /home/mpeg4/local/include for include in portaudio.h pa_linux_alsa.h pa_jack.h; do \ /usr/bin/install -c -m 644 -m 644 ./include/$include /home/mpeg4/local/include/$include; \ done /usr/bin/install -c -d /home/mpeg4/local/lib/pkgconfig /usr/bin/install -c -m 644 portaudio-2.0.pc /home/mpeg4/local/lib/pkgconfig/portaudio-2.0.pc ------------------------------------------------------------ PortAudio was successfully installed. On some systems (e.g. Linux) you should run 'ldconfig' now to make the shared object available. You may also need to modify your LD_LIBRARY_PATH environment variable to include the directory /home/mpeg4/local/lib ------------------------------------------------------------ make install-recursive make[1]: Entering directory '/home/mpeg4/portaudio' if test -n "" ; then for dir in ""; do make -C $dir install; done ; fi make[1]: Leaving directory '/home/mpeg4/portaudio' c4r3s5% echo 'export CFLAGS="$CFLAGS -I$HOME/local/include"' >> ~/.bashrc c4r3s5% echo 'export LDFLAGS="$LDFLAGS -L$HOME/local/lib"' >> ~/.bashrc c4r3s5% echo 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc c4r3s5% echo 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc c4r3s5% source ~/.bashrc c4r3s5% VS Code 가상환경에서 실행하면 잘안되네 ((ml-env) ) sh-5.2$ pip uninstall sounddevice Found existing installation: sounddevice 0.5.2 Uninstalling sounddevice-0.5.2: Would remove: /home/mpeg4/Codyssey/ml-env/lib/python3.12/site-packages/_sounddevice.py /home/mpeg4/Codyssey/ml-env/lib/python3.12/site-packages/sounddevice-0.5.2.dist-info/* /home/mpeg4/Codyssey/ml-env/lib/python3.12/site-packages/sounddevice.py Proceed (Y/n)? y Successfully uninstalled sounddevice-0.5.2 ((ml-env) ) sh-5.2$ pip install sounddevice Collecting sounddevice Using cached sounddevice-0.5.2-py3-none-any.whl.metadata (1.6 kB) Requirement already satisfied: CFFI>=1.0 in ./ml-env/lib/python3.12/site-packages (from sounddevice) (2.0.0) Requirement already satisfied: pycparser in ./ml-env/lib/python3.12/site-packages (from CFFI>=1.0->sounddevice) (2.23) Using cached sounddevice-0.5.2-py3-none-any.whl (32 kB) Installing collected packages: sounddevice Successfully installed sounddevice-0.5.2 ((ml-env) ) sh-5.2$ /home/mpeg4/Codyssey/ml-env/bin/python /home/mpeg4/Codyssey/proj1/p5s3/javis_test.py Traceback (most recent call last): File "/home/mpeg4/Codyssey/proj1/p5s3/javis_test.py", line 5, in <module> import sounddevice as sd File "/home/mpeg4/Codyssey/ml-env/lib/python3.12/site-packages/sounddevice.py", line 71, in <module> raise OSError('PortAudio library not found') OSError: PortAudio library not found ((ml-env) ) sh-5.2$ /home/mpeg4/Codyssey/ml-env/bin/python /home/mpeg4/Codyssey/proj1/p5s3/javis_test.py Traceback (most recent call last): File "/home/mpeg4/Codyssey/proj1/p5s3/javis_test.py", line 5, in <module> import sounddevice as sd File "/home/mpeg4/Codyssey/ml-env/lib/python3.12/site-packages/sounddevice.py", line 71, in <module> raise OSError('PortAudio library not found') OSError: PortAudio library not found ((ml-env) ) sh-5.2$ /home/mpeg4/Codyssey/ml-env/bin/python /home/mpeg4/Codyssey/proj1/p5s3/javis_a.py Traceback (most recent call last): File "/home/mpeg4/Codyssey/proj1/p5s3/javis_a.py", line 1, in <module> import sounddevice as sd File "/home/mpeg4/Codyssey/ml-env/lib/python3.12/site-packages/sounddevice.py", line 71, in <module> raise OSError('PortAudio library not found') OSError: PortAudio library not found ((ml-env) ) sh-5.2$ /home/mpeg4/Codyssey/ml-env/bin/python /home/mpeg4/Codyssey/proj1/p5s3/javis_a.py Traceback (most recent call last): File "/home/mpeg4/Codyssey/proj1/p5s3/javis_a.py", line 1, in <module> import sounddevice as sd File "/home/mpeg4/Codyssey/ml-env/lib/python3.12/site-packages/sounddevice.py", line 71, in <module> raise OSError('PortAudio library not found') OSError: PortAudio library not found
PortAudio 컴파일 및 설치는 성공적으로 완료된 것으로 보이지만, sounddevice가 가상 환경 내에서 새로 설치된 라이브러리를 제대로 찾지 못하는 문제가 발생하고 있습니다.
이 문제는 주로 다음 두 가지 원인 중 하나로 발생합니다.
환경 변수 문제: source ~/.bashrc는 현재 셸에만 적용됩니다. VS Code 터미널에서 가상 환경을 실행하는 과정에서 환경 변수가 올바르게 전달되지 않았을 수 있습니다.
sounddevice 재설치 문제: sounddevice가 재설치될 때 PortAudio 라이브러리를 컴파일하여 빌드하지 않고, 캐시된 바이너리 파일을 사용했을 가능성이 있습니다.
해결 방법
다음 단계를 따라 문제를 해결해 보세요. 특히 3, 4단계에 집중해야 합니다.
가상 환경 비활성화 후 환경 변수 확인: 가상 환경을 비활성화한 상태에서 PortAudio 관련 환경 변수가 올바르게 설정되었는지 확인합니다.
sh
deactivate
echo $LD_LIBRARY_PATH
코드를 사용할 때는 주의가 필요합니다.

출력 결과에 /home/mpeg4/local/lib가 포함되어야 합니다.
VS Code 터미널 재시작: 환경 변수 변경 사항을 완전히 반영하기 위해 VS Code 터미널을 완전히 닫았다가 다시 엽니다.
sounddevice 강제 재설치: -no-cache-dir 옵션을 사용하여 pip이 캐시를 사용하지 않고 새로 패키지를 빌드하도록 강제합니다.
sh
# 가상 환경 재활성화
source /home/mpeg4/Codyssey/ml-env/bin/activate

# 기존 sounddevice 제거
pip uninstall sounddevice

# PortAudio를 링크하도록 강제하여 새로 빌드
pip install --no-cache-dir --no-binary :all: sounddevice
코드를 사용할 때는 주의가 필요합니다.

--no-binary :all: 옵션은 pip이 미리 빌드된 바이너리 패키지를 사용하지 않고, 소스 코드를 다운로드하여 로컬에서 컴파일하도록 강제합니다. 이 과정에서 설정한 CFLAGS와 LDFLAGS가 사용되어 PortAudio 라이브러리를 올바르게 링크하게 됩니다.
스크립트 실행: 다시 스크립트를 실행하여 정상 작동하는지 확인합니다.
sh
python /home/mpeg4/Codyssey/proj1/p5s3/javis_a.py
코드를 사용할 때는 주의가 필요합니다.

추가 문제 해결: 의존성 부족
만약 -no-binary 옵션으로 설치 시 컴파일 오류가 발생하면, 시스템에 필요한 컴파일 관련 의존성(예: build-essential, libasound2-dev)이 누락되었을 수 있습니다. 이 경우 관리자에게 관련 패키지 설치를 요청해야 합니다.
AI 대답에는 오류가 있을 수 있습니다. 자세히 알아보기



echo $LD_LIBRARY_PATH -> /app/lib
/app/lib라는 LD_LIBRARY_PATH 출력은 문제가 있습니다. 이는 환경 변수가 올바르게 설정되지 않았거나, 가상 환경이 활성화되면서 기본 설정으로 덮어쓰인 것입니다. 
PortAudio가 /home/mpeg4/local/lib에 설치되었으므로, LD_LIBRARY_PATH에 이 경로가 포함되어야 sounddevice가 PortAudio를 찾을 수 있습니다.
해결 방법: 가상 환경 activate 스크립트 수정
가상 환경 활성화 스크립트에 LD_LIBRARY_PATH를 직접 추가하여, 가상 환경을 실행할 때마다 이 변수가 올바르게 설정되도록 합니다.
가상 환경 비활성화:
sh
deactivate
코드를 사용할 때는 주의가 필요합니다.

activate 스크립트 편집: 텍스트 편집기를 사용하여 ml-env의 activate 스크립트를 엽니다.
sh
nano /home/mpeg4/Codyssey/ml-env/bin/activate
코드를 사용할 때는 주의가 필요합니다.

activate 스크립트에 LD_LIBRARY_PATH 추가: 스크립트의 마지막 부분에 다음 코드를 추가합니다. 이는 기존 LD_LIBRARY_PATH 값에 사용자 라이브러리 경로를 추가합니다.
sh
export LD_LIBRARY_PATH="/home/mpeg4/local/lib:$LD_LIBRARY_PATH"
코드를 사용할 때는 주의가 필요합니다.

activate 스크립트 저장 및 종료: Ctrl+X를 누르고, y를 입력한 뒤 Enter를 눌러 저장합니다.
가상 환경 활성화 및 환경 변수 확인: 수정된 스크립트를 사용하여 가상 환경을 다시 활성화하고 LD_LIBRARY_PATH를 확인합니다.
sh
source /home/mpeg4/Codyssey/ml-env/bin/activate
echo $LD_LIBRARY_PATH
코드를 사용할 때는 주의가 필요합니다.

이제 /home/mpeg4/local/lib 경로가 포함된 것을 볼 수 있습니다.
sounddevice 재설치: 환경 변수가 올바르게 설정된 상태에서 sounddevice를 다시 설치합니다.
sh
pip install --no-cache-dir --no-binary :all: sounddevice
코드를 사용할 때는 주의가 필요합니다.

스크립트 실행: 다시 javis_a.py를 실행하면 정상적으로 동작해야 합니다.
sh
python /home/mpeg4/Codyssey/proj1/p5s3/javis_a.py
코드를 사용할 때는 주의가 필요합니다.

AI 대답에는 오류가 있을 수 있습니다. 자세히 알아보기




undefined
사이트 1개
Add LD_LIBRARY_PATH to activate script when installing ...
2023. 5. 24. — Unfortunately virtualenv doesn't set LD_LIBRA...
파비콘
GitHub

뭔가 좋와진것 같다 ((ml-env) ) sh-5.2$ /home/mpeg4/Codyssey/ml-env/bin/python /home/mpeg4/Codyssey/proj1/p5s3/javis_a.py Traceback (most recent call last): File "/home/mpeg4/Codyssey/proj1/p5s3/javis_a.py", line 7, in <module> import whisper ModuleNotFoundError: No module named 'whisper'
오류 메시지 ModuleNotFoundError: No module named 'whisper'는 javis_a.py 스크립트가 whisper 라이브러리를 필요로 하지만, 가상 환경(ml-env)에 설치되어 있지 않다는 것을 의미합니다.
해결 방법
가상 환경 활성화: 현재 가상 환경이 활성화되어 있는지 확인합니다. 만약 아니라면 다음 명령어로 활성화하세요.
sh
source /home/mpeg4/Codyssey/ml-env/bin/activate
코드를 사용할 때는 주의가 필요합니다.

whisper 라이브러리 설치: 가상 환경이 활성화된 상태에서 pip을 사용하여 whisper를 설치합니다. OpenAI에서 개발한 whisper는 음성-텍스트 변환을 위한 라이브러리입니다.
sh
pip install openai-whisper
코드를 사용할 때는 주의가 필요합니다.

주의: pip install whisper가 아닌 pip install openai-whisper를 사용해야 합니다. 종종 이름이 겹치는 다른 패키지가 존재할 수 있습니다.
javis_a.py 스크립트 재실행: 설치가 완료되면 스크립트를 다시 실행합니다.
sh
python /home/mpeg4/Codyssey/proj1/p5s3/javis_a.py
코드를 사용할 때는 주의가 필요합니다.

이제 whisper 모듈을 찾을 수 있으므로, 스크립트가 정상적으로 실행될 것입니다.