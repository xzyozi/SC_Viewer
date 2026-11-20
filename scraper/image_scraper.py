import requests,time,re
from lxml import html
from datetime import datetime
import threading
from urllib.parse import urlparse

IMG_STYLE = [ 'jpg' , 'png' , 'gif' , 'jpeg']

D_HIERARCHY =["//","///","////"]


def img_web_surfaceList(url):
    img_tags = []
    #D_hierarchy =["//","///","////","/////","//////","///////","////////"]
    response = requests.get(url)
    html_doc = response.content

    tree = html.fromstring(html_doc)

    domain = urlparse(url).hostname

    for k in D_HIERARCHY:
    # imgタグのsrc属性を取得
        try :
            for i in  tree.xpath(f'{k}img/@src'):
                
                if i.find('//') == 0:
                    i = f'https:{i}'
                    #print(i)
                elif i.find('/')==0:
                    i = f'{url}{i}'
                elif i.find('http')==0:
                    pass
                else:
                    head_text =  url.rfind("/")
                    url_ed = url[:head_text]
                    i = f"{url_ed}/{i}"
                img_tags.append(i)
            time.sleep(1)
        except Exception as e :
            print(e) 
            
            pass


    img_tags = list(dict.fromkeys(img_tags))

    #print(img_tags)

    return img_tags



def img_webS_srcList(urls):
    img_tags = []
    D_hierarchy =["//","///","////","/////","//////"]
    for n,url in enumerate(urls):
        response = requests.get(url)
        html_doc = response.content

        #print(n)
        tree = html.fromstring(html_doc)
        #for k in D_hierarchy:
        # imgタグのsrc属性を取得
        try :
            for i in  tree.xpath('//img/@src'):
                
                if i.find('//') == 0:
                    i = f'https:{i}'
                    #print(i)
                elif i.find('/')==0:
                    i = f'{url}{i}'
                elif i.find('http')==0:
                    pass
                else:
                    head_text =  url.rfind("/")
                    url_ed = url[:head_text]
                    i = f"{url_ed}/{i}"
                img_tags.append(i)
            time.sleep(1)
        except Exception as e :
            print(e) 
        #continue
        try :
            for i in  tree.xpath('a/img/@src'):
                if i.find('//') == 0:
                    i = f'https:{i}'
                elif i.find('/')==0:
                    i = f'{url}{i}'
                elif i.find('http')==0:
                    pass
                else:
                    head_text =  url.rfind("/")
                    url_ed = url[:head_text]
                    i = f"{url_ed}/{i}"
                    
                img_tags.append(i)
            time.sleep(1)
        except Exception as e :print(e) 
        
        
        try :
            for k in D_hierarchy:
                a_tags = tree.xpath('//a/@href')
                for j in a_tags:
                    
                    
                    for i in  j.xpath('/img/@src'):
                        if i.find('//') == 0:
                            i = f'https:{i}'
                        elif i.find('/')==0:
                            i = f'{url}{i}'
                        elif i.find('http')==0:
                            pass
                        else:
                            head_text =  url.rfind("/")
                            url_ed = url[:head_text]
                            i = f"{url_ed}/{i}"
                        img_tags.append(i)
                        
                    time.sleep(1)
        
        except Exception as e :print(e) 

    img_tags = list(dict.fromkeys(img_tags))

    #print(img_tags)

    return img_tags


def deepHTML_img(url):

    img_tags = []
    #D_hierarchy =["//","///","////","/////","//////","///////","////////"]
    response = requests.get(url)
    html_doc = response.content

    tree = html.fromstring(html_doc)

    domain = urlparse(url).hostname
    try :
        for k in D_HIERARCHY:
            a_tags = tree.xpath(f'{k}a/@href')
            for j in a_tags:
                responseJ = requests.get(j)
                html_docJ = responseJ.content

                treeJ = html.fromstring(html_docJ)
                print(treeJ)
                for i in  treeJ.xpath('/img/@src'):
                    if i.find('//') == 0:
                        i = f'https:{i}'
                    elif i.find('/')==0:
                        i = f'{url}{i}'
                    elif i.find('http')==0:
                        pass
                    else:
                        head_text =  url.rfind("/")
                        url_ed = url[:head_text]
                        i = f"{url_ed}/{i}"
                    img_tags.append(i)
                    
            time.sleep(1)
    
    except Exception as e :print(e) 
    
    img_tags = list(dict.fromkeys(img_tags))
    print(" deepHTML_img end")
    return img_tags




