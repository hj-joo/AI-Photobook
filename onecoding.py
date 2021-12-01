from operator import ne
from PIL import Image
import numpy as np
import os, re
from PIL.ExifTags import TAGS
import googlemaps
import cv2 
from deepface import DeepFace
import random
import time
import sys

from numpy.lib.type_check import real
start = time.time()  # 시작 시간 저장

"""
중복 사진 제거

""" 
    # 이미지 데이터를 Average Hash로 변환하기 --- (※1)
def average_hash(fname, size = 16):
        img = Image.open(fname) # 이미지 데이터 열기---(※2)
        img = img.convert('L') # 그레이스케일로 변환하기 --- (※3)
        img = img.resize((size, size), Image.ANTIALIAS) # 리사이즈하기 --- (※4)
        pixel_data = img.getdata() # 픽셀 데이터 가져오기 --- (※5)
        pixels = np.array(pixel_data) # Numpy 배열로 변환하기 --- (※6)
        pixels = pixels.reshape((size, size)) # 2차원 배열로 변환하기 --- (※7)
        avg = pixels.mean() # 평균 구하기 --- (※8)
        diff = 1 * (pixels > avg) # 평균보다 크면 1, 작으면 0으로 변환하기 --- (※9)
        return diff

# # 이진 해시로 변환하기 --- (※10)
# def np2hash(ahash):
#     bhash = []
#     for nl in ahash.tolist():
#         sl = [str(i) for i in nl]
#         s2 = "".join(sl)
#         i = int(s2, 2) # 이진수를 정수로 변환하기
#         bhash.append("%04x" % i)
#     return "".join(bhash)
# Average Hash 출력하기

# ahash = average_hash('./Camera Roll/angry_boy.jpg')
# print(ahash)
# print(np2hash(ahash))

# 파일 경로 지정하기
search_dir = "./Camera Roll/"
cache_dir = "./cache"
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)
# 이미지 데이터를 Average Hash로 변환하기 --- (※1)
def average_hash(fname, size = 16):
    fname2 = fname[len(search_dir):]
    # 이미지 캐시하기
    cache_file = cache_dir + "/" + fname2.replace('/', '_') + ".csv"
    if not os.path.exists(cache_file): # 해시 생성하기
        img = Image.open(fname)
        img = img.convert('L').resize((size, size), Image.ANTIALIAS)
        pixels = np.array(img.getdata()).reshape((size, size))
        avg = pixels.mean()
        px = 1 * (pixels > avg)
        np.savetxt(cache_file, px, fmt="%.0f", delimiter=",")
    else: # 캐시돼 있다면 읽지 않기
        px = np.loadtxt(cache_file, delimiter=",")
    return px

# 해밍 거리 구하기 --- (※2)
def hamming_dist(a, b):
    aa = a.reshape(1, -1) # 1차원 배열로 변환하기
    ab = b.reshape(1, -1)
    dist = (aa != ab).sum()
    return dist
