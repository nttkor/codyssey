from datetime import datetime

ctime = datetime.now()
print(ctime)
stime = ctime.strftime('%Y-%m-%d %H:%M:%S')
print(stime)
ptime = datetime.strptime(stime,'%Y-%m-%d %H:%M:%S')
print(ptime)