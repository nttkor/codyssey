import cv2                 
import os                  
import zipfile             
import numpy as np         

# ----- 유틸 (변경 없음) -----
def unzip_file(zip_path, extract_to):
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} 파일을 찾을 수 없습니다.")
        return
    # zipfile.ZipFile 사용 (이전 코드에서 open으로 되어있던 부분 수정)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        print(f"{zip_path} 압축 해제 중...")
        zip_ref.extractall(extract_to)

def is_image(filename):
    lower = filename.lower()
    return lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".png")

# ----- NMS 함수 (변경 없음) -----
def non_max_suppression(boxes, overlapThresh=0.3):
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes)
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,0] + boxes[:,2]
    y2 = boxes[:,1] + boxes[:,3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    pick = []

    while len(idxs) > 0:
        last = idxs[-1]
        pick.append(last)

        xx1 = np.maximum(x1[last], x1[idxs[:-1]])
        yy1 = np.maximum(y1[last], y1[idxs[:-1]])
        xx2 = np.minimum(x2[last], x2[idxs[:-1]])
        yy2 = np.minimum(y2[last], y2[idxs[:-1]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / areas[idxs[:-1]] 

        idxs = np.delete(idxs, np.concatenate(([len(idxs)-1],
            np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")

# ----- Helper 클래스 -----
class MasImageHelper:
    def __init__(self, folder):
        self.folder = folder
        self.images = sorted([f for f in os.listdir(folder) if is_image(f)])
        self.index = 0
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.image_count = len(self.images)

    def has_images(self):
        return self.image_count > 0

    def is_last_image(self):
        return self.index >= self.image_count - 1

    def current_meta(self):
        idx = self.index + 1
        return idx, self.image_count

    def show_image(self):
        if not self.has_images():
            return None, None
        path = os.path.join(self.folder, self.images[self.index])
        img = cv2.imread(path)
        idx, total = self.current_meta()
        return self.annotate(img, idx, total), path 

    def next_image(self):
        if self.index < self.image_count - 1:
            self.index += 1
            return True
        return False

    def prev_image(self):
        self.index = (self.index - 1) % self.image_count
        return True

    def annotate(self, img, idx, total, message=None, color=(255, 255, 255), message_scale=1.2, message_thickness=3):
        if img is None:
            return img
        overlay = img.copy()
        text = f"{idx}/{total}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.7
        thickness = 2
        margin = 10
        (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
        box_w, box_h = tw + 2 * margin, th + 2 * margin
        cv2.rectangle(overlay, (10, 10), (10 + box_w, 10 + box_h), (0, 0, 0), -1)
        alpha = 0.4
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        cv2.putText(img, text, (10 + margin, 10 + box_h - margin),
                    font, scale, color, thickness, cv2.LINE_AA)

        if message:
            h, w = img.shape[:2]
            # 텍스트 중앙 정렬 계산
            (text_w, text_h), _ = cv2.getTextSize(message, font, message_scale, message_thickness)
            text_x = (w - text_w) // 2
            text_y = (h + text_h) // 2
            
            cv2.putText(img, message, (text_x, text_y),
                        font, message_scale, (0,255,255), message_thickness, cv2.LINE_AA)

        return img

# MasImageHelper 클래스 내부의 detect_people_and_faces 함수를 이것으로 교체
# MasImageHelper 클래스 내부의 detect_people_and_faces 함수
    def detect_people_and_faces(self, img,
                                winStride=(4,4), padding=(32,32), scale=1.01, hitThreshold=-0.6, 
                                face_scaleFactor=1.1, face_minNeighbors=5, face_minSize=(30,30), 
                                angles=[0, -45, 45]):
        h, w = img.shape[:2]                       
        center = (w//2, h//2)                      
        all_rects = [] 

        # 1. HOG 검출 (회전본/축소본 포함)
        for angle in angles:
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(img, M, (w, h))
            rects, _ = self.hog.detectMultiScale(rotated, winStride=winStride, padding=padding, scale=scale, hitThreshold=hitThreshold)
            M_inv = cv2.invertAffineTransform(M)   
            for (x, y, rw, rh) in rects:           
                pts = np.array([[[x, y]], [[x+rw, y]], [[x, y+rh]], [[x+rw, y+rh]]], dtype=np.float32) 
                pts = cv2.transform(pts, M_inv)    
                x_coords = pts[:,0,0]; y_coords = pts[:,0,1] 
                x0, y0, x1, y1 = int(x_coords.min()), int(y_coords.min()), int(x_coords.max()), int(y_coords.max()) 
                all_rects.append((x0,y0,x1-x0,y1-y0)) 

        small = cv2.resize(img, (w//2, h//2))      
        rects_small, _ = self.hog.detectMultiScale(small, winStride=winStride, padding=padding, scale=scale, hitThreshold=hitThreshold)
        rects_small = [(x*2, y*2, rw*2, rh*2) for (x,y,rw,rh) in rects_small] 
        all_rects.extend(rects_small)              

        # 2. 얼굴 검출 (Haar Cascade)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = self.face_cascade.detectMultiScale(gray, 
                                                   scaleFactor=face_scaleFactor,
                                                   minNeighbors=face_minNeighbors,
                                                   minSize=face_minSize)
        
        # 💡 오류 수정: faces가 NumPy 배열인 경우에만 tolist()를 호출하여 all_rects에 추가
        if isinstance(faces, np.ndarray) and faces.size > 0:
            all_rects.extend(faces.tolist())

        # 3. NMS 적용 (임계값 0.3)
        final_rects = non_max_suppression(all_rects, overlapThresh=0.3) 
        people_found = len(final_rects) > 0
        
        # 4. 박스 그리기
        for (x,y,rw,rh) in final_rects:            
            # 비율에 따른 색상 결정 (사람: 초록, 얼굴: 파랑)
            ratio = rh / rw
            if 0.5 < ratio < 2.0: # 꽤 네모난 형태 (사람이나 큰 얼굴)
                color = (0,255,0) # 초록색
            else: 
                color = (255,0,0) # 파란색
                
            cv2.rectangle(img, (x,y), (x+rw,y+rh), color, 2) 

        idx, total = self.current_meta()           
        return self.annotate(img, idx, total), people_found

def problem2():
    if not os.path.exists("cctv"):                 
        unzip_file("cctv.zip", "cctv")             

    helper = MasImageHelper("cctv")                
    if not helper.has_images():                    
        print("cctv 폴더에 이미지가 없습니다.")       
        return                                     

    cv2.namedWindow("CCTV Search", cv2.WINDOW_AUTOSIZE) 
    state = {"img": None}                          

    # 상태 관리 변수: 엔터 시작을 위해 False 유지
    is_searching = False      
    is_paused_on_find = False 
    search_finished = False   

    def on_mouse(event, x, y, flags, param):
        nonlocal is_searching, is_paused_on_find
        if event == cv2.EVENT_LBUTTONDOWN and state["img"] is not None:
            # 자동/정지 상태와 관계없이 마우스 클릭으로 순환 가능
            
            h, w, _ = state["img"].shape

            if x < w // 3:                         
                helper.prev_image()                
            elif x > 2 * w // 3:                   
                helper.next_image()                
            
            new_img, _ = helper.show_image()
            state["img"] = new_img
            cv2.imshow("CCTV Search", new_img)

    cv2.setMouseCallback("CCTV Search", on_mouse)  

    # --- 메인 루프 ---
    while True:                                    
        img, path = helper.show_image()            
        if img is None:                            
            break                                  

        state["img"] = img                         
        
        # 1. 검색 종료 상태 (Finish 크게 표시)
        if search_finished:
            final_img = helper.annotate(img.copy(), *helper.current_meta(), 
                                        message="Finish", color=(0, 255, 255), 
                                        message_scale=3.0, message_thickness=5)
            cv2.imshow("CCTV Search", final_img)
            key = cv2.waitKey(0)

        # 2. 자동 검색 중
        elif is_searching and not is_paused_on_find:
            # 'Detecting...' 메시지 표시
            temp_img = helper.annotate(img.copy(), *helper.current_meta(), message="Detecting...")
            cv2.imshow("CCTV Search", temp_img)
            key = cv2.waitKey(1) 

            detected_img, people_found = helper.detect_people_and_faces(img.copy())
            cv2.imshow("CCTV Search", detected_img)

            if people_found:
                print(f"사람 발견: {path} 에서 검색이 중단되었습니다. 다음 검색을 시작하려면 Enter 키를 누르세요.")
                is_paused_on_find = True 
                key = cv2.waitKey(0) 

            else:
                if helper.is_last_image(): 
                    search_finished = True 
                    print("모든 사진 검색이 완료되었습니다.")
                else:
                    helper.next_image()
                key = cv2.waitKey(1) 

        # 3. 정지/일시 정지 모드 (자동 검색 전, 또는 발견 후 정지 상태)
        else:
            cv2.imshow("CCTV Search", img)             
            key = cv2.waitKey(0) 

        # --- 키 입력 처리 ---
        if key == 27:  # ESC 키
            break
        
        elif key == 13: # Enter 키
            if search_finished:
                break
                
            elif is_paused_on_find:
                # 사람 발견 후 정지 상태 -> 다음 이미지로 이동 후 자동 검색 재시작
                is_paused_on_find = False
                if helper.is_last_image():
                    search_finished = True
                    print("모든 사진 검색이 완료되었습니다.")
                else:
                    helper.next_image()
                is_searching = True # 👈 자동 검색 True로 전환
            
            elif is_searching:
                # 자동 검색 중 -> 일시 중지
                is_searching = False # 👈 자동 검색 False로 전환
                print("자동 검색이 일시 중지되었습니다.")
                
            else:
                # 검색 중이 아님 (초기 상태) -> 자동 검색 시작
                is_searching = True
                print("자동 검색을 시작합니다.")

        # 화살표 키 처리 (수동 이미지 순환)
        elif key in [2424832, 81]: 
            if not is_searching and not is_paused_on_find:
                 helper.prev_image()
        elif key in [2555904, 83]: 
            if not is_searching and not is_paused_on_find:
                helper.next_image()

    cv2.destroyAllWindows()                        

if __name__ == "__main__":
    try:
        problem2()                                     
    except Exception as e:
        print(f"오류 발생: {e}")
        cv2.destroyAllWindows()