def img_web_AHREFsrc(url):
    img_tags = []
    a_tags = []
    #a_imgtags = []
    
    D_hierarchy =["//","///","////","/////","//////"]
    
    #D_hierarchy =["//"]

    response = requests.get(url)
    html_doc = response.content

    tree = html.fromstring(html_doc)
    
    domain = urlparse(url).hostname
    #print(domain)
    for k in D_hierarchy:
        try:    
            for i in  tree.xpath(f'{k}a/@href'):
                    if i.find('//') == 0:
                        i = f'https:{i}'
                    elif i.find('/')==0:
                        #print(i)
                        # j = f'https://{domain}{i}'
                        
                        # a_tags.append(j)
                        #print(j)
                        i = f'{url}{i}'
                        #print(j)
                        
                    elif i.find('http')==0:
                        pass
                    else:
                        head_text =  url.rfind("/")
                        url_ed = url[:head_text]
                        i = f"{url_ed}/{i}"
                    a_tags.append(i)
        except Exception as e :print(e)    
        #print(a_tags)


        for i in a_tags:
            for k in IMG_STYLE:
                nam = i.rfind(k)

                if nam == len(i)-3 or nam == len(i)-4:
                    img_tags.append(i)

        
           
        # for j in a_imgtags:
        #     try:
        #         responseJ = requests.get(j)
        #         html_docJ = responseJ.content

        #         treeJ = html.fromstring(html_docJ)
        #         #print(treeJ)
        #         for i in  treeJ.xpath('//img/@src'):
        #             print(i)
        #             if i.find('//') == 0:
        #                 i = f'https:{i}'
        #             elif i.find('/')==0:
        #                 i = f'{url}{i}'
        #             elif i.find('http')==0:
        #                 pass
        #             else:
        #                 head_text =  url.rfind("/")
        #                 url_ed = url[:head_text]
        #                 i = f"{url_ed}/{i}"
        #                 img_tags.append(i)
        #         #print(img_tags)    
        #         #time.sleep(1)
    
        #     except Exception as e :
        #         print(e)
        #         pass
    print("ahref end")
    img_tags = list(dict.fromkeys(img_tags))

    return img_tags


def web_P_imgsrc(url):
    img_tags = []

    response = requests.get(url)
    html_doc = response.content

    tree = html.fromstring(html_doc)        

    for j in D_HIERARCHY:  
        try :
            for i in  tree.xpath(f'{j}p/img/@src'):
                if i.find('//') == 0:
                    i = f'https:{i}'
                elif i.find('/')==0:
                    i = f'{url}{i}'
                elif i.find('http')==0:
                    pass
                else:
                    head_text =  url.rfind("/")
                    url_ed = url[:head_text]
                    i = f"{url_ed}/{i}"
                img_tags.append(i)
            time.sleep(1)
        except Exception as e :print(e) 
    
    print("p_img end")
    img_tags = list(dict.fromkeys(img_tags))

    return img_tags   


def detaSlider(url):
    img_tags = []
    response = requests.get(url)
    html_doc = response.content

    tree = html.fromstring(html_doc)        
    domain = urlparse(url).hostname
    for j in D_HIERARCHY:
        try :
            for i in  tree.xpath(f'{j}img/@data-src'):

                img_tags.append(i)
            time.sleep(1)
        except Exception as e :print(e) 

    print("slide_img end")
    img_tags = list(dict.fromkeys(img_tags))

    return img_tags   

def img_web_Aimgsrc(url):
    img_tags = []
    
    response = requests.get(url)
    html_doc = response.content

    tree = html.fromstring(html_doc)        
    domain = urlparse(url).hostname
    for j in D_HIERARCHY:  
        try :
            for i in  tree.xpath(f'{j}a/img/@src'):
                if i.find('//') == 0:
                    i = f'https:{i}'
                elif i.find('/')==0:
                    j = f'https://{domain}{i}'
                        
                    img_tags.append(j)
                    
                    i = f'{url}{i}'
                
                elif i.find('http')==0:
                    pass
                else:
                    head_text =  url.rfind("/")
                    url_ed = url[:head_text]
                    i = f"{url_ed}/{i}"
                img_tags.append(i)
            time.sleep(1)
        except Exception as e :print(e) 
    
    print("a_img end")
    img_tags = list(dict.fromkeys(img_tags))

    return img_tags   



