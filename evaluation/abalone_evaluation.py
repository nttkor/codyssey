import pandas as pd  # pandas를 불러와 DataFrame 처리를 사용합니다

ATTR_PATH = "abalone_attributes.txt"  # 속성(헤더) 파일 경로를 작업 디렉토리 기준으로 고정합니다
DATA_PATH = "abalone.txt"  # 실제 데이터 파일 경로를 작업 디렉토리 기준으로 고정합니다


def load_attributes(path=ATTR_PATH):  # 속성 파일을 읽어 컬럼명 리스트를 반환하는 함수 정의
    try:  # 파일 열기에서 발생할 수 있는 예외를 처리하기 위해 try 블록을 사용합니다
        with open(path, "r", encoding="utf-8") as f:  # UTF-8로 파일을 열어 읽습니다
            cols = [line.strip() for line in f.readlines()]  # 각 줄에서 개행을 제거하고 리스트로 만듭니다
        return cols  # 컬럼명 목록을 호출자에게 반환합니다
    except FileNotFoundError:  # 파일이 존재하지 않을 경우의 예외를 잡습니다
        print("File open error")  # 요구사항에 맞는 정확한 에러 문자열을 출력합니다
        return  # 함수 종료(메인에서 None 체크로 중단)
    except UnicodeDecodeError:  # 디코딩 오류가 발생했을 때의 예외를 잡습니다
        print("Decoding error")  # 요구사항에 맞는 정확한 에러 문자열을 출력합니다
        return  # 함수 종료
    except Exception:  # 그 외 예기치 못한 모든 예외는 처리 단계 오류로 표기합니다
        print("Processing error")  # 처리 에러 메시지 출력
        return  # 함수 종료


def load_data(path=DATA_PATH, columns=None):  # 데이터를 읽어 DataFrame으로 반환하는 함수 정의
    try:  # 파일 읽기에서 발생 가능한 예외를 처리합니다
        # pandas로 CSV를 읽습니다. 파일에 헤더가 없으므로 names 파라미터로 컬럼명을 지정합니다
        df = pd.read_csv(path, names=columns, header=None)  # 구분자는 기본 콤마이며 header=None으로 원본 헤더 무시
        return df  # 읽은 DataFrame 반환
    except FileNotFoundError:  # 파일이 없을 때
        print("File open error")  # 요구사항에 맞는 문자열 출력
        return  # 호출자에서 None 확인
    except UnicodeDecodeError:  # 인코딩 문제가 있을 때
        print("Decoding error")  # 요구사항에 맞는 문자열 출력
        return  # 함수 종료
    except Exception:  # 그 외 처리 중 오류 발생 시
        print("Processing error")  # 처리 에러 메시지 출력
        return  # 함수 종료


def make_label(df):  # DataFrame에서 Sex 컬럼을 label로 복사하고 원래 Sex는 제거하는 함수 정의
    try:  # 예외가 발생할 수 있는 영역을 잡아냅니다
        df = df.copy()  # 원본 변경을 피하기 위해 복사본으로 작업합니다
        df["label"] = df["Sex"]  # 'Sex' 컬럼을 그대로 'label' 컬럼으로 복사합니다
        df = df.drop(columns=["Sex"])  # 원본 'Sex' 컬럼은 요구사항대로 제거합니다
        return df  # 변경된 DataFrame 반환
    except KeyError:  # 'Sex' 컬럼이 없을 경우 KeyError가 발생할 수 있습니다
        print("Processing error")  # 요구사항에 따라 처리 에러로 간주하여 메시지를 출력합니다
        return  # 함수 종료
    except Exception:  # 그 외 예외는 일반 처리 에러로 간주합니다
        print("Processing error")  # 처리 에러 메시지 출력
        return  # 함수 종료


