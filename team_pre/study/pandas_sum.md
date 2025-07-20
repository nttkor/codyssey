# 라이브러리 임포트
import numpy as np
import pandas as pd

# 주피터에서 보이는 행 늘리기
pd.set_option('max_rows', 500)	
# 주피터에서 보이는 열 늘리기
pd.set_option('max_columns', 500)	

#################################################


# 데이터프레임 만들기
pd.DataFrame({'col':[data]})
pd.DataFrame([[20190103, 'Kim', 'H'],
              [20190222, 'Lee', 'W'],
              [20190531, 'Jeong', 'S']], columns = ['ID', 'name', 'class'])

# 행 조회
df.head()   # 상위 n개 값만 보이기   
df.tail()   # 하위 n개 값만 보이기   
df.sample()   # 랜덤으로 n개 값만 보이기  

# 데이터프레임의 열 이름 조회
df.columns

# 데이터타입 조회
df.dtypes / df['col'].dtypes	

# 데이터타입 변경
df.astype({'col1':'int'})
df['col'].astype('type')

# to_~
s.to_list()
s.to_frame()   # 데이터프레임으로 
pd.to_numeric(data)
pd.to_datetime(data)
s.to_timestamp()

# 데이터프레임 정보
df.info()

# 데이터프레임 형태
df.shape   # (행, 열)
df.ndim   # 행

# 기술통계
df.describe(include = 'all')

# 상관계수
data.corr()

# 공분산
data.cov()

# 누적~
data.cumsum()   # 누적합
data.cum**()   # **에 min, max, prod

# 고유값(Unique)
df.unique()

# 고유값의 갯수
data.nunique()

# 데이터의 갯수
data.count()

# 상위 n개 / 하위 n개
s.nlargest(n, keep = ) / s.nsmallest(n, keep = )


# 복사
df.copy()

# 값 선택하여 조회
df.loc[행, 열]
df.iloc['row', 'col']   # 인덱스
df.at[행, 'col']
df.iat[행, 열]   # 인덱스

# 행/열 삭제
df.drop(['A', 'B'], axis=1)



#################################################

# 결측값이 있는지
data.isnull() / data.isna()	

# 결측값이 아닌 값
data.notnull() / data.notna()

# 결측값이 있는 행 조회
df[df.isnull().any(axis=1)]

# 결측값 채우기
df.fillna('값')	

# 결측값이 있는 행/열 제외
pd.dropna()

#################################################


# 데이터 가져오기
pd.read_csv('path/file_name.csv')
pd.read_excel('path/file_name.xlsx')  
pd.read_table('path/file_name.csv', sep='t')
pd.read_table('URL')
pd.read_json('URL')

# 데이터 내보내기
pd.to_csv(df, 'path/file_name.csv', index = False)
pd.to_excel(df, 'path/file_name.xlsx', index = False, sheet_name = )

# 인덱스 재정렬
df.reset_index(drop = )	

# 인덱스 순으로 정렬
df.sort_index(ascending = , inplace = )	

# col을 기준으로 데이터프레임 정렬
df.sort_values(by = ['col'], ascending = False)	

# 중복 제거
df.drop_duplicates(['col1', 'col2'], keep='last')

# 데이터프레임 합치기
pd.concat([df1, df2], axis = 0)   # axis = 0(행)/1(열)
pd.merge(df1, df2, on = '기준', how = '방식')

# GroupBy
df.groupby(['col'], axis = 1, as_index = ).exp()	

# 피봇테이블
pd.pivot_table(df, values =, index =, columns =, values =, aggfunc =)

# melt : 열 이름을 기준으로 값 생성
pd.melt(df, id_vars = ['A'], value_vars = ['B', 'C']) 

# 속해있는 값 찾기 / 특정 값을 포함하는지
df.isin([리스트])
df.isin({'col' : [리스트]})
df['col'].isin([리스트])

# 문자를 포함하는지
df.contains('문자') / df['col'].str.contains('문자')

# 문자 변경
df.replace('Before', 'After') / df['col'].str.contains('Before', 'After')

# 데이터 옮기기
df.shift(periods=n, axis = 0, fill_value=0)

# n번째 값과의 차이
s.diff(periods=-n)

# 특정 기간의 시간 데이터 생성
pd.date_range(start = 'yyyy-mm-dd', end = 'yyyy-mm-dd', periods = 3, freq = 'M')

# One-Hot Encoding
pd.get_dummies(data)

# 조건에 따른 값 반환
np.where(조건, True, False)
