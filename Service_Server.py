# -*- encoding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import socket
from flask import Flask, render_template, request
import threading
import os
import time
import json

SERVER_IP = ""
SERVER_PORT = ""

def run_model():
    time.sleep(3)
    os.system('./model')

with open("Setting.ini", 'r') as f:
    data = f.read()
    data = data.split('\n')
    SERVER_IP = data[0].split(': ')[1]
    SERVER_PORT = data[1].split(': ')[1]

line1 = {"청량리": 158, "제기동": 157, "신설동": 156, "동묘앞": 159, "동대문": 155, "종로5가": 154, "종로3가": 153,
         "종각": 152 , "시청": 151, "서울": 150}
line2 = {"시청": 201, "을지로입구": 202, "을지로3가": 203, "을지로4가": 204, "동대문역사문화공원": 205, "신당": 206, "상왕십리": 207,
         "왕십리": 208, "한양대": 209, "뚝섬": 210, "성수": 211, "건대입구": 212, "구의": 213, "강변": 214, "잠실나루": 215, "잠실": 216,
         "신천": 217, "종합운동장": 218, "삼성": 219, "선릉": 220, "역삼": 221, "강남": 222, "교대": 223, "서초": 224, "방배": 225,
         "사당": 226, "낙성대": 227, "서울대입구": 228, "봉천": 229, "신림": 230, "신대방": 231, "구로디지털단지": 232, "대림": 233, "신도림": 234,
         "문래": 235, "영등포구청": 236, "당산": 237, "합정": 238, "홍대입구": 239, "신촌": 240, "이대": 241, "아현": 242, "충정로": 243,
         "용답": 244, "신답": 245, "신설동": 246, "도림천": 247, "양천구청": 248, "신정네거리": 249, "용두": 250,
}

line3 = {"수서": 339, "일원": 338, "대청": 337, "학여울": 336, "대치": 335, "도곡": 334, "매봉": 333, "양재": 332, "남부터미널": 331,
         "교대": 330, "고속터미널": 329, "잠원": 328, "신사": 327, "압구정": 326, "옥수": 325, "금호": 324, "약수": 323, "동대입구": 322,
         "충무로": 321, "을지로3가": 320, "종로3가": 319, "안국": 318, "경복궁": 317, "독립문": 316, "무악재":315, "홍제": 314, "녹번": 313,
         "불광": 312, "연신내": 311, "구파발": 310, "지축": 309}

line4 = {"당고개": 409, "상계": 410, "노원": 411, "창동": 412, "쌍문": 413, "수유": 414, "미아": 415, "미아사거리": 416,
         "길음": 417, "성신여대입구": 418, "한성대입구": 419, "혜화": 420, "동대문": 421, "동대문역사문화공원": 422, "충무로": 423,
         "명동": 424, "회현": 425, "서울역": 426, "숙대입구": 427, "삼각지": 428, "신용산": 429, "이촌": 430, "동작": 431,
         "총신대입구": 432, "사당": 433, "남태령": 434,
}

thread = threading.Thread(target=run_model)
thread.start()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 1
sock.bind(("127.0.0.1", 11120))
sock.listen(5)

client = sock.accept()[0]
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)
print client.recv(1000)

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        input_value = request.form['line'].encode('utf-8') + " " + request.form['station'].encode('utf-8') + " "+  request.form['time'].encode('utf-8')
        input_value = input_value.strip("\n").split(" ")
        if input_value[0] == "1":
            input_value[1] = str(line1[input_value[1]])
        if input_value[0] == "2":
            input_value[1] = str(line2[input_value[1]])
        if input_value[0] == "3":
            input_value[1] = str(line3[input_value[1]])
        if input_value[0] == "4":
            input_value[1] = str(line4[input_value[1]])
        client.send(' '.join(input_value))
        busy = client.recv(100)
        table = "<table>" \
                "<tr><th>Line</th><th>Station</th><th>Time</th>" \
                "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" \
                "</table>"

    return "111"

@app.route('/keyboard', methods = ['GET', 'POST'])
def requests():
    res = {'type':'text'}
    return json.dumps(res)

@app.route('/message', methods = ['GET', 'POST'])
def response():
    if request.method == 'POST':
        input_value = request.json['content']
        input_value = input_value.encode('UTF-8')
        message = ''
        fmt = '%d호선 %s역: %s'
        cur_time = ':'.join(time.ctime().split(' ')[4].split(':')[:2])
        line = {}
        line.update(line1)
        line.update(line2)
        line.update(line3)
        line.update(line4)
        res = {}

        if input_value == '도움말':
            message += '서울 메트로가 관리하는 1 ~ 4호선 지하철역의 승객 혼잡도를 알려주는 봇입니다.' \
                       '' \
                       '지하철 역을 이용하는 승객의 수가 2000명 이상이면 혼잡을, 그렇지 않으면 한적하다고 알려줍니다.' \
                       '' \
                       '지하철역 이름만 입력하시면 현재시간 그 지하철역의 혼잡도를 알려줍니다. 특정 시간 지하철역의 혼잡도를 알고 싶으시면 지하철역 이름과 시간을 입력해주세요.'
            res['message'] = {'text':message}
            return json.dumps(res)
        else:
            for key, value in line.iteritems():
                if input_value in key:
                    client.send(str(value/100)+' '+str(value)+' '+cur_time)
                    busy = client.recv(100).strip('\n')
                    if busy == 'Busy':
                        message += fmt %(value/100, key, '혼잡(이용객 2000명 이상)')
                    else:
                        message += fmt % (value/100, key, '한적(이용객 2000명 미만)')
                    message += '\n'
            # if input_value[0] == "1":
            #     input_value[1] = str(line1[input_value[1]])
            # if input_value[0] == "2":
            #     input_value[1] = str(line2[input_value[1]])
            # if input_value[0] == "3":
            #     input_value[1] = str(line3[input_value[1]])
            # if input_value[0] == "4":
            #     input_value[1] = str(line4[input_value[1]])
            # client.send(' '.join(input_value))
            # busy = client.recv(100)
            res['message'] = {'text':message}
            res['message_button'] = {'label':'만족'}
            return json.dumps(res)
    return 1111

if __name__ == '__main__':
    app.run(host=SERVER_IP, port=int(SERVER_PORT))