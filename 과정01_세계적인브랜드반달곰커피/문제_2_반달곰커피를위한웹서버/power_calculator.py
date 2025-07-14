def inputNum()->float:
    while True:
        try: 
            num = float(input("Enter number: "))
            return num
        except:
            print('Invalid number input.')

def inputExponent()->int:
    while True:
        try: 
            num = int(input("Enter exponent: "))
            return num
        except:
            print('PInvalid exponent input.')
def main():
    num = inputNum()
    exp = inputExponent()
    minus = False
    if(exp<0):
        exp = abs(exp)
        minus = True
        print(exp)

    sum = 1
    for v in range(exp):
        if minus == False:
            sum *= num
        else:
            sum /= num
    print(f"Result:{sum}")

if __name__ == "__main__":
    main()


