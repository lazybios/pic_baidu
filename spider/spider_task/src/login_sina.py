# coding=utf-8

import urllib
import urllib2
import lxml.html as HTML
import cookielib


class Login_sina(object):
    # 定义公共变量
    url = 'http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='
    postdata = {
                'backTitle':"新浪微博",
                'backURL':'http%3A%2F%2Fweibo.cn%2F',
                'mobile':'',
                'submit':'登录', }
    headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; QQDownload 718; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3; Tablet PC 2.0)'}
    
    
    def __init__(self):
        # 绑定cookies
        self.cj = cookielib.LWPCookieJar()
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        
    def get_hidden_input(self):
        #获取登录表单中的隐藏值及随机值
        req = urllib2.Request(Login_sina.url , urllib.urlencode({}), Login_sina.headers)
        resp = urllib2.urlopen(req)
        login_page = resp.read()
        
        rand_action = HTML.fromstring(login_page).xpath("//form/@action")[0]
        passwd = HTML.fromstring(login_page).xpath("//input[@type='password']/@name")[0]
        vk = HTML.fromstring(login_page).xpath("//input[@name='vk']/@value")[0]
        
        return rand_action, passwd, vk
            
        
    def login(self, username, passwd):
        #根据指定帐号信息登录并获取cookies认证
        self.temp_url, passwd_name, self.vk = self.get_hidden_input()
        Login_sina.postdata[passwd_name] = passwd
        Login_sina.postdata['vk'] = self.vk
        Login_sina.postdata['mobile'] = username
        # post登录信息
        self.submit_url = 'http://login.sina.cn/prog/wapsite/sso/' + self.temp_url
        self.data = urllib.urlencode(Login_sina.postdata)
        req = urllib2.Request(self.submit_url, self.data, Login_sina.headers)
        resp = urllib2.urlopen(req)
        successful_page = resp.read()        
        # 登录成功跳转生产cookies信息
        jump_link = HTML.fromstring(successful_page).xpath("//a/@href")
        req = urllib2.Request(jump_link[0] ,urllib.urlencode({}), Login_sina.headers)
        resp = urllib2.urlopen(req)        
        if resp:
            print '登录成功！'        
        
        
    def crawl_web(self,target_url):
        #爬去指定连接，返回页面源代码
        req = urllib2.Request(target_url ,urllib.urlencode({}), Login_sina.headers)
        resp = urllib2.urlopen(req)
        return resp.read()        
            
            
        
        
        
