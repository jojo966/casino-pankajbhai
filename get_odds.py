# from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver 
import threading
import os

options=webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-sh-usage")

# driver = webdriver.Chrome(seleniumwire_options=options)


driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options)
# driver = webdriver.Firefox(executable_path='geckodriver.exe',firefox_options=options)
driver.get("https://world777.com/admin")
# print(driver.requests)
sleep(20)

def login():
    sleep(30)
    print("website load...")
    btn_login = driver.find_element_by_xpath("//button[@class='btn btn-primary login-btn']") #<button data-v-f57657b2="" class="btn btn-primary login-btn">Login</button>
    btn_login.click()
    sleep(10)
    username = driver.find_element_by_id("input-1")
    username.send_keys("Demo801")
    sleep(3)
    password = driver.find_element_by_id("input-2")
    password.send_keys("Abab2020")
    sleep(3)
    lg_btn = driver.find_element_by_xpath("//button[@class='btn btn-block btn-theme1 btn-lg btn-submit btn-secondary'][@type='submit']") # login button 
    lg_btn.click()    
    sleep(30)
    if driver.current_url =="https://world777.com/admin/home":    
        print("logged in successfully")
        driver.get("https://world777.com/admin/casino/teenpattit20")
    else:
        print(driver.current_url)
        print("not logged in...error")

