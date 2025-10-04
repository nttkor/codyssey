class MyFileError(Exception): pass
def read_file():
    try:
        with open('ython/password.txt',mode='r') as f:
            return f.read()
    except Exception:
        raise MyFileError("파일 열기 실패")
    else:
        print("open sucessfuly")

def main():
    try:
        print("main start")
        data = read_file()
        print(data)

    except MyFileError as e:
        print(e)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()