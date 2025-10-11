def func1():
    raise OSError

def func2():
    try:
        raise ValueError
    except:
        raise TypeError

def func3():
    try:
        raise ValueError
    except Exception as e:
        raise
    
def main():

    func1()
    func2()




if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print('OSError')
    except ValueError as e:
        print('ValueError')
    except TypeError as e:
        print('TypeError')