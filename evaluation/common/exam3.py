import json
import pprint
from datetime import datetime

LOG_FILE = 'data_source/mission_computer_main.log'

# 문제에서 로딩 펑션 주어짐 만지지 말고 에러처리만 처리하면 됨
def process_log_file(file_path=LOG_FILE, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError, IOError: #에러 나면 raise로 던지면 메인의 except: 로 전달됨 메인에 except:없다면 종료
        raise FileNotFoundError
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError
    except Exception as e:
        raise  


# class ProcessingError(Exception):
#     def __init__(self, message: str, stage: str, details: Optional[dict] = None):
#         super().__init__(message)
#         self.stage = stage
#         self.details = details or {}


def main():
    try:
        log_origin = process_log_file()
        print(f'=== log original DataSet Structure ===')
        print(f'{log_origin}\n\n')

        # log_list = [logs.strip('\n').split(',', 2) for logs in log_origin[1:]]

        log_list = []
        log_lines = log_list.splitlines()
        if log_lines[0] != 'timestamp,event,message':  #헤더가 없으면 에러
            raise ValueError
        for logs in log_lines[1:]:  #헤더 빼고 첫번째 줄부터
            # if len(logs) <22:
            #     raise ValueError
            log_data = logs.strip().split(',', 2)
            if len(log_data) == 3:
                time_stamp, log_level, message = log_data
                if datetime.strptime(time_stamp.strip(), '%Y-%m-%d %H:%M:%S'):  #시간포맷 에러 처리, 형식은 문제 맨 밑에 나옴
                    log_list.append((time_stamp.strip(), message.strip()))
                else:
                    raise (ValueError, TypeError)

        print(log_list)
        reversed_list = sorted(log_list, key=lambda x: x[0], reverse=True)
        print(reversed_list)
        dict_result = dict(reversed_list)
        print(dict_result)
    except FileNotFoundError, IOError:
        print("FileNotFoundError")  #메세지는 문제에 있는 그대로 복사해서출력할것 점 포함 
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
    except  ValueError: # 대부분 ValueError, TypeError를 Value error에 
        print('ValueError')  #메세지는 문제에 있는 그대로 복사해서출력할것 점 포함 
    except TypeError: # Type Error에 대한 처리는 문제어 없을것 같으나 변환시 에러는 Value Error처리해야할지도
        print('ValueError')  #메세지는 문제에 있는 그대로 복사해서출력할것 점 포함 
    except RuntimeError as e:  #리스트 변환시 그밖의 에러
        print('Processing Error')
    except Exception as e:
        print('Unexpected Exception.')


if __name__ == '__main__':
    main()
#try: except:를 여기서 몰아서 처리해도 됨 단 raise로 전달해야함. 
# try:
#    main()
# except FileNotFoundError, IOError:
#     print("FileNotFoundError")  #메세지는 문제에 있는 그대로 복사해서출력할것 점 포함 
# except UnicodeDecodeError:
#     print("UnicodeDecodeError")
# except  ValueError: # 대부분 ValueError, TypeError를 Value error에 
#     print('ValueError')  #메세지는 문제에 있는 그대로 복사해서출력할것 점 포함 
# except TypeError: # Type Error에 대한 처리는 문제어 없을것 같으나 변환시 에러는 Value Error처리해야할지도
#     print('ValueError')  #메세지는 문제에 있는 그대로 복사해서출력할것 점 포함 
# except RuntimeError as e:  #리스트 변환시 그밖의 에러
#     print('Processing Error')
# except Exception as e:
#     print('Unexpected Exception.')