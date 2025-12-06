import pandas as pd

def load_attributes():
    try:
        with open("abalone_attributes.txt", "r", encoding="utf-8") as f:
            cols = [line.strip() for line in f.readlines() if line.strip()]
        return cols
    except FileNotFoundError:
        print("File open error.")
        return None
    except UnicodeDecodeError:
        print("Decoding error.")
        return None

def load_data(columns):
    try:
        df = pd.read_csv("abalone.txt", header=None, names=columns, encoding="utf-8")
        return df
    except FileNotFoundError:
        print("File open error.")
        return None
    except UnicodeDecodeError:
        print("Decoding error.")
        return None
    except Exception:
        print("Processing error.")
        return None

def make_label(df):
    try:
        df["label"] = df["Sex"]
        df = df.drop(columns=["Sex"])
        return df
    except Exception:
        print("Processing error.")
        return None

def minmax_manual(df):
    try:
        scaled = df.copy()
        numeric_cols = scaled.select_dtypes(include="number").columns
        for col in numeric_cols:
            x_min = scaled[col].min()
            x_max = scaled[col].max()
            denom = x_max - x_min
            if denom == 0:
                scaled[col] = 0.0
            else:
                scaled[col] = (scaled[col] - x_min) / denom
        return scaled
    except Exception:
        print("Processing error.")
        return None
    

def main():
    try:
        cols = load_attributes()

        df = load_data(cols)
        print(df.shape)

        df = make_label(df)
        print(df["label"].value_counts().to_dict())

        scaled = minmax_manual(df.drop(columns=["label"]))
        
        print(scaled.describe().loc[["min", "max"]].round(6).to_dict())
    except FileNotFoundError:
        print("File open error.")
        return
    except UnicodeDecodeError:
        print("Decoding Error.")
        return
    except Exception:
        print("Processing error.")
        return


if __name__ == "__main__":
    main()