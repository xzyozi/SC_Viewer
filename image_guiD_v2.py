import requests, sys, os
import csv
import PySimpleGUI as sg
from PIL import Image , ImageTk
from io import BytesIO
#from lxml import html
import webbrowser
import pandas as pd
# -- my py --------------------------------
from search_img_Thread3 import img_webS_srcList ,SurDeep_imgthread 


url = 'https://media.thisisgallery.com/20185441'  
#url ='https://bijutsufan.com/paintings/paintings-name/list-artist-name/'
# url = 'https://www.pysimplegui.org/en/latest/#menu-definition'

# +-----------------------------------------------------------------------------------+
# + ブラウザー指定   chrome
# +-----------------------------------------------------------------------------------+

browser = webbrowser.get('"C:\Program Files\Google\Chrome\Application\chrome.exe" %s &')

# +-----------------------------------------------------------------------------------+
# + csv読み込み
# +-----------------------------------------------------------------------------------+

csv_pass = 'save/df_saveURL_V2.csv'

#csv_pass = 'save/image_saveURL.csv'
#csv_pass = 'save/ex_saveURL.csv'

#+直下にフォルダー作成
os.makedirs(name='./save',exist_ok=True)

try:
    with open(csv_pass, 'r',encoding="utf-8") as f:
        reader = csv.reader(f)

        listBox = [box for box in reader]

except:

    #df = pd.DataFrame(columns=('title','url'))
    df = pd.DataFrame(
        data = {'title':['sample'] ,
                'url': [url],
                'error_image':['0a1a20a116a118a120a121a123a125a126a127a130a134a136a138a140a142a144a145a151a153a156a158a160a161a167a169a170a173a179a181a183a185a186a187a189a194a196a200a202a203a204a206a208a209a211a213a214a216a218a219a222a225a228a230a232a233a236a240a242a245a249a251a254a256a258a260a261a262a263a313a314a315a316a317a318a319a320a321a322a323a324a325a326a327a328a329a330a331a332a333a334a335a336a337a338a339a340a341a342a343a344a345a346'],
                'image_range':[346]
    },index=[0])
    df.to_csv(csv_pass,encoding="shift_jis",index=False)

    with open(csv_pass, 'r',encoding="utf-8") as f:
        reader = csv.reader(f)

        listBox = [box for box in reader]   
#print(listBox)

#listBox_nameCol = [line[0] for line in listBox]
listBox_nameCol  = [line[0] for n,line in enumerate(listBox) if n>0]
listBox_urlCol = [line[1] for n,line in enumerate(listBox) if n>0]
listBox_errorCol = [line[2] for n,line in enumerate(listBox) if n>0]
listBox_rangeCol = [line[3] for n,line in enumerate(listBox) if n>0]


#print(len(listBox_nameCol))
# len_lixtBox = len(listBox)

# print(listBox[len_lixtBox-1][0])
# col_names = [i for i in range(1,2)]
# df = pd.read_csv(csv_pass,index_col=0,names=col_names)
# print(df)


# +-----------------------------------------------------------------------------------+
# + csv読み込み part2
# +-----------------------------------------------------------------------------------+

with open('sc/artist_url_4.csv', 'r',encoding="utf-8") as f:
    reader = csv.reader(f)
    #for line in reader:
        #print(line)
        #print(line[0])
        
    box = [line for line in reader]

#print(box)
box_col0 = [line[0] for line in box]


# +-----------------------------------------------------------------------------------+
# + スタイル設定
# +-----------------------------------------------------------------------------------+
# + テーマ + 
sg.theme('DarkTeal6')
#sg.theme('HotDogStand')
#sg.theme('Topanga')
#sg.theme('PythonPlus')

GUI_THEME = ['PythonPlus','Topanga','HotDogStand','DarkTeal6']

# + フォント + 
#guiFont = "@Terminal"
guiFont = "Impact"
#guiFont = "Candara"
#guiFont = "Symbol"
#guiFont = "Lucida Handwriting"



# +-----------------------------------------------------------------------------------+
# + listで選んだ項目　→　url_list
# +-----------------------------------------------------------------------------------+

