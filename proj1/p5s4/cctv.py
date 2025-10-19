import cv2                 # OpenCV 라이브러리를 임포트합니다. 컴퓨터 비전 작업을 위해 사용됩니다.
import os                  # OS(Operating System) 모듈을 임포트합니다. 파일 시스템 작업을 위해 사용됩니다.
import zipfile             # zipfile 모듈을 임포트합니다. ZIP 파일 압축 해제를 위해 사용됩니다.
import numpy as np         # NumPy 라이브러리를 임포트합니다. 배열(행렬) 연산을 위해 사용되며, NMS 등에 활용됩니다.

# ----- 유틸 -----
def unzip_file(zip_path, extract_to):
    # 지정된 경로의 ZIP 파일을 대상 폴더에 압축 해제하는 함수
    with zipfile.ZipFile(zip_path, 'r') as zip_ref: # ZIP 파일을 읽기 모드로 엽니다.
        zip_ref.extractall(extract_to)               # 지정된 경로(extract_to)에 모든 내용을 압축 해제합니다.

def is_image(filename):
    # 파일 이름이 이미지 파일 확장자인지 확인하는 함수
    lower = filename.lower()                          # 파일 이름을 소문자로 변환합니다.
    return lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".png") # 지원하는 이미지 확장자(.jpg, .jpeg, .png)로 끝나는지 확인합니다.

# ----- NMS 함수 -----
def non_max_suppression(boxes, overlapThresh=0.3):
    # NMS (Non-Maximum Suppression): 겹치는 영역이 많은(Overlapping) 바운딩 박스들 중에서 가장 점수가 높은 박스 하나만 남기고 나머지를 제거하는 함수
    if len(boxes) == 0:                            # 입력된 박스가 없으면
        return []                                  # 빈 리스트를 반환합니다.
    boxes = np.array(boxes)                        # 입력 박스 리스트를 NumPy 배열로 변환합니다.
    x1 = boxes[:,0]                                # 모든 박스의 좌상단 x 좌표 (x)
    y1 = boxes[:,1]                                # 모든 박스의 좌상단 y 좌표 (y)
    x2 = boxes[:,0] + boxes[:,2]                   # 모든 박스의 우하단 x 좌표 (x + width)
    y2 = boxes[:,1] + boxes[:,3]                   # 모든 박스의 우하단 y 좌표 (y + height)

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)          # 각 박스의 면적을 계산합니다.
    idxs = np.argsort(y2)                          # y2(박스의 바닥 y 좌표)를 기준으로 오름차순 정렬한 인덱스를 얻습니다. (일반적인 NMS는 점수를 사용하지만, 이 구현은 y2를 사용)
    pick = []                                      # 최종 선택된 박스의 인덱스를 저장할 리스트

    while len(idxs) > 0:                           # 처리할 인덱스가 남아있는 동안 반복합니다.
        last = idxs[-1]                            # 현재 가장 큰 y2 값을 가진 박스의 인덱스(가장 아래에 있는 박스)를 선택합니다.
        pick.append(last)                          # 선택된 인덱스를 최종 선택 리스트에 추가합니다.

        # 선택된 박스와 나머지 박스들 간의 겹치는 영역 좌표를 계산합니다.
        xx1 = np.maximum(x1[last], x1[idxs[:-1]])  # 겹치는 영역의 좌상단 x 좌표 (max(x1_last, x1_rest))
        yy1 = np.maximum(y1[last], y1[idxs[:-1]])  # 겹치는 영역의 좌상단 y 좌표 (max(y1_last, y1_rest))
        xx2 = np.minimum(x2[last], x2[idxs[:-1]])  # 겹치는 영역의 우하단 x 좌표 (min(x2_last, x2_rest))
        yy2 = np.minimum(y2[last], y2[idxs[:-1]])  # 겹치는 영역의 우하단 y 좌표 (min(y2_last, y2_rest))

        w = np.maximum(0, xx2 - xx1 + 1)           # 겹치는 영역의 너비 (음수 방지)
        h = np.maximum(0, yy2 - yy1 + 1)           # 겹치는 영역의 높이 (음수 방지)

        overlap = (w * h) / areas[idxs[:-1]]       # 겹치는 영역 / 나머지 박스들의 면적 = IOU(Intersection over Union)가 아닌 '겹치는 면적 비율' (IoU와 유사하나, 분모가 A 또는 B 면적)

        # 겹치는 면적 비율이 overlapThresh를 초과하는 모든 박스(겹치는 박스)의 인덱스를 제거합니다.
        idxs = np.delete(idxs, np.concatenate(([len(idxs)-1], # 현재 선택된 박스 인덱스 (idxs의 마지막 원소)
            np.where(overlap > overlapThresh)[0])))         # 겹침 임계값 초과하는 박스의 인덱스

    return boxes[pick].astype("int")               # 최종 선택된 박스들의 좌표를 정수형으로 반환합니다.

