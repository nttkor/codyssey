from datetime import datetime
now = datetime.now()
dtime = now.strftime('%Y-%m-%d %H:%M:%S')
print(type(dtime),dtime)
print(type(datetime.strptime(dtime,'%Y-%m-%d %H:%M:%S')))