def url_change(artist_name):
    for nam,i in enumerate(box_col0):
        if i == artist_name :
            #print("found")
            url_list = [box[nam][1]]
            
            if bool(box[nam][2]) == True:   #  box[nam][2] != ''
                url_list.append(box[nam][2])
                #print("found")
            if bool(box[nam][3]) == True :
                url_list.append(box[nam][3])
            if bool(box[nam][4]) == True :
                url_list.append(box[nam][4])
            #print(url_list)
    return url_list


# +-----------------------------------------------------------------------------------+
# + pysimplegui のレイアウト
# +-----------------------------------------------------------------------------------+


right_click_menu_jp = ['&Right',['コピー', '貼り付け'] ]
right_click_menu_jp_copy = ['&Right',['コピー'] ]

buttonInButton = [[sg.Button('RETURN')],
                  [sg.Text('終了します')]]

MENU_df = [
    ['&setting', ['style',[GUI_THEME]]],

]
                    




def window_made():
    Frame_1 = sg.Frame("LIST control",[[sg.Button("Save",key='-save-',font=(guiFont,11)),sg.Button("put URL",key='-put-',font=(guiFont,11))],
                                       [sg.T(font=(4))],
                                       [sg.B("List Delete",key='-del-',size=(13,0),font=((guiFont,11)))]],
                       font=(guiFont,11) )
    
    
    main_button_col = [[sg.Button("Open",size=(6,1),key='-open search-',font=(guiFont,11)),sg.Button("Clear",size=(6,1),font=(guiFont,11))],
            [sg.T("")],
            [Frame_1],
            ]
    
    tab2_layout = [  
            [sg.Listbox(box_col0,size=(49,20),key='-LIST-')],
            [sg.Button("Open",key='-open list-',size=(5,1),font=(guiFont,11))]
            ]
    
    open_layout = [
        [sg.InputText(default_text=url,key='-Input-' ,right_click_menu=right_click_menu_jp ,size=(51,10)) ],
            [sg.Column(main_button_col,vertical_alignment='top'),sg.Listbox(listBox_nameCol,size=(28,20),key='-listbox-')]
    ]
    
    tab_group_layout = [
    [sg.TabGroup([
        [sg.Tab('Search Image', open_layout)],
        [sg.Tab('Artist List', tab2_layout)]
    ],focus_color='yellow')],
    [sg.Button("Exit",size=(8,1),font=(guiFont,11),pad=((15,0),(0,0)))]]
    
    main_layout = [[sg.Menu(MENU_df,tearoff=False,key='-menu-')],
        [sg.Column(tab_group_layout)]]
    
    return sg.Window("メインウィンドウ", main_layout, finalize=True)



def window_viewer_made():
    
    button_col = [[sg.Button('Start & SpeedDown',size=(15,2),font=(guiFont,11))],
                [sg.Button('Back SCROLL & SpeedDown',key='-backscroll-',size=(15,2),font=(guiFont,11))],
                [sg.T()],
                [sg.Button('STOP',size=(6,None),font=(guiFont,11))],
                [sg.Text()],
                [sg.Button('BACK',size=(6,1),font=(guiFont,11)),sg.Button('NEXT',size=(6,1),font=(guiFont,11))],
                [sg.Text()],
                [],
                [sg.Text()],
                [sg.Button('RETURN',font=(guiFont,11))],
                [sg.T()],
                [sg.B("",font=(guiFont,20),key='-counttext-',pad=((20,0),(100,0)))]
                ]
    
    viewer_layout = [[sg.Column(button_col,vertical_alignment='top'),sg.Image(key='-IMAGE-')],
          [sg.Button("Web",key='-web-',font=(guiFont,11)),sg.InputText(key='-TEXT-',right_click_menu=right_click_menu_jp_copy,size=(120,10) )]]
    
    return sg.Window('Image Viewer', viewer_layout, resizable=True, finalize=False,location=(150,8))



