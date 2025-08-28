import math

# 재질 밀도 (g/cm³)
material_density = {
    "glass": 2.4,
    "aluminum": 2.7,
    "carbon_steel": 7.85
}

# 화성의 중력 (지구의 중력의 약 0.38배)
mars_gravity = 0.38

# 돔의 표면적과 무게 계산 함수
def sphere_area(diameter, material, thickness=1):
    # 유효한 재질 체크
    if material not in material_density:
        raise ValueError("유효한 재질을 입력하세요: glass, aluminum, carbon_steel")

    # 지름을 cm로 변환 (1 m = 100 cm)
    diameter_cm = diameter * 100

    # 면적 계산 (두께를 고려한 실제 표면적 계산)
    outer_radius = (diameter_cm + thickness) / 2  # 지름 + 두께로 외부 반지름
    inner_radius = (diameter_cm - thickness) / 2  # 지름 - 두께로 내부 반지름

    # 외부 구의 표면적에서 내부 구의 표면적을 빼서 실제 표면적 계산
    outer_surface_area = 2 / 3 * math.pi * outer_radius**3  # 외부 반구 표면적
    inner_surface_area = 2 / 3 * math.pi * inner_radius**3  # 내부 반구 표면적
    surface_area = outer_surface_area - inner_surface_area  # 두께를 고려한 표면적

    # 재질의 밀도에 맞는 무게 계산
    # 두께는 cm 단위로 계산되므로 이를 변환하여 cm³로 부피 계산
    thickness_cm = thickness  # 기본 두께는 1cm
    volume = 2 * math.pi * (outer_radius**2) * (thickness_cm)  # cm³ 단위로 계산
    mass_in_grams = volume * material_density[material]  # g 단위

    # 화성 중력 반영 (kg 단위로 변환 후 적용)
    mass_in_kg = mass_in_grams / 1000  # g -> kg 변환
    weight_on_mars = mass_in_kg * mars_gravity  # 화성 중력 반영

    return surface_area, weight_on_mars

# 프로그램 메인 함수
def main():
    material_options = {
        "1": "glass",
        "2": "aluminum",
        "3": "carbon_steel"
    }

    while True:
        try:
            # 사용자 입력
            diameter_input = input("지름을 입력하세요 (m):  -> 0:종료.")
            if diameter_input.lower() == '0':
                print("프로그램을 종료합니다.")
                break
            diameter = float(diameter_input)

            if diameter <= 0:
                print("지름은 0보다 커야 합니다. 다시 입력하세요.")
                continue

            # 재질 선택
            print("재질을 선택하세요:")
            print("1. glass")
            print("2. aluminum")
            print("3. carbon_steel")
            material_choice = input("선택 (1, 2, 3): ")

            if material_choice not in material_options:
                print("유효한 선택을 입력하세요. (1, 2, 3)")
                continue
            material = material_options[material_choice]

            thickness_input = input("두께를 입력하세요 (cm, 기본값 1): ")
            if thickness_input.strip() == "":
                thickness = 1  # 기본값
            else:
                thickness = float(thickness_input)

            if thickness <= 0:
                print("두께는 0보다 커야 합니다. 다시 입력하세요.")
                continue

            # 돔의 표면적과 무게 계산
            surface_area, weight_on_mars = sphere_area(diameter, material, thickness)

            # 결과 출력
            print(f"재질 ⇒ {material}, 지름 ⇒ {diameter} m, 두께 ⇒ {thickness} cm, 면적 ⇒ {surface_area:.3f} cm², 무게 ⇒ {weight_on_mars:.3f} kg")

        except ValueError as e:
            print(f"잘못된 입력입니다: {e}. 다시 시도해 주세요.")

if __name__ == "__main__":
    main()
