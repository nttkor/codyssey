from datetime import datetime
def func1():
    ctime = datetime.now()
    print(ctime)
    stime = ctime.strftime('%Y-%m-%d %H:%M:%S')
    print(stime)
    ptime = datetime.strptime(stime,'%Y-%m-%d %H:%M:%S')
    print(ptime)
def func2():
    try:
        time = datetime.now()
        stime = str(time)
        strtime = datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
        dtime = datetime.strptime(strtime+":",'%Y-%m-%d %H:%M:%S')
        print(stime,isinstance(stime,str))
        print(strtime, type(strtime))
        print(dtime, type(dtime))
    except Exception as e:
        print("datetime Error", e)


        

func2()