from bs4 import BeautifulSoup
from pyrogram import Client
import time,sqlite3,os
from requests_html import HTMLSession


bot = Client( # setting pyrogram - visit my.telegram.org and @botfather 
  "prothomaloX",
  api_id =  int(os.environ.get("ID")),
  api_hash = os.environ.get("HASH"),
  bot_token= os.environ.get("TOKEN"))

co = sqlite3.connect("newses.db",check_same_thread=False) # create a new database named 'newses.db'
cu = co.cursor()
cu.execute("CREATE TABLE IF NOT EXISTS pa (news TEXT,images TEXT,videos TEXT)")
co.commit()

while True:
    session = HTMLSession(browser_args=["--no-sandbox"])
    r = session.get("https://www.prothomalo.com/collection/latest")
    r.html.render(timeout=30)
    soup = BeautifulSoup(r.html.html,"lxml")
    news = soup.find_all('div',class_="left_img leftImageRightNews-m__left_img__2vxV3")

    for sources in news:
        source = sources.find('a')['href']
        cu.execute(f"SELECT * FROM pa WHERE news='{source}'")
        v = cu.fetchall()
        if len(v)==0:
            try:
                session = HTMLSession(browser_args=["--no-sandbox"])
                rr = session.get(source)
                rr.html.render(timeout=30)
            except: continue
            page = BeautifulSoup(rr.html.html,'lxml')
            title = page.find('meta',property="og:title")['content']
            #author = page.find('meta',{'name':'author'})['content']
            description = page.find('meta',{'name':'description'})['content']
            image = page.find('meta',property="og:image")['content']
            #print(title,description,image,author)
            post = f"<b><a href='{source}'>{title}</a></b>\n\n{description}"
            imagei = image.split('?')[0]
            try: 
                with bot: bot.send_photo(f'prothomaloX',imagei,post)
                print('Posted',source)
            except Exception as e: 
              print(e)
              continue
            cu.execute(f"INSERT INTO pa (news) VALUES ('{source}')")
            co.commit()
        else:
            print('No new news. Naping...',int(time.time()))
            time.sleep(120)
            break

    ## Images from prothom alo - Will be worked on in near future..
    # print('Searching for images...',int(time.time()))
    # sessioni = HTMLSession()
    # ri = sessioni.get("https://www.prothomalo.com/photo")
    # ri.html.render(timeout=30)
    # soup = BeautifulSoup(ri.html.html,"lxml")
    # ilinks = soup.find_all('a',{'class':'newsHeadline-m__title-link__1puEG'})

    # for images in ilinks:
    #     ilink = images['href']
    #     cu.execute(f"SELECT * FROM pa WHERE images='{ilink}'")
    #     v = cu.fetchall()
    #     if len(v)==0:
    #         try:
    #             session = HTMLSession()
    #             rr = session.get(ilink)
    #             rr.html.render(timeout=30)
    #         except: continue
    #         page = BeautifulSoup(rr.html.html,'lxml')
    #         title = page.find('meta',property="og:title")['content']
    #         #author = page.find('meta',{'name':'author'})['content']
    #         description = page.find('meta',{'name':'description'})['content']
    #         image = page.find('meta',property="og:image")['content']
    #         imageix = image.split('?')[0]
    #         post = f"<b><a href='{ilink}'>{title}</a></b>\n\n{description}"
    #         # print(title,description,image,author)
    #         try: 
    #             print(imageix)
    #             with bot: bot.send_photo('prothomaloX',imageix,post)
    #             print('Posted',ilink)
    #         except Exception as e: print(e)
    #         cu.execute(f"INSERT INTO pa (images) VALUES ('{ilink}')")
    #         co.commit()
    #     else:
    #         print('No new images. Naping...',int(time.time()))
    #         time.sleep(120)
    #         break
