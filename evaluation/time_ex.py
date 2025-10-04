from datetime import datetime as dt
def main():
    now = dt.now()
    print(now)
    datetime_str = dt.strftime(now,'%Y-%m-%d %H:%M:%S')
    str_datetime = dt.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
    print(now, datetime_str, str_datetime)
if __name__ == '__main__':
    main()