#############################################################################
#MM@^      ?WMMM%!!!!!!!!!!!?MMM!!!!!!!!!!MMMMMF!!!!!!!!?"WMMMM>!!!!!!!!!!!?#
#`          ,MM}            MM#          MMMMMF            TMM~           . #
#!     ..     JM}            MMF          dMMMMF     ..      dM~           .#
#     JMM]    .MMMM#     dMMMMM]    .)    (MMMMF     MMN.    ,MMMM#     MMMM#
#     dMM]    .MMMM#     dMMMMM%    (]    .MMMMF     MMM{    ,MMMM#     MMMM#
#     dMM]  ` .MMMM#     dMMMMM!    dF    .MMMMF     MMM{    ,MMMM#     MMMM#
#   ` JMM]    ,MMMM#     dMMMMM     MN     MMMMF     MMM{    ,MMMM#     MMMM#
#.     TMMMMMMMMMMM#     dMMMM#     MN     MMMMF     MMM`    (MMMM#     MMMM#
#b       (TMMMMMMMM#     dMMMMF    .MM     dMMMF     ""'    .MMMMM#     MMMM#
#MN.        ?MMMMMM#     dMMMMF    .MM_    (MMMF         ..MMMMMMM#     MMMM#
#MMMNa,      .MMMMM#     dMMMM%    .MM|    .MMMF           (WMMMMM#     MMMM#
#MMMMMMNa     (MMMM#     dMMMM{    .??`    .MMMF    .MMM     MMMMM#     MMMM#
#     MMM|    .MMMM#     dMMMM`             MMMF    .MMM     dMMMM#     MMMM#
#     MMM[    .MMMM#     dMMM#              MMMF    .MMM     JMMMM#     MMMM#
#     MMM[   `.MMMM#     dMMM#     MMMN     dMMF    .MMM     JMMMM#     MMMM#
#     MMM\    .MMMM#     dMMMF    .MMMM.    JMMF    .MMM     JMMMM#     MMMM#
#.    ."=     .MMMM#     dMMM]    .MMMM-    -MMF    .MMM     JMMMM#     MMMM#
#h.          .MMMMM#     dMMM}    .MMMM[    .MMF    .MMM     JMMMM#     MMMM#
#MN&,     ..+MMMMMMN.....dMMM-....JMMMMb.....MMb.....MMMp....,MMMM#.....MMMM#
#############################################################################



#window = sg.Window("メインウィンドウ", main_layout, finalize=True)
window = window_made()

