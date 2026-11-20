import time,re
from datetime import datetime
import threading
from urllib.parse import urlparse

from scraper.http_client import fetch_tree, is_allowed_by_robots
from scraper.url_resolve import IMG_STYLE, is_image_url, resolve_img_url

#IMG_STYLE = [ 'jpg' , 'png' , 'gif' , 'jpeg']   # scraper/url_resolve.py へ移動(webp追加)

# 旧: D_HIERARCHY =["//","///","////"] で XPath を階層ごとに繰り返していた。
# XPath の '//' は全階層を対象にするため、1回の評価で足りる。重複取得と time.sleep(1) を廃止した。


def _tree_of(url, tree=None):
    """tree が渡されていればそれを使い、無ければ取得する。(1ページの重複取得を避けるため)"""
    return tree if tree is not None else fetch_tree(url)


def img_web_surfaceList(url, tree=None):
    img_tags = []
    #D_hierarchy =["//","///","////","/////","//////","///////","////////"]
    tree = _tree_of(url, tree)


    domain = urlparse(url).hostname

    # imgタグのsrc属性を取得
    try :
        for i in  tree.xpath('//img/@src'):

            i = resolve_img_url(url, i)
            img_tags.append(i)
    except Exception as e :
        print(e) 


    img_tags = list(dict.fromkeys(img_tags))

    #print(img_tags)

    return img_tags



def img_webS_srcList(urls):
    img_tags = []
    for n,url in enumerate(urls):
        tree = fetch_tree(url)

        #print(n)
        # imgタグのsrc属性を取得
        try :
            for i in  tree.xpath('//img/@src'):
                
                i = resolve_img_url(url, i)
                img_tags.append(i)
        except Exception as e :
            print(e) 
        #continue
        try :
            for i in  tree.xpath('a/img/@src'):
                i = resolve_img_url(url, i)
                    
                img_tags.append(i)
        except Exception as e :print(e) 

        time.sleep(1)  # ページ間の待機(複数ページの連続取得用)
        
        
        # [削除] リンク先の画像取得ブロック。
        # '//a/@href' は文字列のリストなので j.xpath(...) は常に AttributeError となり、
        # 例外が握りつぶされて機能していなかった。リンク先の取得は deepHTML_img が担当する。

    img_tags = list(dict.fromkeys(img_tags))

    #print(img_tags)

    return img_tags


def deepHTML_img(url):

    img_tags = []
    #D_hierarchy =["//","///","////","/////","//////","///////","////////"]
    tree = fetch_tree(url)


    domain = urlparse(url).hostname
    try :
        a_tags = tree.xpath('//a/@href')
        for j in a_tags:
            # 連続取得: robots.txt を確認し、リンク先ごとに待機する
            j = resolve_img_url(url, j)
            if not is_allowed_by_robots(j):
                continue
            time.sleep(1)
            treeJ = fetch_tree(j)
            print(treeJ)
            for i in  treeJ.xpath('/img/@src'):
                i = resolve_img_url(url, i)
                img_tags.append(i)
    
    except Exception as e :print(e) 
    
    img_tags = list(dict.fromkeys(img_tags))
    print(" deepHTML_img end")
    return img_tags




def img_web_AHREFsrc(url, tree=None):
    img_tags = []
    a_tags = []
    #a_imgtags = []
    
    #D_hierarchy =["//"]

    tree = _tree_of(url, tree)

    
    domain = urlparse(url).hostname
    #print(domain)
    try:    
        for i in  tree.xpath('//a/@href'):
                #print(i)
                # j = f'https://{domain}{i}'
                
                # a_tags.append(j)
                #print(j)
                i = resolve_img_url(url, i)
                a_tags.append(i)
    except Exception as e :print(e)    
    #print(a_tags)

    # 拡張子フィルタは階層ループの外で1回だけ行う
    for i in a_tags:
        # クエリ付き(a.jpg?w=800)・大文字(a.JPG)も画像として判定する
        if is_image_url(i):
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


def web_P_imgsrc(url, tree=None):
    img_tags = []

    tree = _tree_of(url, tree)


    try :
        for i in  tree.xpath('//p/img/@src'):
            i = resolve_img_url(url, i)
            img_tags.append(i)
    except Exception as e :print(e) 
    
    print("p_img end")
    img_tags = list(dict.fromkeys(img_tags))

    return img_tags   


def detaSlider(url, tree=None):
    img_tags = []
    tree = _tree_of(url, tree)

    domain = urlparse(url).hostname
    try :
        for i in  tree.xpath('//img/@data-src'):

            img_tags.append(i)
    except Exception as e :print(e) 

    print("slide_img end")
    img_tags = list(dict.fromkeys(img_tags))

    return img_tags   

def img_web_Aimgsrc(url, tree=None):
    img_tags = []
    
    tree = _tree_of(url, tree)

    domain = urlparse(url).hostname
    try :
        for i in  tree.xpath('//a/img/@src'):
            # 旧: '/' 始まりの分岐で外側ループ変数 j を上書きし、img_tags に2件追加していた。
            # 変数 j は上書きせず、正しい絶対URLを1件だけ追加する。
            i = resolve_img_url(url, i)
            img_tags.append(i)
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
    # ページの取得とパースは1回だけ行い、各スクレイピング関数へ共有する(旧: 5スレッドが同じURLを5回取得していた)
    tree = fetch_tree(url)
    # スレッドで並列にスクレイピングを行う
    url_thread = threading.Thread(target=lambda: img_surfacelist.extend(img_web_surfaceList(url, tree)))
    image_thread = threading.Thread(target=lambda: a_href_imglist.extend(img_web_AHREFsrc(url, tree)))
    #deep_thread = threading.Thread(target=lambda: htmldeep.extend(deepHTML_img(url)))
    aIMG_thread = threading.Thread(target=lambda:a_img_srclist.extend(img_web_Aimgsrc(url, tree)))  # 旧: a_href_imglist に混入し a_img_srclist は常に空だった
    p_img_thread = threading.Thread(target=lambda:P_img_list.extend(web_P_imgsrc(url, tree)))
    d_Slider_thread = threading.Thread(target=lambda: slide_list.extend(detaSlider(url, tree)))


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