login()
sleep(20)
print("getting live odds")
def get_odds():
    while True:
        list_of_data = []
        list_of_data.append("{\n")
        list_of_data.append("\"success:True\",\n")
        # f.write("{")
        # f.write('\"sucess\":true,')
        list_of_data.append('\"game\":')
        try:
            game_name = driver.find_element_by_xpath("//span[@class='casino-name']").text
            game_round_id = driver.find_element_by_xpath("//div[@class='casino-video-rid']").text
            # print(game_name)
            # print(game_round_id)
            list_of_data.append(f'[\"game_name\":\"{game_name}\",\"game_round_id\":\"{game_round_id}\"],\n')
        except:
            sleep(10)
            game_name = driver.find_element_by_xpath("//span[@class='casino-name']").text
            game_round_id = driver.find_element_by_xpath("//div[@class='casino-video-rid']").text
            # print(game_name)
            # print(game_round_id)
            list_of_data.append(f'[\"game_name\":\"{game_name}\",\"game_round_id\":\"{game_round_id}\"],\n')

        list_of_data.append("\"last_result\":")
        try:
            last_result = driver.find_element_by_xpath("//div[@class='casino-video-last-results']").text
            last_result = last_result.split()
            last_result.pop() #remove last ... of link 
            list_of_data.append(f"{last_result},\n")
        except:
            sleep(10)
            last_result = driver.find_element_by_xpath("//div[@class='casino-video-last-results']").text
            last_result = last_result.split()
            last_result.pop() #remove last ... of link
            list_of_data.append(f"{last_result},\n")



        #timer 

        timer = driver.find_element_by_xpath("//div[@class='casino-timer']").text
        timer =timer.replace("\n","")
        list_of_data.append(f"\"timer\":{timer},\n")
        print(f"timer:"+timer)

        # #cards img
        # <div class="casino-video-cards"><div class="casino-cards-shuffle"><i class="fas fa-grip-lines-vertical"></i></div> <div class="casino-video-cards-container"><div><span data-v-b64efdfa=""><img data-v-b64efdfa="" src="https://sitethemedata.com/v3/static/front/img/cards/JDD.png"></span> <span data-v-b64efdfa=""><img data-v-b64efdfa="" src="https://sitethemedata.com/v3/static/front/img/cards/1.png"></span> <span data-v-b64efdfa=""><img data-v-b64efdfa="" src="https://sitethemedata.com/v3/static/front/img/cards/1.png"></span></div> <div><span data-v-b64efdfa=""><img data-v-b64efdfa="" src="https://sitethemedata.com/v3/static/front/img/cards/KDD.png"></span> <span data-v-b64efdfa=""><img data-v-b64efdfa="" src="https://sitethemedata.com/v3/static/front/img/cards/1.png"></span> <span data-v-b64efdfa=""><img data-v-b64efdfa="" src="https://sitethemedata.com/v3/static/front/img/cards/1.png"></span></div></div></div>
        div_source = driver.find_element_by_xpath("//div[@class='casino-video-cards-container']").get_attribute('innerHTML')
        soup = BeautifulSoup(div_source,'html.parser')
        all_img_tag = soup.find_all('img')
        player_a_cards =[]
        player_b_cards = []
        j=0
        for i in all_img_tag:
            if j>=3:
                player_b_cards.append(str(i['src']))
            else:
                player_a_cards.append(str(i['src']))
            j+=1
        list_of_data.append(f"\"player_a_cards\":{player_a_cards},\n")
        list_of_data.append(f"\"player_b_cards\":{player_b_cards},\n")
       
        #odds 
        list_of_data.append("\"player_a_odds\":[") # appeend "plyera":[
        odds_box_list = driver.find_elements_by_xpath("//div[@class='casino-bl-box mb-4']") #find elements
        
        #player_a_odds 

        source_a = odds_box_list[0].get_attribute('innerHTML') #get source code of div
        name = ['WINNER','KHAL','TOTAL','PAIR PLUS'] #title of odds
        soup = BeautifulSoup(source_a,'html.parser') 
        soup_text = soup.text #get text from source code 
        list_of_odds_a = soup_text.split() #split str to list
        list_of_odds_a = list_of_odds_a[::2] #get required odds
        dict_of_player_a_odds = dict(zip(name,list_of_odds_a)) #combine title and odds and make dict
        list_of_data.append(f"{dict_of_player_a_odds},") #add first odds dict to player a
        # print(list_o  f_odds_a)
        # print(list_of_data)
        
        #play_a_odds2
        odds2_box_list =driver.find_elements_by_xpath("//div[@class='casino-rb-box-container mb-3']")
        player_a_odds2_source = odds2_box_list[0].get_attribute('innerHTML') #get source code of box        
        soup = BeautifulSoup(player_a_odds2_source,'html.parser') #apply soup
        img_list = soup.find_all('img') #find all img tag inside div
        img_src=[]  
        for i in img_list: #itrate through list of img tag and find src of images
            img_src.append(i['src'])        
        book_black = soup.find_all('span',{'class':'d-block casino-box-odd'}) #d-block casino-box-odd == value  
        if len(img_src)!=0:
            rate=[]
            for i in book_black:
                rate.append(i.text)
            
            img_src.insert(2,rate[0])
            img_src.insert(5,rate[1])
            # print(img_src)
        else:
            img_src.insert(0,0)
            img_src.insert(1,0)
            img_src.insert(2,0)
            img_src.insert(3,0)
            img_src.insert(4,0)
            print('in else')
        # print(img_src)
        list_of_data.append(f'{img_src}],\n')

        #player_b odds  starts from here
        list_of_data.append("\"player_b_odds\":[")
        
        #player_b_odds1 
        source_b = odds_box_list[1].get_attribute('innerHTML') #get source code of div
        name = ['WINNER','KHAL','TOTAL','PAIR PLUS'] #title of odds
        soup = BeautifulSoup(source_b,'html.parser') 
        soup_text = soup.text #get text from source code 
        list_of_odds_b = soup_text.split() #split str to list
        list_of_odds_b = list_of_odds_b[::2] #get required odds
        dict_of_player_b_odds = dict(zip(name,list_of_odds_b)) #combine title and odds and make dict
        list_of_data.append(f"{dict_of_player_b_odds},") #add first odds dict to player a
        
        #player_b_odds_2
        
        odds2_box_list =driver.find_elements_by_xpath("//div[@class='casino-rb-box-container mb-3']")
        player_b_odds2_source = odds2_box_list[1].get_attribute('innerHTML') #get source code of box        
        soup = BeautifulSoup(player_b_odds2_source,'html.parser') #apply soup
        img_list = soup.find_all('img') #find all img tag inside div
        img_src=[]  
        for i in img_list: #itrate through list of img tag and find src of images
            img_src.append(i['src'])        
        book_black = soup.find_all('span',{'class':'d-block casino-box-odd'}) #d-block casino-box-odd == value  
        if len(img_src)!=0:
            rate=[]
            for i in book_black:
                rate.append(i.text)
            
            img_src.insert(2,rate[0])
            img_src.insert(5,rate[1])
            # print(img_src)
        else:
            img_src.insert(0,0)
            img_src.insert(1,0)
            img_src.insert(2,0)
            img_src.insert(3,0)
            img_src.insert(4,0)
            print('in else')
        # print(img_src)
        list_of_data.append(f'{img_src}]\n')
        list_of_data.append("}")
        # print(list_of_data)
        
        
        
        
        
        
        f = open("odd.json","w",encoding="utf-8")  
        for i in list_of_data:
            f.write(i)
        f.close()
        print("data succesfully written")



        

        
        
        
        
        
        # div_element = driver.find_elements_by_xpath("//div[@class='casino-detail']") #class="dealer-name w-100 mb-1"
        # # print(type(div_element))
        # # print(div_element) 
        # for i in div_element:
        #     d = i.text #get text in string format
        #     d_list = d.split() #split it to list
        #     # print(f"before len of d_list {len(d_list)}")
        #     # f.write(f"before len of d_list {len(d_list)}\n")
        #     # print(d_list)

        #     #delete unwanted elements
        #     index_to_remove = d_list.index("R:100-100K") # remove 
        #     d_list =  d_list[:index_to_remove]
        #     # print(d_list)
        #     #remove unwanted zeros
        #     # print(f"after len of d_list {len(d_list)}")
        #     # f.write(f"after len of d_list {len(d_list)}\n")
      
        #     # print(d_list)
        #     #      0      1      2     3         4     5    6        7    8        9     10      11   12       13       14    15     16    17     18      19
        #     # ['Total', '0', '12.12', '13.74', '0', 'Total', '1', '3.83', '4.09', '0', 'Total', '2', '2.31', '2.41', '0', 'Total', '3', '4.11', '4.41', '0']
        #     total_0={}
        #     total_0.setdefault(d_list[0]+d_list[1],[])
        #     for i in range(1,3):
        #         total_0[d_list[0]+d_list[1]].append(d_list[i+1])

        #     total_1 = {}
        #     total_1.setdefault(d_list[5]+d_list[6],[])
        #     for i in range(6,8):
        #         total_1[d_list[5]+d_list[6]].append(d_list[i+1])              
           
        #     total_2 = {}
        #     total_2.setdefault(d_list[10]+d_list[11],[])
        #     for i in range(11,13):
        #         total_2[d_list[10]+d_list[11]].append(d_list[i+1])

        #     total_3 = {}
        #     total_3.setdefault(d_list[15]+d_list[16],[])
        #     for i in range(16,18):
        #         total_3[d_list[15]+d_list[16]].append(d_list[i+1])
                
        #     # total_0 = {(d_list[0]+d_list[1]):d_list[i+1] for i  in range(1,3)}
        #     # total_1 = {(d_list[5]+d_list[6]):d_list[i+1] for i in range(6,8)}
        #     # total_2 = {(d_list[10]+d_list[11]):d_list[i+1] for i in range(11,13)}
        #     # total_3 = {(d_list[15]+d_list[16]):d_list[i+1] for i in range(16,18)}
        #     print(total_0)
        #     print(total_1)
        #     print(total_2)
        #     print(total_3)
           
        #     f.write(str(total_0))
        #     f.write(str(total_1))
        #     f.write(str(total_2))
        #     f.write(str(total_3))
