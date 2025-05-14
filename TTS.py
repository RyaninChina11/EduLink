import requests
import urllib.parse

API_KEY = ""
SECRET_KEY = ""

def run(tex,name):
    url = "https://tsn.baidu.com/text2audio"
    tex = urllib.parse.quote(tex)
    tex = urllib.parse.quote(tex)
    payload='tex='+tex+'&tok='+get_access_token()+'&cuid=AP7wREpuJfL7x8XUgiiI5gha93Dy1p5u&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=1&aue=3'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    with open(name+".mp3", "wb") as file:
        file.write(response.content)
        file.flush()
        file.close()
    
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

__all__ = ['run']