while True:
    
    img_tags = []
    #window = sg.Window("メインウィンドウ", main_layout, finalize=True)
    event, values = window.read()
    #window['-listbox-'].update(listBox)
    print(f"event:{event}--values:{values}")


    if event == sg.WIN_CLOSED or event == "Exit":
        #sys.exit()
        break
    if event == "Clear":
        window['-Input-'].update("")
        continue
    
    elif event in ("コピー"):
            # try - except で弾かれたとき用に、バックアップの値を用意しておく
            # backup = window["-Input-"].Widget.clipboard_get()
            # window["-Input-"].Widget.clipboard_clear()
            try:
                selected_text = window["-Input-"].Widget.selection_get()
                window["-Input-"].Widget.clipboard_append(selected_text)
            except:
                #window["-Input-"].Widget.clipboard_append(backup)
                pass


    elif event in ("貼り付け"):
            try:
                clipboard_text = window["-Input-"].Widget.clipboard_get()
                insert_pos = window["-Input-"].Widget.index("insert")
                window["-Input-"].Widget.insert(insert_pos, clipboard_text)
            except:
                pass



    elif event in GUI_THEME:
        sg.theme(event)
        window.close()
        window = window_made()
        continue

    # elif event == 'style':
    #     sg.theme(values['GUI_THEME'])
    #     window = window.create_new_window(window)



    if event == '-save-':
        r = sg.PopupGetText("保存する名前を入力してください",grab_anywhere=True) #no_titlebar=True
        
        save_url = window["-Input-"].get()
        save_url = str(save_url)
        
        if r in listBox_nameCol:
            sg.Popup("同じ名前はつけられません。違う名前をつけてください。",auto_close=True)
            r = None
            continue
        
        if save_url in listBox_urlCol:
            sg.Popup("LIST内に同じURLが存在します。既存のLISTを削除してください",auto_close=True)
            r = None
            continue
        
        #print(r)
        
        #window['-listbox-'].update(listBox_nameCol)
    
    if event == '-put-' :
        listName = window['-listbox-'].get()
        #print(listName)
        #print(type(listName))
        try :
            listNameStr = listName[0]
            #print(listNameStr)
            for nam,i in enumerate(listBox_nameCol):
                if i == listNameStr :
            #print("found")
                    url_list = listBox[nam+1][1]
        
            window['-Input-'].update(url_list)
            
        except IndexError : 
            sg.Popup("LIST内から項目を選んでください。",auto_close=True)
            continue
        except Exception as e:print(e)
    
    
    if event == '-del-' :
        listName = window['-listbox-'].get()
        if listName == [] :
            sg.Popup("LIST内から項目を選んでください。",auto_close=True)
            continue
        else :
            # print(listBox)
            # print(len(listBox))
            if len(listBox) <= 2 :
                sg.Popup("LIST内の要素を’1以下’に出来ません",auto_close=True)
                continue
            g = sg.popup_yes_no('本当に消しますか？') 
        
        
    # Openボタンが押された場合
    if event == ("-open search-"):
        try :
            url = window['-Input-']
            #print(type(url))
            url = url.get()
            url = str(url)
            
            #+--------------
            #+ スクレイピング
            #+--------------
            img_tags = SurDeep_imgthread(url)
        except Exception as e: 
            sg.popup(f"{e}のエラーがおきました")
            continue
        
        if img_tags == []:
            sg.popup("画像Urlを取得する出来ませんでした",auto_close= True)
            continue


    if event == "-open list-":
        try :
            artist_name = values['-LIST-']
            artist_name =  artist_name[0]
            #print(type(artist_name))
            #print(artist_name)
            
            url = url_change(artist_name)  
            #print(url)
            #print(type(url))
            img_tags = img_webS_srcList(url)

        except Exception as e: 
            print(e)
            sg.Popup('ERROR',auto_close=True)
            continue
        # メインウィンドウを閉じて、サブウィンドウを作成して表示する
        
        if img_tags == []:
            sg.popup("画像Urlを取得する出来ませんでした",auto_close= True)
            continue        
   
    if bool(img_tags) == True:    
        
        #save用の判別用
        input_url = window["-Input-"].get()
        input_url = str(input_url)
        

        save_url = window["-Input-"].get()
        save_url = str(save_url)

        # メインウィンドウを閉じて、サブウィンドウを作成して表示する
        window.close()

        window = window_viewer_made() 
        
        image_elem = window['-IMAGE-']
        text_elem = window['-TEXT-']
    
            
        #変数定義
        timeout = 1000                  #画面移行する時間　defoult 1000ms = 1秒
        loop = True                     #whileのループを変える
        range_tags = len(img_tags) -1   #スクレイピングした画像の数
        count = 0                       #画像の番号（順番）
        error_img = []                  #errorが起こった画像の番号を格納
        #error_nam = 0                  
        back_scroll = False             #countの進む方向　True = マイナス値  False = プラス値
        #error_nam_back = 0
        #skip_count = 0
        skip90 = (range_tags*0.9)       #スクレイピングした画像の数の90％
        zero_through = True             #count == 0 をスルーするかどうか  True = スルー　　False = スルーしない
        #print(range_tags)
        stop_image = False              #timeout == None かどうか
        end_count_through = True        #backscroll時の count == range_count をスルーするかどうか True = スルー false = スルーしない
        countCount = []                 #countの数える　
        countFULL = [i for i in range(range_tags)] 
        
        


        for nam,i in enumerate(listBox_urlCol):
            if i == input_url :
                # print(listBox[nam+1][3])
                # print(type(listBox[nam+1][3]))
                try:
                    if int(listBox[nam+1][3]) == range_tags:
                        print("error_tagを読み込みました")
                        errorBOX = listBox[nam+1][2]
            
            
                        box_li = errorBOX.split("a")
                        
                        for i in box_li:
                            i_int =int(i)
                            
                            error_img.append(i_int)
                            
                except Exception as e:
                    print(e)        
                         
        #print(range_tags +1)
        
        #+--------------------
        #+ while Start
        #+--------------------
        
        while loop :
            #for img_url in img_tags:
                #print(img_url)
           
            # if count == 0:
            #     zero_through = True
            # else:
            #     zero_through = False

            #print(count)
            
            if count not in countCount:
                countCount.append(count)


            error_img_code = False
            
            event, values = window.read(timeout=timeout)
            
            
            #読み込めなかった画像をスキップ
            try:
                
                if count in error_img:
                    
                    print("error_imgのためskipしました。")
                    error_img_code = True
                        
            except:pass
            
            #print(error_img)
            
            if error_img_code == True :
                
                if event == sg.WIN_CLOSED or window is None:
                    break
                
                if event == 'RETURN':
                    window.close()
                    #loop = False
                    #window = sg.Window("メインウィンドウ", main_layout, finalize=True)
                    print("return")
                    window = window_made()
                    break
                
                if back_scroll == False:
                    
                    timeout = 10
                    
                    #print(skip_count)
                    
                    if len(error_img)-1 >= skip90 :
                        window.close()
                        print("error画像が多いのでreturnします")
                        window = window_made()
                        break
                    
                    
                    if count == range_tags:
                        count = 0
                    
                    else:
                        count += 1
                    continue
                
                elif back_scroll == True:
                    
                    if zero_through == True :
                        if count == 0:
                            count = range_tags
                    
                        else : 
                            count -= 1
                    
                    timeout = 10
                    
                    

                    if len(error_img)-1 >= skip90 :
                        window.close()
                        print("return")
                        window = window_made()
                        break
                    
                    
                    continue
            
                       
            #print(timeout)
            
            #if count == 0 :
                #timeout = 1000
            
            if event == sg.WIN_CLOSED or window is None:
                #print("break top")
                break
            
            elif event in ("コピー"):
            # try - except で弾かれたとき用に、バックアップの値を用意しておく
                #backup = window["-TEXT-"].Widget.clipboard_get()
                #window["-TEXT-"].Widget.clipboard_clear()
                try:
                    
                    selected_text = str(window["-TEXT-"].Widget.selection_get())
                    #selected_text = window["-TEXT-"].Widget.selection_get(selection='SELECTION_CLIPBOARD')
                    window["-TEXT-"].Widget.clipboard_append(selected_text)
                except:
                    #window["-TEXT-"].Widget.clipboard_append(backup)
                    pass
                continue
            
            
            if event =='STOP':
                timeout = None
                print("画像を止めました")
                stop_image = True
                continue
            
            
            #img control
            if event =='NEXT':
                timeout = None
                count += 1
                stop_image = True
                back_scroll = False
                if count >= range_tags:
                    count = 0
            

            if event =='BACK':
                timeout = None
                count -= 1
                back_scroll = True
                stop_image = True
                if count == -1:
                    count = range_tags 
            
            
                
            if event == 'Start & SpeedDown':
                
                if timeout == None :
                    timeout = 500
                
                if back_scroll == True:
                    timeout = 500
                
                back_scroll = False
                
                timeout += 500
                print(f"{round(timeout/1000,1)}秒で動きます")
                stop_image = False
                continue
            
            if event == '-backscroll-' :
                
                if timeout == None :
                    timeout = 500
                
                if back_scroll == False:
                    timeout = 500
                back_scroll = True
                
                timeout += 500
                print(f'{round(timeout/1000,1)}秒でバックスクロールします')
                stop_image = False
                continue
            
            if event == 'RETURN':
                window.close()
                #loop = False
                #window = sg.Window("メインウィンドウ", main_layout, finalize=True)
                print("return")
                window = window_made()
                break
            
            
            if event == '-web-':
                
                web_url = window['-TEXT-']
                web_url = web_url.get()
                web_url = str(web_url)
                
                WEB_re = browser.open(f'{web_url}')
                #print(WEB_re)
                if WEB_re == False:
                    webbrowser.open(web_url)
                timeout = None
                stop_image = False
                continue
            
            
            
            if event == '-counttext-':
                re = sg.PopupGetText("ジャンプする番号を\n入力してください。",size=(20,10))
                if bool(re) == False :
                    continue
                try:
                    re = int(re)
                except Exception as e :
                    print(e)
                    continue
                if re >= range_tags :
                    continue
                else : count = re -1

            

            # +-----------------------------------------------------------------------------------+
            # + 描画処理
            # +-----------------------------------------------------------------------------------+
            #print(count)
            if count <= range_tags :    
                img_url = img_tags[count]
            
            
            #response = requests.get(img_url)
            #img_bio = BytesIO(response.content)
            #img = Image.open(img_bio)

                #画像表示の処理
                try:
                    response = requests.get(img_url)
                    img = Image.open(BytesIO(response.content))
                    #print("読み込めました")
                    
                    # アスペクト比の計算
                    width, height = img.size
                    aspect_ratio = height / width
                    
                    if width <= 150:
                        print('small image ',end="")
                        raise
                    elif aspect_ratio <= 0.277 or aspect_ratio >= 3.62:
                        print("aspect ",end="")
                        raise
                    else:   
                        # リサイズ
                        if height <= 300 :
                            new_height = 300
                            new_width = int(new_height / aspect_ratio)
                        
                        elif height <= 400 :
                            new_height = 400
                            new_width = int(new_height/ aspect_ratio)
                        
                        elif aspect_ratio >= 0.909 or aspect_ratio <= 1.1 :
                            new_height = 650
                            new_width = int(new_height / aspect_ratio)
                        
                        elif width > height:
                            new_width = 770
                            new_height = int(new_width * aspect_ratio)
                        elif width < height:
                            new_height = 700
                            new_width = int(new_height / aspect_ratio)


                        resized_img = img.resize((new_width, new_height))
                        text_elem.update(img_url)
                        bio = BytesIO()
                        resized_img.save(bio, format='png')
                        image_elem.update(data=bio.getvalue())
                    
                    
                    if stop_image == True :
                        timeout = None
                    
                    if timeout == 10 :
                        timeout = 1000
        
                        #window.refresh()
                        
                except Exception as e:
                    print(e)
                
                #error_nam_back += 1
                    if count not in error_img:
                        #描画出来なかった画像をlist("error_img")に保存
                        error_img.append(count)
                        #print("Error")

            # +-----------------------------------------------------------------------------------+
            # + 自動的にセーブ
            # +-----------------------------------------------------------------------------------+
            
            
            # if count not in countCount:
            #     countCount.append(count)
            
            print(error_img)
            #countALL = countCount + error_img
            
            #print(f"countALL : {countALL}")
            

            #print(f"countCount : {countCount}")
            if countCount == countFULL:
                    
                if (save_url not in listBox_nameCol) and (input_url not in listBox_urlCol) :   
                    #文字列　save_url
                    LENsave_url = len(save_url)

                    if save_url.rfind('/') == LENsave_url:
                        save_url = save_url[0:save_url.rfind('/')]
                    if save_url.rfind('.html') == LENsave_url :
                        save_url = save_url[0:save_url.rfind('.html')]
                    if save_url.rfind('#') == LENsave_url :
                        save_url = save_url[0:save_url.rfind('#')]


                    # if save_url.find('https') == 0:
                    #     save_url = save_url[8:]
                    # if save_url.find('http') == 0 :
                    #     save_url = save_url[7:]
                    # if save_url.find('www') == 0 :
                    #     save_url = save_url[4:]
                    # if save_url.find('ftp') == 0 :
                    #     save_url = save_url[5:]
                    # if save_url.find('file') == 0 :
                    #     save_url = save_url[6:]
                    
                    save_url = save_url.replace('https://', '')
                    save_url = save_url.replace('http://', '')
                    save_url = save_url.replace('www//', '')
                    save_url = save_url.replace('ftp//', '')
                    save_url = save_url.replace('file//', '')
                    save_url = save_url.replace('www.', '')
                    save_url = save_url.replace('.com', '')
                    

                    error_img_str = str(error_img) 
                    error_img_str = error_img_str.replace(", ","a") # (",ここにスペース")
                    

                    error_img_str = error_img_str.replace("[","")
                    error_img_str = error_img_str.replace("]","")
                    #print(error_img_str)


                
            

                    save_line = [save_url,input_url,error_img_str,int(range_tags)]

                    with open(csv_pass, 'a',encoding="utf-8",newline="\n") as f:
                        writer = csv.writer(f)
                        writer.writerow(save_line)

                    print("autosaveしました")

            #del countALL
            #window_refresh(img_tags,count)
            
            window['-counttext-'].update(f"{count+1}/{range_tags+1}")
            #window['-countinput-'].update(count+1)
            
            #count処理           
            if back_scroll == False :
                if range_tags <= count:
                    print('ループしました')
                    count = 0
                    zero_through = False

                if count < range_tags :
                    if range_tags != 1:
                        if timeout != None :
                            if zero_through == True :
                                count += 1
            
            if back_scroll == True:
                if count <= 0 :
                    count = range_tags
                    print("バックループしました")
                    end_count_through = False
                #print("backscroll")
                if range_tags != 1 :
                    if timeout != None:
                        if end_count_through == True :
                            count -= 1
            
            
            if count == 0:
                zero_through = True
            
            if count == range_tags :
                end_count_through = True
            
            
            #window.refresh()