def get_last_result_cards():
    while True:
        #last result cards 
        list_of_data =[]
        list_of_data.append("\"last_result_cards\":")
        last_result_div = driver.find_element_by_xpath("//div[@class='casino-video-last-results']").get_attribute('innerHTML')
        soup = BeautifulSoup(last_result_div,'html.parser')
        span_list =soup.find_all('span')
        # print(len(span_list))
        temp_data=[]
        z=0
        l=[]
        for i in span_list:
            l.append(i['class'])
        process=[]
        for i in l:
            class_nm = i[0]
            c_out = process.count(class_nm)
            # print(c_out)
            # print(f'//span[@class="{class_nm}"]')
            try:
                span = driver.find_elements_by_xpath(f'//span[@class="{class_nm}"]')[c_out]
                sleep(1)
                span.click()
                process.append(class_nm)
                sleep(2)
                cards_box = driver.find_element_by_xpath('//div[@class="col-12 col-lg-8"]').get_attribute('innerHTML')
                soup = BeautifulSoup(cards_box,'html.parser')
                img_lst = soup.find_all("img")
                result= []
                for i in  img_lst:
                    result.append(i['src'])
                # print(result)

                if(result.index("https://sitethemedata.com/v3/static/front/img/winner.png") ==3):
                    temp_data.append("\"b\":")
                    z+=1
                else:
                    temp_data.append("\"a\":")
                    z+=1
                temp_data.append(f"{result}")
                driver.find_element_by_class_name("close").click()
                list_of_data.append(f"{temp_data}")
                list_of_data.append("}")        
                    
                f = open("last_result_card.json","w")
                for i in list_of_data:
                    f.write(i)
                f.close()
                print("last resultwriteen succesfull")
            except:
                continue
if __name__ =="__main__":  
    t1 = threading.Thread(target=get_odds)
    t2 = threading.Thread(target=get_last_result_cards)
    t1.start()
    t2.start()

# while True:
    # get_odds()
# get_odds()

