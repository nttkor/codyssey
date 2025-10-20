import math

material_dict = {
    '유리': 2.4,
    '알루미늄': 2.7,
    '탄소강': 7.85
}

def sphere_area(diameter,material,thickness):
    if not isinstance(diameter,float):
        raise ValueError
    # 문제에 계산식 다 있음 x를 *정도 바꾸면 되는데 
    try:
        pass



    except:
        raise ValueError # 여기서 나는건 전부 ValidError로 전달해야함.




    return round('면적', 3), round('무게', 3)

def main():
    try: #입력시 나는 에러는 전부 처리햐야함. 문제 잘 읽어 볼것
        diameter = input('지름을 입력하시오').strip()
        diameter = float(diameter)
        if not isinstance(diameter, float) and diameter <= 0:
            raise ValueError

        material = input('재질 입력').strip()
        if material not in material_dict.keys():
            raise ValueError

        thickness = input('두께를 입력하시오').strip()
        if thickness == '':
            thickness = 1.0
        if not isinstance(thickness, float) and thickness <= 0:
            raise ValueError

        print(diameter, material, thickness)

    except (TypeError, ValueError):
        print(f'Input Value Error.')
    except Exception as e:
        print('ProcessError')  #아마 기타 에러는 전부 프로세서 에러

if __name__ == '__main__':
    main()