# 모든 폴더에 처리 적용하기 --- (※3)
def enum_all_files(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            fname = os.path.join(root, f)
            if re.search(r'\.(jpg|jpeg|png)$', fname):
                yield fname

 #이미지 찾기 --- (※4)
def find_image(fname, rate):
    src = average_hash(fname)
    for fname in enum_all_files(search_dir):
        dst = average_hash(fname)
        diff_r = hamming_dist(src, dst) / 256
        # print("[check] ",fname)
        if diff_r < rate:
            yield (diff_r, fname)
# 찾기 --- (※5)
from os import unlink
photo_list = []
for f in os.listdir('./Camera Roll'):
    if 'jpg' in f:
        photo_list.append(f)
# print(photo_list)

for i in photo_list:
    srcfile = search_dir + i
    html = ""
    sim = list(find_image(srcfile, 0.99))
    sim = sorted(sim, key=lambda x:x[0])
    #print(sim)
    for r, f in sim:
        #print(r, ">", f)
        if r <= 0.1:
            if sim[0][1] == f:
                continue
            unlink(f)
    # s = '<div style="float:left;"><h3>[ 차이 :' + str(r) + '-' + \
    #     os.path.basename(f) + ']</h3>'+ \
    #     '<p><a href="' + f + '"><img src="' + f + '" width=400>'+ \
    #     '</a></p></div>'
    # html += s

# HTML로 출력하기
# html = """<html><head><meta charset="utf8"></head>
# <body><h3>원래 이미지</h3><p>
# <img src='{0}' width=400></p>{1}
# </body></html>""".format(srcfile, html)
# with open("./avhash-search-output.html", "w", encoding="utf-8") as f:
#     f.write(html)
# print("ok")
"""
사진 정보 빼오기

"""
path = "./Camera Roll"
file_lst = os.listdir(path)
info_date=[]
for file in file_lst:
    filepath = path + '/' + file
    


    gmaps = googlemaps.Client(key='{API_KEY}')

    image = Image.open(path + '/'+file)

    info = image._getexif()
    image.close()
    taglabel = {}



    def get_decimal_from_dms(dms, ref):
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 5)

    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            taglabel[decoded] = value
        exifGPS = taglabel["GPSInfo"]
        latData =  get_decimal_from_dms(exifGPS[2], exifGPS[1])
        longData = get_decimal_from_dms(exifGPS[4], exifGPS[3])


        reverse_geocode_result = gmaps.reverse_geocode((latData,longData), language='ko')
        #print(reverse_geocode_result[1])
        #print(taglabel['DateTimeOriginal'])
        """
        주소 중 가장 디테일한 정보를 담기 위해서 재설정
        """
        add1= reverse_geocode_result[0]['formatted_address']
        add2= reverse_geocode_result[1]['formatted_address']
        add3= reverse_geocode_result[2]['formatted_address']
        address = [add1, add2, add3]
        for i in address:
            if len(i) == max(len(add1),len(add2),len(add3)):
                add = i
                break
        # add = max((reverse_geocode_result[0]['formatted_address']),(reverse_geocode_result[1]['formatted_address']),(reverse_geocode_result[2]['formatted_address']))
        # add = reverse_geocode_result[0]['formatted_address']
        print(add)
        # print(reverse_geocode_result[1]['formatted_address'])
        # print(reverse_geocode_result[2]['formatted_address'])
        # a=0
        # b=0
        realtime =taglabel['DateTimeOriginal']
        # for i in taglabel['DateTimeOriginal']:
        #     a += 1
        #     if i == ':':
        #         year = taglabel['DateTimeOriginal'][0:a-1]
        #         tempdate = taglabel['DateTimeOriginal'][a:]
        #         a = 0
        #         break
        # for i in tempdate:
        #     a += 1
        #     if i == ' ':
        #         date = tempdate[0:a-1]
        #         for j in date:
        #             b+=1
        #             if j == ':':
        #                 date1 = date[0:b-1]
        #                 date2 = date[b:]
        #         b = 0
        #         time1 = tempdate[a:]
        #         for k in time1:
        #             b+=1
        #             if k == ':':
        #                 time2= time1[0:b-1]
        #                 time1= time1[b:]
        #                 break
        #         b=0
        #         for l in time1:
        #             b+=1
        #             if l == ':':
        #                 time3 = time1[0:b-1]
        #                 time4 = time1[b:]
        #                 break
        #         a = 0
        #         break
        # print(year)
        # print(date)
        # print(time1)
        # print(time2)
        # print(time3)
        # print(time4)
        # date = date1 +":"+date2
        # time1 = time2+":"+time3+":"+time4  
    except KeyError as e:
        add = 'no address'
        # year = 'no year'
        # date1 = 'no date'
        # date2= ''
        # time1 = 'no time'
        realtime = 'no time'
        print("GPS 정보가 없습니다.")
    except AttributeError as e:
        add = 'no address'
        # year = 'no year'
        # date1 = 'no date'
        # date2= ''
        # time1 = 'no time'
        realtime = 'no time'
        print("사진 세부 정보가 부족합니다.")
    
    """
    감정 인식

    """

    # img = cv2.imread('angry_sungju.jpg')
    # img = cv2.resize(img, dsize=(545,720), interpolation=cv2.INTER_AREA)

    # predictions = DeepFace.analyze(img)
    # # print(predictions)
    # print(predictions['dominant_emotion'])


    happy = [ '웃으면 행복이 온답니다!',
                '행복은 멀지 않은곳에..',
                '이 행복한 감정 잊지 말도록 해요',
                '행복이란 바이러스에 감염된것만 같아..',
                '나는 행복합니다~ 나는 행복합니다~', 
                '웃쨔 웃쨔 읏쨔~',
                '더도말고 덜도말고 오늘만 같아라~',
                '웃음은 강장제이고, 안정제이며, 진통제이다.', 
                '우린 웃을때 제일 이쁘답니다.',
                '모험 하지 않는자는 행운이 없다.',
                '음~ 맛있는 음~식도 빠지면  섭하지',
                '행복은 우리자신한테 달려있답니다.',
                '행복은 목적지로 향하는 여정!',
                '행복은 네가 경험하는것이 아닌 기억하는것.',
                '새로운 요리의 발견이 새로운 별의 발견보다 인간을 더 행복하게 만든다.',
                '위는 마음을 지배한다.',
                '입에 음식이 있는한 당분간 당신은 모든 문제를 해결했어요!',
                '보고 맛보고 느껴라!',
                '행복은 나누면 배가 된답니다!',
                '모자라는 부분을 채워나가봐요! 그것이 행복이랍니다.' ]
    angry = ['오늘은 무엇인가 나를 짜증나게 만들었다.',
                '화가 날땐 쉼호흡을 크게 해보자.',
                '노여움이 일면 그 결과를 생각하라.',
                '분노는 무모함으로 시작해 후회로 끝난다.',
                '무엇이 나를 화나게 만들었을까?',
                '오늘같이 화가나는 날엔 파전먹으러 가야지',
                '분노는 내 자신을 갉아먹을 뿐.',
                '화가 날땐 억지로라도 환하게 웃어보자.',
                '표정이 일그러졌는데 어떻게 해야할까?',
                '그만 두자 모든걸 그래야 화가 풀리니깐.']
    fear = ['두렵다. 그것은 무서움의 다른 말.',
            '공포는 어디서부터 오는 걸까?',
            '두려움은 자신을 모르기 때문에 생기는 감정.',
            '공포에는 한계가 없으니 두려움을 없애라.',
            '두려움은 사람이 소유한 감정 중 판단력을 가장 흐리게 한다.',
            '겁이 많아보이네, 겁이 많을수록 크게 짖는다더니.',
            '겁이나 난 겁이나 아버지! 날 보고있다면 정답을 알려줘.',
            '진짜 너 겁에 질려 떨고있는 거야??',
            '공포는 미신때문에 생긴대.',
            '두려움을 극복하는 방법은 맛있는 걸 먹으러 가면 돼!']
    sad = ['우울해', '되는 일이 없네', '너무 슬퍼', '서글프다', '눈물이 차올라', '눈물이 주르륵', '서러워', '답답하고 막막해', '마음이 아파', '짠하다', '엉엉 울고 싶어', 
            '우울한 일이 있으면 확 털어놓는 거야.', '넌 혼자서 속으로 꿍얼꿍얼하니까 해결이 안 되지.',
            '기분이 우울할 때는 음악을 들으라고!', 
            '나는 우울할 때면 옥상에서 햇볕을 쬐어봐요',
            '슬픔은 가장 좋은 친구입니다',
            '말로 슬픔을 덜 수는 없지요',
            '슬픔과 우울은 언제나 혼자 오지 않는다. 뒤에서 떼를 지어 몰려 오는 법이다.',
            '이상과 현실 사이에 생기는 거리감 즉 기대와 현실 사이에 갭이 우울증이다.',
            '우울한 기분을 조심하세요 기분이 우울하면 인생 또한 우울해 보이기 마련입니다',
            '이것 또한 지나가리라',
            '살다보면 누구나 힘들때가 있고 지칠 때가 있어요',
                    '너무 우울해', '슬픈 날', '서럽다 서러워']
    surprise = ['와우!', '놀라워!', '신기하다', '입이 떡 벌어진다', '너무 놀랐어', '완전 신기해', '와 대박', '쩔어!', '진짜 놀라워!', '깜짝 놀랐어!', '짱 신기해!', '실화야','꿈이야 생시야'
                    '친숙한 것에서 새로움을 익숙한 것에서 놀라움을',
                '우리의 뇌는 놀라움을 사랑한다']
    neutral= ['평온한 날들',
                '멍한건지 평화로운건지',
                '어쨌든 결말은 평화',
                '무표정 연기중',
                '오늘-평화=0',
                '평화는 행복의 극치',
                '행복할 때 나오는 무표정',
                '오늘도 무사히',
                '여긴어디 나는 누구',
                '무념무상']
    disgust = ['저질이야.',
                    '극혐. - 휴.',
                    '징그러워요...',
                    '와... 정말 징글징글하다.',
                    '살짝 토나온다.',
                    '너무 징그러워 보여!',
                    '아, 징그럽게 뭐 하는 거야.'
                    ,'그게 그렇게 역하지 않아요.'
                    ,'대박! - 정 떨어져.'
                    ,'징그러워 소름 돋아.',
                    '이건 너무 더러워. – 더러워!',
                    '기분이 너무 안 좋았어요.']
    
    
    
    
    img2 = cv2.imread(path + '/'+file)
    # img2 = cv2.resize(img2,dsize=(545,720), interpolation=cv2.INTER_AREA)
    # cv2.imshow('image1',img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    try:
        predictions1 = DeepFace.analyze(img2)
        #print(predictions1)
        feeling = predictions1['dominant_emotion']
        if feeling == 'happy':
            sen = random.choice(happy)
        elif feeling == 'angry':
            sen = random.choice(angry)
        elif feeling == 'fear':
            sen = random.choice(fear)
        elif feeling == 'sad':
            sen = random.choice(sad)
        elif feeling == 'surprise':
            sen = random.choice(surprise)
        elif feeling == 'neutral':
            sen = random.choice(neutral)
        elif feeling == 'disgust':
            sen = random.choice(disgust)
        else:
            sen = feeling    
        

        info_date.append([add,realtime,sen,file])
        

    except ValueError as e:
        info_date.append([add,realtime,"background",file])
        print("얼굴이 인식되지 않았습니다.")
    #print(predictions1)
    
    # img1 = cv2.imread('angry_boy.jpg')

    # predictions1 = DeepFace.analyze(img1)
    # print(predictions1)
    # print(predictions1['dominant_emotion'])

"""
날짜 순으로 나열
"""

for i in info_date:
    if i[1] == 'no time':
        i[1] = sys.maxsize
    else:
        i[1]= int(i[1][0:4] + i[1][5:7] + i[1][8:10] + i[1][11:13] + i[1][14:16] + i[1][17:])
        
info_date.sort(key=lambda x:x[1])

for i in info_date:
    if i[1] == sys.maxsize:
        i[1] = 'no time'
    else:
        i[1]= str(i[1])
        i[1]= i[1][0:4] + "년 " +i[1][4:6]+ "월 "  + i[1][6:8]+ "일 "  + i[1][8:10]+ "시 "   + i[1][10:12]+ "분 "  + i[1][12:]+ "초" 

info_date=tuple(info_date)
#print(type(info_date))  
print("\n\n\n최종 결과")
for x in info_date:
    print('{} 사진의 세부 정보 : '.format(x[-1]),end='')
    for i in x:
        print(i, end =', ')
    print('\n') 
print(time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
 
    


