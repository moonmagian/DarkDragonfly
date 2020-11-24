import requests
import gzip
import random
from datetime import datetime
import uuid
import generate_point

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "close",
    "Charset": "UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; SOT31 Build/32.3.C.0.403)",
    'Accept-Encoding': 'gzip, deflate'
}


def make_rundata(begin: int, end: int, username: str, uid: str):
    run = generate_point.generate_points(begin, end, 4)

    data_str = "{'begintime':'%d','endtime':'%d','uid':'%s','schoolno':'10006','distance':'%f','speed':'%f','studentno':'%s','atttype':'2','eventno':'803','location':'%s','pointstatus':'1','usetime':'%f'}" % (
        run[1], run[2], uid, run[4], run[5], username, run[0], run[3])
    return data_str


def login(username: str):
    data = {'name': "['bangdingschool','10006','%s','%s']" % (
        username, uuid.uuid4())}
    result = requests.post(
        'http://quantiwang.cn:8012/cloud/DflyServer', data=data)
    return result.text.split(',')[2]


def login_info(username: str):
    data = {'name': "['bangding','10006','student','%s','21218cca77804d2ba1922c33e0151105']" % (
        username)}
    result = requests.post(
        'http://quantiwang.cn:8012/cloud/DflyServer', data=data)
    return result.text


def get_count(username: str, uid: str):
    datastr = "{'studentno':'%s','uid':'%s'}" % (username, uid)
    data = gzip.compress(datastr.encode('ascii'))
    result = requests.post("http://202.112.131.80:8015/DragonFlyServ/Api/webserver/getRunDataSummary",
                           data=data, headers=headers)
    # rn =
    return int(result.json()['m'].split(':')[1])


def run_all(username: str, uid: str):
    for i in range(1, 80):
        datastr = make_rundata(1605680322 - 86400 * i - random.randint(200, 300),
                               1605680322 - 86400 * i + random.randint(200, 300), username, uid)
        data = gzip.compress(datastr.encode('ascii'))
        result = requests.post("http://202.112.131.80:8015/DragonFlyServ/Api/webserver/uploadRunDataNew",
                               data=data, headers=headers)
        print(result.text)


if __name__ == "__main__":
    # run_all('test')
    username = input('username:')
    print(login_info(username))
    check = input('you? [y/n]:')
    if (check == 'y'):
        uid = login(username)
        # print(get_count(username, uid))
        print('Cyber running...')
        run_all(username, uid)
        print('Done.')
        print('Now you run %d times.' % get_count(username, uid))
    elif (check == 'n'):
        print('bye.')
    else:
        print("What's your problem?")
