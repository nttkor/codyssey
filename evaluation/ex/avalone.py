import pandas as pd # 데이터 처리를 위한 pandas 라이브러리 임포트
import os           # 파일 경로 처리를 위한 os 라이브러리 임포트

# 파일 경로 고정 (Colab 환경 기준, Google Drive 마운트 필요)
# abalone_attributes.txt와 abalone.txt가 Drive의 MyDrive 루트에 있다고 가정
ABALONE_ATTRIBUTES_PATH = "/content/drive/MyDrive/abalone_attributes.txt"
ABALONE_DATA_PATH = "/content/drive/MyDrive/abalone.txt"

# ------------------------------------------------------------
# 1. load_attributes(): 컬럼명(헤더) 파일을 읽어옵니다.
# ------------------------------------------------------------
def load_attributes(file_path):
    """
    abalone_attributes.txt 파일에서 컬럼명 리스트를 로드합니다.
    예외 처리: 파일 열기 실패, 디코딩 에러
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # 각 줄의 양쪽 공백 및 개행 문자를 제거하여 리스트 생성
            columns = [line.strip() for line in f]
        return columns
    except FileNotFoundError:
        print("File open error") # 파일이 없을 경우 에러 메시지 출력
        return None # None 반환하여 상위 함수에 에러 알림
    except UnicodeDecodeError:
        print("Decoding error") # 인코딩 문제가 발생할 경우 에러 메시지 출력
        return None
    except Exception as e:
        print(f"Processing error: {e}") # 기타 예외 처리
        return None

# ------------------------------------------------------------
# 2. load_data(): abalone.txt 파일을 읽어 DataFrame을 생성합니다.
# ------------------------------------------------------------
def load_data(file_path, columns):
    """
    abalone.txt 파일을 지정된 컬럼명으로 읽어 pandas DataFrame을 생성합니다.
    헤더가 없으므로 header=None을 사용합니다.
    예외 처리: 파일 열기 실패, 디코딩 에러, 기타 파싱 에러
    """
    try:
        # pd.read_csv를 사용하여 데이터 파일 로드
        # names=columns: 미리 로드한 컬럼명을 지정
        # header=None: 파일에 헤더가 없음을 명시
        df = pd.read_csv(file_path, names=columns, header=None)
        return df
    except FileNotFoundError:
        print("File open error")
        return None
    except UnicodeDecodeError:
        print("Decoding error")
        return None
    except Exception as e:
        print(f"Processing error: {e}") # 파싱 과정 등에서 발생할 수 있는 기타 예외 처리
        return None

# ------------------------------------------------------------
# 3. make_label(): 'Sex' 컬럼을 'label'로 분리하고 원본을 제거합니다.
# ------------------------------------------------------------
def make_label(df):
    """
    DataFrame에서 'Sex' 컬럼을 'label' 컬럼으로 복사하고, 원본 'Sex' 컬럼을 제거합니다.
    예외 처리: 'Sex' 컬럼이 없는 경우
    """
    try:
        # 원본 DataFrame을 직접 수정하지 않도록 .copy()를 사용하여 복사본 생성
        processed_df = df.copy()
        # 'Sex' 컬럼의 값을 'label'이라는 새 컬럼으로 복사
        processed_df["label"] = processed_df["Sex"]
        # 원본 'Sex' 컬럼 제거
        processed_df = processed_df.drop(columns=["Sex"])
        return processed_df
    except KeyError:
        print("Processing error: 'Sex' column not found.") # 'Sex' 컬럼이 없을 경우 에러 메시지
        return None
    except Exception as e:
        print(f"Processing error during label creation: {e}")
        return None

# ------------------------------------------------------------
# 4. min_max_manual(): Min-Max 스케일링을 수동으로 구현합니다.
# ------------------------------------------------------------
def min_max_manual(df):
    """
    Min-Max 스케일링을 수동으로 구현합니다. label을 제외한 모든 수치형 컬럼에 적용합니다.
    분모가 0인 상수열의 경우 해당 열을 0.0으로 채웁니다.
    예외 처리: NaN 값 발견, 계산 중 오류
    """
    try:
        # 스케일링 결과를 저장할 DataFrame 복사본 생성
        scaled = df.copy()
        # DataFrame의 모든 컬럼을 순회
        for col in df.columns:
            # 현재 컬럼의 최소값과 최대값 계산
            col_min = df[col].min()
            col_max = df[col].max()

            # 최소값 또는 최대값이 NaN인 경우 처리 에러로 간주
            if pd.isna(col_min) or pd.isna(col_max):
                print("Processing error: NaN values found in min/max calculation.")
                return None

            # 분모(최대값 - 최소값)가 0인 경우 (상수열)
            if col_max == col_min:
                scaled[col] = 0.0  # 해당 컬럼을 모두 0.0으로 채움
            else:
                # Min-Max 스케일링 공식 적용: (x - min) / (max - min)
                scaled[col] = (df[col] - col_min) / (col_max - col_min)
        return scaled # 스케일링된 DataFrame 반환
    except Exception as e:
        print(f"Processing error during Min-Max scaling: {e}") # 기타 예외 처리
        return None

# ------------------------------------------------------------
# 5. main(): 전체 프로그램의 흐름을 제어합니다.
# ------------------------------------------------------------
def main():
    # 1. 컬럼명 로드
    columns = load_attributes(ABALONE_ATTRIBUTES_PATH)
    if columns is None: return # 에러 발생 시 종료

    # 2. 데이터 로드
    df = load_data(ABALONE_DATA_PATH, columns)
    if df is None: return # 에러 발생 시 종료

    # 3. 'Sex' 컬럼을 'label'로 분리하고 원본 'Sex' 제거
    df = make_label(df)
    if df is None: return # 에러 발생 시 종료

    # 4. 'label' 컬럼 분리 및 수치형 데이터 추출
    label_series = df["label"] # 'label' 컬럼은 Series 형태로 저장
    # 스케일링 대상에서 'label' 컬럼 제외
    data_for_scaling = df.drop(columns=["label"]) 
    
    # 데이터 타입 확인 및 필요한 경우 변환 (모든 컬럼이 숫자형이어야 스케일링 가능)
    # 예를 들어, 'Rings'가 object 타입으로 읽혔을 경우를 대비
    for col in data_for_scaling.columns:
        if data_for_scaling[col].dtype == 'object':
            try:
                data_for_scaling[col] = pd.to_numeric(data_for_scaling[col])
            except ValueError:
                print(f"Processing error: Column '{col}' contains non-numeric values and cannot be scaled.")
                return


    # 5. Min-Max 스케일링 수행
    scaled_data = min_max_manual(data_for_scaling)
    if scaled_data is None: return # 에러 발생 시 종료

    # ------------------------------------------------------------
    # 최종 출력 (요구사항에 따른 3가지 print 문만 수행)
    # ------------------------------------------------------------

    # 1. 원본 data frame 모양 (label 컬럼이 포함된 상태의 df.shape를 출력)
    print(df.shape)

    # 2. 라벨 분포 (label_series의 value_counts 결과를 딕셔너리로 변환하여 출력)
    print(label_series.value_counts().to_dict())

    # 3. 스케일 결과의 상, 하한 요약 (scaled_data의 describe 결과에서 min, max만 추출하여 출력)
    # round(6)으로 소수점 6자리까지 반올림
    print(scaled_data.describe().loc[["min", "max"]].round(6).to_dict())

# ------------------------------------------------------------
# 스크립트 직접 실행 시 main 함수 호출
# ------------------------------------------------------------
if __name__ == "__main__":
    # Google Drive 마운트 (Colab 환경에서 필요)
    # 이 부분은 노트북의 다른 셀에서 이미 실행되었을 수 있으므로 주석 처리하거나
    # 필요에 따라 활성화하여 테스트하세요.
    # from google.colab import drive
    # drive.mount('/content/drive')

    main()