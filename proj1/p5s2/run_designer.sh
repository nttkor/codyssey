#!/bin/bash

# Qt Designer를 실행하는 명령어
/home/mpeg4/.local/lib/python3.10/site-packages/qt6_applications/Qt/bin/designer

# 스크립트가 실행된 후 터미널이 바로 닫히는 것을 방지
# 필요에 따라 주석 처리하거나 삭제
read -p "Press Enter to exit..."


# 셸 스크립트 실행하기
# 이제 만든 .sh 파일을 실행 가능하도록 권한을 변경해야 합니다.

# 실행 권한 부여: 터미널에서 아래 명령어를 실행하여 스크립트 파일에 실행 권한을 줍니다.

# Bash

# chmod +x run_designer.sh
# chmod는 파일의 권한을 변경하는 명령어이고, +x는 '실행 가능' 권한을 추가합니다.
# 스크립트 실행: 이제 파일을 실행할 수 있습니다.

# Bash

# ./run_designer.sh
# ./는 현재 디렉터리에 있는 파일을 실행하겠다는 의미입니다.

# 이렇게 하면 designer를 실행할 때마다 긴 경로를 입력할 필요 없이 run_designer.sh