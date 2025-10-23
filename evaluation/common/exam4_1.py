import math

material_list = {  # 그대로 유지
    "유리":2.4,
    "알루미늄":2.7,
    "탄소강" : 7.87
}

def sphere_area(diameter: float, material: str, thickness: float = 1.0):
    # 내부에서는 최소한의 방어만 수행 (중복 검사 제거)  # 변경: 중복된 isinstance 검사 제거
    if not isinstance(diameter, (int, float)) or diameter <= 0: 
        raise ValueError  # 변경: int도 허용하도록 확장
    if not isinstance(thickness, (int, float)) or diameter <= 0: 
        raise ValueError # 변경: thickness 타입 검사 추가
    if material not in material_list: 
        raise ValueError  # 변경: 변수명 통일(material) 및 명확한 에러
    try:
        # 계산부: 입력은 이미 검증되었다고 가정  # 변경: 검증은 외부에서 수행하도록 구조 변경
        r = float(diameter) / 2.0  # 변경: 명시적 float 변환 및 2.0 사용
        area = 2.0 * math.pi * r**2  # 변경: 실수 연산 명시
        thickness_m = float(thickness) / 100.0  # 변경: mm->m 변환 명확화
        volume = area * thickness_m
        struct_weight = volume * float(material_list[material])  # 변경: material_list 접근에 material 사용
        struct_weight_mars = struct_weight * 0.38
    except:
        raise ValueError
    return area, struct_weight_mars

def is_valid_diameter(diameter):
    if diameter == "": 
        raise ValueError # 변경: 빈 문자열 명확 처리
    val = float(diameter)  # 변경: float 변환을 한 번만 수행
    if val <= 0: raise ValueError  # 변경: 0 이하 검사
    return val

def is_valid_material(material):
    if material == "": 
        raise ValueError  # 변경: 빈 문자열 처리
    if material not in material_list: 
        raise ValueError # 변경: 존재 여부 검사, 여기서 안해도 되기는 할것 같음
    return material

def is_valid_thickness(thickness):
    if thickness == "": 
        return 1.0  # 변경: 빈 문자열이면 기본값 반환
    else:
        val = float(thickness)  # try: except: 안걸어도 ValueError 발생
    if val <= 0: raise ValueError # 변경: 0 이하 검사
    return val

def main():
    try:
        diameter_raw = input("지름: ").strip()  # 변경: raw 변수명으로 명확화
        diameter = is_valid_diameter(diameter_raw)  # 변경: 입력 검증은 main에서 수행

        material_raw = input("재질: ").strip()
        material = is_valid_material(material_raw)  # 변경: 변수명 통일

        thickness_raw = input("두께 (기본 1.0 mm): ").strip()
        thickness = is_valid_thickness(thickness_raw)  # 변경: 기본값 처리 명확화

        area, mars_weight = sphere_area(diameter, material, thickness)  # 변경: 검증된 값 전달
        print(f'재질 : {material}, 지름 : {diameter:g}, 두께 : {thickness:g}, 면적 : {area:.3f}, 화성무게 : {mars_weight:.3f}kg')
    except ValueError:
        print("Invalid input.")  # 변경: 오타 수정(Invaild -> Invalid)
    except Exception:
        print("Processing Error")

if __name__ == "__main__":
    main()