# ----- Helper 클래스 -----
class MasImageHelper:
    # 이미지 폴더를 관리하고, 이미지 탐색, 주석 추가, 사람/얼굴 검출 기능을 제공하는 헬퍼 클래스
    def __init__(self, folder):
        self.folder = folder                       # 이미지 폴더 경로를 저장합니다.
        self.images = sorted([f for f in os.listdir(folder) if is_image(f)]) # 폴더 내 이미지 파일 목록을 가져와 정렬합니다.
        self.index = 0                             # 현재 보여줄 이미지의 인덱스입니다. (초기값: 0)
        self.hog = cv2.HOGDescriptor()             # HOG Descriptor 객체를 생성합니다.
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) # HOG 검출기에 기본 사람 검출기(SVM)를 설정합니다.
        self.face_cascade = cv2.CascadeClassifier( # 얼굴 검출을 위한 Haar Cascade 분류기 객체를 생성합니다.
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml" # 미리 학습된 정면 얼굴 XML 파일을 로드합니다.
        )

    def has_images(self):
        # 이미지 파일이 존재하는지 확인합니다.
        return len(self.images) > 0

    def current_meta(self):
        # 현재 이미지의 인덱스와 전체 이미지 수를 반환합니다.
        total = len(self.images)                   # 전체 이미지 수
        idx = self.index + 1                       # 현재 이미지 번호 (1부터 시작)
        return idx, total

    def show_image(self):
        # 현재 인덱스의 이미지를 로드하고 번호를 표시한 후 반환합니다.
        if not self.has_images():                  # 이미지가 없으면
            return None, None                      # None을 반환합니다.
        path = os.path.join(self.folder, self.images[self.index]) # 현재 이미지 파일의 전체 경로를 만듭니다.
        img = cv2.imread(path)                     # 이미지를 로드합니다.
        idx, total = self.current_meta()           # 현재 인덱스 및 전체 메타 정보를 가져옵니다.
        return self.annotate(img, idx, total), path # 이미지에 주석(번호)을 추가하고 주석이 추가된 이미지와 경로를 반환합니다.

    def next_image(self):
        # 다음 이미지로 인덱스를 이동시킵니다. (순환)
        self.index = (self.index + 1) % len(self.images) # 인덱스를 1 증가시키고, 전체 이미지 수로 나눈 나머지(모듈러 연산)를 사용하여 순환 구조를 만듭니다.

    def prev_image(self):
        # 이전 이미지로 인덱스를 이동시킵니다. (순환)
        self.index = (self.index - 1) % len(self.images) # 인덱스를 1 감소시키고, 순환을 위해 모듈러 연산을 사용합니다.

    def annotate(self, img, idx, total):
        # 이미지에 현재 이미지 번호/전체 이미지 수 텍스트를 오버레이하는 함수
        if img is None:                            # 이미지가 없으면
            return img                             # 그대로 반환합니다.
        overlay = img.copy()                       # 이미지 복사본을 만들어 오버레이용으로 사용합니다.
        text = f"{idx}/{total}"                    # 표시할 텍스트 (예: "1/10")
        font = cv2.FONT_HERSHEY_SIMPLEX            # 폰트 지정
        scale = 0.7                                # 폰트 크기 비율
        thickness = 2                              # 폰트 두께
        margin = 10                                # 텍스트 주변 여백
        (tw, th), _ = cv2.getTextSize(text, font, scale, thickness) # 텍스트의 너비와 높이를 계산합니다.
        box_w, box_h = tw + 2 * margin, th + 2 * margin # 텍스트 박스의 너비와 높이를 계산합니다.
        cv2.rectangle(overlay, (10, 10), (10 + box_w, 10 + box_h), (0, 0, 0), -1) # 좌상단에 검은색 배경 박스를 그립니다. (-1은 채우기)
        alpha = 0.4                                # 오버레이 투명도 설정
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img) # 원본 이미지에 투명한 검은색 박스를 합성합니다.
        cv2.putText(img, text, (10 + margin, 10 + box_h - margin), # 이미지에 흰색 텍스트를 박스 위에 출력합니다.
                    font, scale, (255, 255, 255), thickness, cv2.LINE_AA)
        return img                                 # 주석이 추가된 이미지를 반환합니다.

    # --- 사람 + 얼굴 검출 (원본 + 축소본 + 회전본, NMS 적용) ---
    def detect_people_and_faces(self, img,
                                winStride=(8,8), padding=(8,8), scale=1.05, hitThreshold=0.0, # HOG 검출 파라미터
                                face_scaleFactor=1.1, face_minNeighbors=5, face_minSize=(30,30), # 얼굴 검출 파라미터
                                angles=[0, -45, 45]): # HOG를 적용할 이미지 회전 각도 목록
        h, w = img.shape[:2]                       # 이미지 높이와 너비를 가져옵니다.
        center = (w//2, h//2)                      # 이미지 중심 좌표
        all_rects = []                             # 검출된 모든 사람 박스를 저장할 리스트

        # 회전본 검출
        for angle in angles:                       # 정의된 각도별로 반복합니다.
            M = cv2.getRotationMatrix2D(center, angle, 1.0) # 회전을 위한 2x3 변환 행렬을 계산합니다.
            rotated = cv2.warpAffine(img, M, (w, h)) # 이미지를 지정된 각도로 회전합니다.
            rects, _ = self.hog.detectMultiScale(rotated, # 회전된 이미지에서 HOG로 사람을 검출합니다.
                                                 winStride=winStride,
                                                 padding=padding,
                                                 scale=scale,
                                                 hitThreshold=hitThreshold)
            M_inv = cv2.invertAffineTransform(M)   # 역변환 행렬을 계산합니다. (회전된 좌표를 원본 이미지 좌표로 되돌리기 위함)
            for (x, y, rw, rh) in rects:           # 검출된 각 박스에 대해
                # 회전된 좌표를 원본 이미지 좌표로 변환합니다.
                pts = np.array([[[x, y]], [[x+rw, y]], [[x, y+rh]], [[x+rw, y+rh]]], dtype=np.float32) # 박스의 네 꼭짓점 좌표
                pts = cv2.transform(pts, M_inv)    # 역변환 행렬을 적용하여 원본 이미지 좌표로 변환합니다.
                x_coords = pts[:,0,0]; y_coords = pts[:,0,1] # 변환된 x, y 좌표
                x0, y0, x1, y1 = int(x_coords.min()), int(y_coords.min()), int(x_coords.max()), int(y_coords.max()) # 변환된 네 꼭짓점의 최소/최대 좌표를 사용하여 새로운 박스 좌표를 계산합니다.
                all_rects.append((x0,y0,x1-x0,y1-y0)) # 새로운 박스 (x, y, width, height)를 저장합니다.

        # 축소본 검출
        small = cv2.resize(img, (w//2, h//2))      # 원본 이미지를 1/2 크기로 축소합니다.
        rects_small, _ = self.hog.detectMultiScale(small, # 축소된 이미지에서 HOG로 사람을 검출합니다.
                                                   winStride=winStride,
                                                   padding=padding,
                                                   scale=scale,
                                                   hitThreshold=hitThreshold)
        rects_small = [(x*2, y*2, rw*2, rh*2) for (x,y,rw,rh) in rects_small] # 축소된 이미지의 박스 좌표를 원본 이미지 크기에 맞게 2배로 스케일링합니다.
        all_rects.extend(rects_small)              # 스케일링된 박스를 전체 박스 리스트에 추가합니다.

        # NMS 적용
        final_rects = non_max_suppression(all_rects, overlapThresh=0.4) # 회전/축소본에서 얻은 모든 박스에 대해 NMS를 적용하여 중복을 제거합니다.

        for (x,y,rw,rh) in final_rects:            # 최종 선택된 각 사람 박스에 대해
            cv2.rectangle(img, (x,y), (x+rw,y+rh), (0,255,0), 2) # 이미지에 초록색(0,255,0) 사각형을 그립니다. (사람 검출 결과)

        # 얼굴 검출 (원본만)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 이미지 색상을 BGR에서 회색조(Gray)로 변환합니다. (Haar Cascade는 주로 회색조 이미지를 사용)
        faces = self.face_cascade.detectMultiScale(gray, # 회색조 이미지에서 Haar Cascade로 얼굴을 검출합니다.
                                                   scaleFactor=face_scaleFactor,
                                                   minNeighbors=face_minNeighbors,
                                                   minSize=face_minSize)
        for (x, y, rw, rh) in faces:               # 검출된 각 얼굴 박스에 대해
            cv2.rectangle(img, (x, y), (x+rw, y+rh), (255,0,0), 2) # 이미지에 파란색(255,0,0) 사각형을 그립니다. (얼굴 검출 결과)

        idx, total = self.current_meta()           # 현재 인덱스 및 전체 메타 정보를 가져옵니다.
        return self.annotate(img, idx, total)      # 검출 결과를 표시한 이미지에 다시 주석(번호)을 추가하고 반환합니다.

def problem2():
    # 메인 실행 함수
    if not os.path.exists("cctv"):                 # 'cctv' 폴더가 존재하지 않으면
        unzip_file("cctv.zip", "cctv")             # 'cctv.zip' 파일의 압축을 'cctv' 폴더에 해제합니다.

    helper = MasImageHelper("cctv")                # MasImageHelper 클래스의 인스턴스를 'cctv' 폴더를 사용하여 생성합니다.
    if not helper.has_images():                    # 이미지 헬퍼에 이미지가 없으면
        print("cctv 폴더에 이미지가 없습니다.")       # 에러 메시지를 출력하고
        return                                     # 함수를 종료합니다.

    cv2.namedWindow("CCTV Search", cv2.WINDOW_AUTOSIZE) # "CCTV Search"라는 이름의 창을 생성합니다. (크기 자동 조절)
    state = {"img": None}                          # 현재 표시 중인 이미지를 저장할 딕셔너리 (마우스 콜백에서 사용)

    # --- 마우스 콜백 ---
    def on_mouse(event, x, y, flags, param):
        # 마우스 이벤트가 발생할 때 호출되는 콜백 함수
        if event == cv2.EVENT_LBUTTONDOWN and state["img"] is not None: # 마우스 왼쪽 버튼을 눌렀고, 현재 이미지가 있을 때
            h, w, _ = state["img"].shape           # 현재 이미지의 높이와 너비를 가져옵니다.

            if x < w // 3:                         # 화면 왼쪽 1/3 영역 클릭 시
                helper.prev_image()                # 이전 이미지로 이동
                new_img, _ = helper.show_image()   # 새로운 이미지 로드 및 주석 추가
                state["img"] = new_img             # 상태 업데이트
                cv2.imshow("CCTV Search", new_img) # 새로운 이미지 표시

            elif x > 2 * w // 3:                   # 화면 오른쪽 1/3 영역 클릭 시
                helper.next_image()                # 다음 이미지로 이동
                new_img, _ = helper.show_image()   # 새로운 이미지 로드 및 주석 추가
                state["img"] = new_img             # 상태 업데이트
                cv2.imshow("CCTV Search", new_img) # 새로운 이미지 표시

            else:                                  # 화면 중앙 1/3 영역 클릭 시 (검출 시작)
                # 검출 중 메시지 표시
                temp = state["img"].copy()
                cv2.putText(temp, "Detecting...", (w//2 - 100, h//2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3, cv2.LINE_AA) # 중앙에 'Detecting...' 텍스트를 노란색으로 표시
                cv2.imshow("CCTV Search", temp)
                cv2.waitKey(1)                     # 화면 업데이트를 위해 잠시 대기

                # 마우스 Y 좌표에 따라 검출 파라미터를 다르게 적용 (Min/Mid/Max 민감도)
                if y < h // 3:                     # 상단 1/3 영역 클릭 (Min: 낮은 민감도)
                    detected = helper.detect_people_and_faces(state["img"].copy(),
                        winStride=(6,6), scale=1.03, hitThreshold=-0.3)
                elif y < 2 * h // 3:               # 중앙 1/3 영역 클릭 (Mid: 중간 민감도)
                    detected = helper.detect_people_and_faces(state["img"].copy(),
                        winStride=(4,4), scale=1.01, hitThreshold=-0.6, padding=(32,32))
                else:                              # 하단 1/3 영역 클릭 (Max: 높은 민감도)
                    detected = helper.detect_people_and_faces(state["img"].copy(),
                        winStride=(2,2), scale=0.95, hitThreshold=-1.0, padding=(64,64))

                cv2.imshow("CCTV Search", detected) # 검출 결과를 표시합니다.

    cv2.setMouseCallback("CCTV Search", on_mouse)  # "CCTV Search" 창에 마우스 콜백 함수를 설정합니다.

    # --- 메인 루프 ---
    while True:                                    # 무한 루프 (UI 상호작용)
        img, path = helper.show_image()            # 현재 인덱스의 이미지를 로드합니다.
        if img is None:                            # 로드된 이미지가 없으면
            break                                  # 루프를 종료합니다.
        state["img"] = img                         # 상태를 업데이트합니다.
        cv2.imshow("CCTV Search", img)             # 이미지를 화면에 표시합니다.

        key = cv2.waitKey(0)                       # 키 입력을 무한정 기다립니다. (0ms 대기)
        if key == 27:                              # ESC 키 (ASCII 27)가 눌리면
            break                                  # 루프를 종료합니다.
        elif key == 81:                            # 왼쪽 화살표 키(81)가 눌리면 (키 코드는 시스템에 따라 다를 수 있음)
            helper.prev_image()                    # 이전 이미지로 이동합니다.
        elif key == 83:                            # 오른쪽 화살표 키(83)가 눌리면
            helper.next_image()                    # 다음 이미지로 이동합니다.

    cv2.destroyAllWindows()                        # 생성된 모든 OpenCV 창을 닫고 종료합니다.


# ----- 실행 -----
if __name__ == "__main__":
    # 스크립트가 직접 실행될 때만 아래 코드를 실행합니다.
    os.chdir(os.path.dirname(__file__))            # 현재 스크립트 파일이 위치한 디렉토리로 작업 디렉토리를 변경합니다. (파일 경로 처리의 일관성을 위함)
    problem2()                                     # problem2 함수를 호출하여 프로그램을 시작합니다.