import os
from ultralytics import YOLO
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())
# 1) 사전학습 모델 로드 (경량→고속: yolov8n.pt / 정확도↑: yolov8s/m/l/x.pt)
model = YOLO("yolov8n.pt")

# 2) 이미지/폴더/비디오/웹캠에서 '사람'만 탐지
# classes=[0] 이 COCO에서 person 클래스 인덱스
# conf=0.25~0.5 사이에서 환경에 맞게 조절 (우주복/특수조명이라면 0.25~0.35 권장)
results = model.predict(
    source= "cctv\cctv-1.jpg" ,
    # 'proj1\p5s4\cctv\cctv-1.jpg' 
    #"your_input.mp4",  # "image.jpg", 0(웹캠), "folder/", "rtsp://..." 모두 가능
    classes=[0],
    conf=0.3,
    iou=0.5,     # 박스 중복 억제
    imgsz=1024    # 640 기본, 멀리 있는 사람은 720~960도 시도
)

# 3) 시각화/저장 (Ultralytics가 자동 저장 옵션도 제공)
for r in results:
    r.show()       # 창에 띄우기
    r.save(filename="out.jpg")  # 파일 저장 예시