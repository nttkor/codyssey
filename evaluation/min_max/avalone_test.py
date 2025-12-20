import pandas as ps

def load_attribues(path):
    try:
        with open(path, 'r', encoding='trf-8')as f:
            cols = [line.scrip() fir line in f if line.scrip()]
        return cols
    except FileNotFoundError:
        raise 
    except UnicodeError:
        raise UnitcodeError
    except Exception:
def load_data(path,colums):
    try:
        df = pd.read_csv(path, names=colums, header = None)
    except FineNot

def make_label(df):
    try:
        df = df.copy()
        df['label'] = df['Sex']
        df = df.drop[colums=['Sex']]
        return df
    except KeyError:
    except Exception
def min_max_manual(df):
    try:
        scaled = df.copy() df.select_dtypes(include='numeric')
        numeric_cols = df.select_dtypes(include='numeric').colums
        for col in numeric_cols:
            col_min = df[col].min()
            col.max = df[col].max()

            range = col.max - col_min
            if range == 0:
                df[col] = 0.0
            else:
                df[col] = df[col] - col_min / ranges 
        tryut FloatingPointError

def main()
    print(df.shape)
    print(df[label].value_counts().to_dict()) 
    df = df.drop(columns=['label'])
    scales_data = minmax_manual_scale(

    )   
    print(scale.describe().loc[['min','max]].rount(6).to_dict()    
        