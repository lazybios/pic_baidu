# coding=utf-8
from extract import extract
import login_sina
import re

# 登录sian weibo
logined = login_sina.Login_sina()
logined.login('sina_username', '******')

target_url = ('http://weibo.cn/album/albummblog?DisplayMode=1&rl=11&fuid=2087836775', 
              'http://weibo.cn/album/15899026002087836775/?DisplayMode=1',)

pic_name = []
large_pic_url = []
# 返回带爬取页面源码
for url in target_url:
    content = extract('<div class="c">','<div class="pm">',logined.crawl_web(url))
    #获取分页总数
    pattern = re.compile(r'\d/(\d)页')
    match = pattern.search(content)
    #不匹配默认只有1页
    if match:        
        total = match.group(1);
        page_num = int(total)        
    else:
        page_num = 1
        
    for i in range(1,page_num+1):
        page_url = url + '&page=' + str(i)
        print page_url
        content = extract('<div class="c">','<div class="pm">',logined.crawl_web(page_url))
        #匹配图片文件名
        pattern = re.compile("<img src=\"(.*?)\" alt='(.*?)' class=\"c\"/>")
        match = pattern.findall(content)
        pic_name.append(match)
    

#拼凑出原图片url地址,写入down.bat脚本中

with open('down.bat','w') as down:
    for url_list in pic_name:
        for pic_url in url_list:
            #获取文件名 
            #反向查找‘/’，然后将其截断，再反向一遍 当然这种写法不太好，但为了省时间就这样了
            print pic_url[0]
            pic_name2 = pic_url[0][::-1][0:pic_url[0][::-1].find('/')][::-1]        
            temp_url = 'http://ww2.sinaimg.cn/large/'+ pic_name2
            down.write('wget -P ./download_pic %s \n' %temp_url)            
        
    down.write('pause')
    down.close()

print '爬取 @胸毛满街撩随便hao就这么骚 图片完成！生成  down.bat 文件'
print 'lazybios@126.com'
print 'campus.baidu.com'
        
        