def min_max_manual(df):  # label을 제외한 모든 수치 컬럼에 대해 수동 Min-Max 스케일링을 수행하는 함수 정의
    try:  # 스케일링 과정에서 발생하는 모든 예외를 잡습니다
        scaled = df.copy()  # 원본을 보존하기 위해 복사본을 사용합니다
        for col in df.columns:  # DataFrame의 모든 열(컬럼)을 순회합니다
            col_min = df[col].min()  # 현재 열의 최소값을 계산합니다
            col_max = df[col].max()  # 현재 열의 최대값을 계산합니다
            if pd.isna(col_min) or pd.isna(col_max):  # NaN이 있는 경우 처리 에러로 간주합니다
                print("Processing error")  # 처리 에러 메시지 출력
                return  # 함수 종료
            # 분모가 0이면(상수열) 요구사항대로 해당 열을 0.0으로 채웁니다
            if col_max == col_min:  # 분모 == 0 체크 (상수열 예외 처리)
                scaled[col] = 0.0  # 상수열의 모든 값을 0.0으로 설정합니다
            else:  # 정상적인 경우 Min-Max 수식을 적용합니다
                scaled[col] = (df[col] - col_min) / (col_max - col_min)  # (x - min) / (max - min)
        return scaled  # 스케일링된 DataFrame을 반환합니다
    except Exception:  # 어떤 예외가 발생하면 처리 에러로 처리합니다
        print("Processing error")  # 처리 에러 메시지 출력
        return  # 함수 종료


def main():  # 스크립트의 메인 흐름을 담당하는 함수 정의
    # 1) 속성(컬럼) 목록 로드
    cols = load_attributes()  # abalone_attributes.txt에서 컬럼명을 읽습니다
    if cols is None:  # 파일 관련 문제가 발생했으면 cols는 None이므로 즉시 반환합니다
        return  # 요구사항: 문제 발생 시 단순 return으로 종료 (sys.exit 금지)

    # 2) 데이터 로드 (컬럼명을 지정하여 읽기)
    df = load_data(columns=cols)  # abalone.txt 파일을 읽어 DataFrame 생성
    if df is None:  # 로딩 실패 시 None이 반환되므로 종료합니다
        return  # 반환하여 종료

    # 3) label 생성 및 Sex 컬럼 제거
    df = make_label(df)  # 'Sex'를 'label'로 복사하고 원본 Sex 컬럼 제거
    if df is None:  # make_label에서 문제가 발생하면 None을 반환하므로 종료
        return  # 반환하여 종료

    # 4) 결과 출력 준비
    # 출력 1: 원본 DataFrame 모양 (예: (N, 9))
    # 출력 2: label 분포를 dict로
    # 출력 3: 스케일된 데이터의 min/max 요약을 dict로

    # label 시리즈를 분리합니다
    label = df["label"]  # 'label' 컬럼만 따로 저장
    data = df.drop(columns=["label"])  # label을 제외한 모든 컬럼을 스케일링 대상으로 설정

    # 5) 수동 Min-Max 스케일링 적용
    scaled = min_max_manual(data)  # 직접 구현한 Min-Max 스케일링 함수 호출
    if scaled is None:  # 스케일링 중 오류 발생 시 None 반환되므로 종료
        return  # 반환하여 종료

    # 6) 최종 출력: 요구사항에 따라 정확히 3번만 print() 수행
    # 출력 내용은 문자열이 아닌 객체(튜플 등)를 print하더라도 문자열 표기로 출력되므로 허용됩니다
    print(df.shape)  # 1) 원본 DataFrame의 모양을 출력합니다 (예: (4177, 9))
    print(label.value_counts().to_dict())  # 2) label 분포를 value_counts 후 dict로 변환하여 출력합니다
    # 3) 스케일된 DataFrame의 min,max 행을 추출해 소수점 6자리로 반올림한 뒤 dict로 변환하여 출력합니다
    print(scaled.describe().loc[["min", "max"]].round(6).to_dict())  # min,max 요약을 dict로 출력


if __name__ == "__main__":  # 스크립트가 직접 실행될 때만 main()을 호출합니다
    main()  # 메인 함수 실행(파일 입출력 및 출력이 여기서 수행됩니다)
