# design_dome.py
import math

# 전역 변수 (마지막 결과 저장용)
last_result = {}

# 재질별 밀도 (kg/m³)
material_dict = {
    '유리': 2400,
    '알루미늄': 2700,
    '탄소강': 7850
}

def sphere_area(diameter, material, thickness=0.01):
    """반구체 돔의 면적(m²)과 무게(kg, 화성 중력 반영)를 계산한다.
       diameter: m, material: 문자열, thickness: m (기본 0.01m=1cm)
    """
    if material not in material_dict:
        raise ValueError("지원하지 않는 재질입니다. (유리/알루미늄/탄소강 중 선택)")
    if diameter <= 0:
        raise ValueError("지름은 양수여야 합니다.")
    if thickness <= 0:
        raise ValueError("두께는 양수여야 합니다.")

    density = material_dict[material]     # kg/m³
    radius = diameter / 2                 # m
    area_m2 = 2 * math.pi * (radius ** 2) # 반구 표면적 (곡면만), m²
    volume_m3 = area_m2 * thickness       # 체적 m³
    mass = density * volume_m3            # kg

    # 화성 중력 반영 (질량 * 0.38)
    mars_mass = mass * 0.38

    # 전역 변수 저장 (출력용)
    global last_result
    last_result = {
        "재질": material,
        "지름": f"{diameter} m",
        "두께": f"{thickness*100:.1f} cm",  # 다시 cm로 출력
        "면적": f"{area_m2:.3f} m²",
        "무게": f"{mars_mass:.3f} kg"
    }

    return area_m2, mars_mass


def main():
    print("=== Mars 돔 구조물 설계 프로그램 ===")
    while True:
        try:
            diameter_input = input("지름(m)을 입력하세요 (종료하려면 exit): ")
            if diameter_input.lower() == "exit":
                print("프로그램을 종료합니다.")
                break
            diameter = float(diameter_input)

            material = input("재질을 입력하세요 (유리/알루미늄/탄소강): ").strip()
            thickness_input = input("두께(cm)를 입력하세요 (기본 1): ").strip()
            thickness_m = float(thickness_input)/100 if thickness_input else 0.01

            # 계산 실행
            sphere_area(diameter, material, thickness_m)

            # 결과 출력
            print(f"재질 ⇒ {last_result['재질']}, "
                  f"지름 ⇒ {last_result['지름']}, "
                  f"두께 ⇒ {last_result['두께']}, "
                  f"면적 ⇒ {last_result['면적']}, "
                  f"무게 ⇒ {last_result['무게']}")

        except ValueError as e:
            print(f"[입력 오류] {e}")
        except Exception as e:
            print(f"[예상치 못한 오류] {e}")


if __name__ == "__main__":
    main()
