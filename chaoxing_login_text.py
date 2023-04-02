import requests,lxml
from bs4 import BeautifulSoup as BS
import time

url = "https://passport2.chaoxing.com/"



#获取登录界面的源码
def requests_index():
    
    login_index_url = url + r"login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com"

    #请求头
    headers = {'Host':'passport2.chaoxing.com','Referer':'https://i.chaoxing.com/','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'}
    html = requests.get(login_index_url,headers=headers)
    soup = BS(html.text,"lxml")

    #解析uuid 与 enc 的值
    uuid = soup.select("#uuid")[0].get("value")
    enc = soup.select("#enc")[0].get("value")

    #返回值
    return uuid,enc

#保存登录二维码
def open_code(uuid):
    #请求头
    headers = {'sec-ch-ua-platform':'Linux','Sec-Fetch-Dest':'image','Host':'passport2.chaoxing.com','Referer':'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https://i.chaoxing.com','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'}
    code_url = url + "createqr?uuid=" + uuid + "&fid=-1"
    code_data = requests.get(code_url,headers=headers)

    #二维码图片的名称
    code_image_name = "code.png"
    #print((bytes(code_data.text,encoding='utf-8').decode('utf-8')))
    #print(code_url)
    #保存
    with open(code_image_name,"wb") as f:
        #使用流保存
        f.write(code_data.content)
        print("二维码文件已保存")
    
    

#轮查二维码状态
def query_login_status(uuid,enc):
    query_code_url = "https://passport2.chaoxing.com/getauthstatus"
    false = False
    true = True

    #post请求提交的数据
    data = {"uuid":uuid,"enc":enc}

    #请求头
    headers = {'Origin':'https://passport2.chaoxing.com','Content-Type':'application/x-www-form-urlencoded;charset=UTF-8','sec-ch-ua-platform':'Linux','Sec-Fetch-Dest':'empty','Host':'passport2.chaoxing.com','Referer':'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https://i.chaoxing.com','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'}
    #print(data)
    print("请打开 code.png 扫码登录")

    #轮查
    while True:
        return_data = requests.post(query_code_url,data=data,headers=headers)
        data_dict = eval(return_data.text)

        #如果在手机上点击了登录
        if (data_dict['status'] == true):
            #print(return_data.text)

            #获取请求头的set-cookie
            Set_Cookie = return_data.raw.headers.getlist('Set-Cookie')
            break

        #延迟
        time.sleep(1)
    return Set_Cookie
    '''
    return_data = requests.post(query_code_url,data=data)
    print(return_data.headers)
    '''

            
    print(">>>>>>>>>>")

#处理返回的set-cookie
def dispose_cookie(cookie_data):
    cookie_str = ''
    for cookie_list_1 in cookie_data:
        #print(type(cookie))
        #print(cookie)
        cookie_list_2 = cookie_list_1.split(';')
        cookie_str = cookie_str + cookie_list_2[0] + ';'
    return cookie_str



#获取uuid 与 enc
uuid,enc = requests_index()

#保存二维码
open_code(uuid)

#获取set-cookie
Set_Cookie = query_login_status(uuid, enc)

#处理set-cookie
cookie = dispose_cookie(Set_Cookie)






    
