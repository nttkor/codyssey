# 문제 2. Mars 돔 구조물 설계 프로그램
# 수행 과제
# 반구체 돔의 표면적과 무게를 계산하는 함수 sphere_area()를 정의한다.
# 함수는 다음 파라미터를 가진다:
# diameter (단위: m)
# material: 유리(glass), 알루미늄(aluminum), 탄소강(carbon_steel)
# thickness: 기본값 1cm
# 지름과 재질은 input()을 통해 사용자로부터 입력받는다.
# 재질의 밀도 (g/cm³)
# 유리: 2.4
# 알루미늄: 2.7
# 탄소강: 7.85
# 결과 출력 시:
# 면적은 소수점 3자리까지
# 무게는 **화성 중력(지구 중력의 약 0.38배)**을 반영하여 출력
# 전역 변수 저장 및 다음 형식으로 출력:
# 재질 ⇒ 유리, 지름 ⇒ 10, 두께 ⇒ 1, 면적 ⇒ 314.159, 무게 ⇒ 500.987 kg
material = {
    '유리':2.4, "알루미늄":2.7, "탄소강":7.85
}
def sphere_area(diameter,material,thickness=1):
    
def main():
    diameter = 1 #m
    material = '유리' 
    thickness = 1 # cm
    sphere_area(diameter, material,thickness)
    
    return
if __main__ == '__main__':
    main()

# 프로그램은 반복 실행되어야 하며, 종료 조건도 구현되어야 한다.
# 잘못된 입력(예: 지름이 0이거나 숫자가 아님)에 대해 예외 처리가 되어 있어야 한다.
# 저장 파일
# 코드 파일은 반드시 design_dome.py로 저장
# 보너스 과제
# material, diameter, thickness 파라미터에 유효하지 않은 값이 들어왔을 때 예외 처리가 되어 있어야 한다.