def SurDeep_imgthread(url):
    results = []
    img_surfacelist = []
    a_href_imglist = []
    htmldeep =[]
    a_img_srclist = []
    P_img_list = []
    slide_list = []
    # スレッドで並列にスクレイピングを行う
    url_thread = threading.Thread(target=lambda: img_surfacelist.extend(img_web_surfaceList(url)))
    image_thread = threading.Thread(target=lambda: a_href_imglist.extend(img_web_AHREFsrc(url)))
    #deep_thread = threading.Thread(target=lambda: htmldeep.extend(deepHTML_img(url)))
    aIMG_thread = threading.Thread(target=lambda:a_href_imglist.extend(img_web_Aimgsrc(url)))
    p_img_thread = threading.Thread(target=lambda:P_img_list.extend(web_P_imgsrc(url)))
    d_Slider_thread = threading.Thread(target=lambda: slide_list.extend(detaSlider(url)))


    url_thread.start()
    image_thread.start()
    #deep_thread.start()
    aIMG_thread.start()
    p_img_thread.start()
    d_Slider_thread.start()
    
    url_thread.join()
    image_thread.join()
    #deep_thread.join()
    aIMG_thread.join()
    p_img_thread.join()
    d_Slider_thread.join()
    # スレッドから返されたリストをまとめて、結果リストに追加する
    results = img_surfacelist + a_href_imglist + a_img_srclist + P_img_list + slide_list #+ htmldeep 
    results = list(dict.fromkeys(results))
    print(results)
    #print(type(results))
    return results




if __name__ == "__main__":
    # urls = ["https://customprinthaus.com/search?options%5Bprefix%5D=last&page=1&q=CLAUDE+MONET&type=product%2Carticle","	https://customprinthaus.com/search?options%5Bprefix%5D=last&page=2&q=CLAUDE+MONET&type=product%2Carticle","	https://customprinthaus.com/search?options%5Bprefix%5D=last&page=3&q=CLAUDE+MONET&type=product%2Carticle"]
    #url = "http://intervaluesa.com/n/nanoka16.html"
    
    #url = "https://bestgirlsexy.com/flash-photobook-2023-01-31-miyu-murashima-村島未悠-good-girl-switch/"
    url = "https://www.gravurefit.com/picture/person-nagisa-konomi/"

    #url  = "https://bestgirlsexy.com/korean/"
    #url = 'https://media.thisisgallery.com/20185441' 
    t1 = datetime.now()
    #box = img_web_srcList(url)
    #boz = img_web_AHREFsrc(url)
    
    biz = SurDeep_imgthread(url)
    t2 = datetime.now()
    
    #print(box)
    
    #print(boz)
    print(biz)
    
    print(t2-t1)
    print(len(biz))
    # response = requests.get(url)
    # xxx = response.content
    # tree =     xxx.cssselect('img').get("src")
    # print(tree)


    # from urllib.parse import urljoin
    # print(1)
    
    # response = requests.get(url)
    # print(response)
    # tree = html.fromstring(response.content)
    # print(tree)
    # img_tags = tree.xpath('//img[@class="aligncenter size-full wp-image-2136"]')

    # for img in img_tags:
    #     img_url = img.get('src')
    #     abs_img_url = urljoin(url, img_url)
    #     print(abs_img_url)


    # # ページを取得
    # response = requests.get(url)
    # page_content = response.content

    # # HTMLをパース
    # tree = html.fromstring(page_content)

    # # aタグのhrefを取得
    # links = tree.xpath('//a/@href')

    # # 各リンク先のHTMLページの中から、imgタグのsrc属性から画像URLを取得
    # for link in links:
    #     # リンク先のページを取得
    #     response = requests.get(link)
    #     page_content = response.content

    #     # HTMLをパース
    #     tree = html.fromstring(page_content)

    #     # imgタグのsrc属性から画像URLを取得
    #     img_urls = tree.xpath('//img/@src')

    #     # 画像URLを表示
    #     for img_url in img_urls:
    #         print(img_url)
