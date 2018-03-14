# coding:utf-8
import urllib


def params_post_toStr(body=None):
    if  body:
        bodystr=''
        for key in body:
            value=body.get(key)
            bodystr=bodystr+str(key)+"="+str(value)+"&"
        return bodystr

def params_get_toStr(url=None, params=None):
    if  url and params:
        urlstr=url+'?'
        for key in params:
            value=params.get(key)
            value=urllib.quote(str(value))
            urlstr=urlstr+str(key)+"="+value+"&"
        return urlstr
if __name__=="__main__":
    body = {
        'page': '1',
        'rows': '100',
        'annNum': 1
    }
    print params_post_toStr(body)
    print params_get_toStr('url:',body)