# +-----------------------------------------------------------------------------------+
# + end while
# +-----------------------------------------------------------------------------------+    
        
    
    if event == sg.WIN_CLOSED or bool(window) == False:
        #window is None
        #print("break outside")
        break
           
    if window != None:
        try:
            #csvに変更があったときの処理
            
            #print(r)
            if bool(r) == True :  # r != "" and r != None
                save_url = window["-Input-"].get()
                #print(type(save_url))
                save_url = str(save_url)
                
                if input_url == save_url:
                    
                    #error_img  skipするcount数
                
                    error_img_str = str(error_img) 
                    error_img_str = error_img_str.replace(", ","a") # (",ここにスペース")
                    

                    error_img_str = error_img_str.replace("[","")
                    error_img_str = error_img_str.replace("]","")
                    #print(error_img_str)
                
                    save_line = [r,save_url,error_img_str,int(range_tags)]
                #print(save_url)
                else:
                    save_line = [r,save_url,"",""]
                
                with open(csv_pass, 'a',encoding="utf-8",newline="\n") as f:
                    writer = csv.writer(f)
                    writer.writerow(save_line)
                    
        except NameError: pass
        except Exception as e:
            print(F"save is {e}")
            pass   
        
        try:    
            if g == "Yes":
                listName = window['-listbox-'].get()
                listNameStr = listName[0]
                for i in listBox_nameCol:
                    if i == listNameStr :
                        df = pd.read_csv(csv_pass,index_col=0)
                        #print(df)
                        df = df.drop(i)
                        df.to_csv(csv_pass)
        except NameError: pass
        except Exception as e:
            print(f"delete is {e}")
                            
                        
        #後処理
        try:            
            with open(csv_pass, 'r',encoding="utf-8") as f:
                reader = csv.reader(f)

                listBox = [box for box in reader]
            
            #print(listBox)
            listBox_nameCol  = [line[0] for n,line in enumerate(listBox) if n>0]
            listBox_urlCol = [line[1] for n,line in enumerate(listBox) if n>0]
            listBox_errorCol = [line[2] for n,line in enumerate(listBox) if n>0]
            listBox_rangeCol = [line[3] for n,line in enumerate(listBox) if n>0]            
            
            
            window['-listbox-'].update(listBox_nameCol)

            
            g = None
            r = None
            
        except Exception as e:
            print(f"file is {e}")
                       
        continue    
        
    break


sg.Popup("Good Bye",auto_close_duration= 2,auto_close= True, font=(guiFont,25) ,text_color="darkorange" ,button_type=5) 


####################################################################
#sg.Popup() GUIDE
#
#button_type = defoult  int = 0 button type
#-----------------------------------------------------------------                     
#                       int = 0 sg.yes(s=10)
#                       int = 1 sg.yes(s=10) , sg.no(s=10)
#                       int = 2 
#                       int = 3 sg.button(text='error')
#                       int = 4 ok cancel
#                       int = 5 button == None
#                       int = 6 sg.button(text = 'OK')
# ----------------------------------------------------------------
#                       int = 7 sg.button(text = 'OK')
#                       int = 8 
#                        *  = *
window.close()

