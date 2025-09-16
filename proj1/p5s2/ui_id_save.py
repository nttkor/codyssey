import os
import xml.etree.ElementTree as ET
os.chdir(os.path.dirname(__file__))
# 파일 경로
ui_file = "engineering.ui"                # 읽어올 ui 파일
output_file = "engineeringui_list.txt"    # 저장할 txt 파일

# UI 파일 파싱
tree = ET.parse(ui_file)
root = tree.getroot()

results = []

# 모든 위젯 탐색
for widget in root.findall(".//widget"):
    # objectName (위젯의 이름)
    name = widget.attrib.get("name", "").lower()

    # text 속성 찾기
    text_elem = widget.find("./property[@name='text']/string")
    if text_elem is not None and text_elem.text:
        text = text_elem.text.strip()
    else:
        text = ""   # 없는 경우 빈 문자열로 처리

    results.append(f"{name},{text}")

# 결과를 파일로 저장
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print(f"저장 완료: {output_file}")
