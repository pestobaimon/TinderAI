from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from acc_keys import email,password
import urllib.request
from urllib.parse import urlparse
import os, sys



class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://www.tinder.com')

        sleep(5)

        google_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[1]/div/button')
        google_btn.click()

        sleep(3)

        #switch to login window popup
        base_window = self.driver.window_handles[0]
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

        #input email
        email_input = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email_input.send_keys(email)
        next_btn = self.driver.find_element_by_xpath('//*[@id="identifierNext"]')
        next_btn.click()

        sleep(3)

        #input password
        pw_input = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        pw_input.send_keys(password)
        pw_next_btn = self.driver.find_element_by_xpath('//*[@id="passwordNext"]')
        pw_next_btn.click()


        sleep(5)

        #switch back to tinder window
        self.driver.switch_to.window(handles[0])

        sleep(5)

        allow_location_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        allow_location_btn.click()

        sleep(3)

        disable_notif_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        disable_notif_btn.click()

    def like(self):
        like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        
        like_btn.click()

    def dislike(self):
        
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        dislike_btn.click()

    def auto_swipe(self):
        while True:
            sleep(0.5)
            try:
                self.like()
            except Exception:
                try:
                    self.close_match()
                except Exception:
                    try:
                        self.close_popup()
                    except Exception:
                        pass

    def close_match(self):
        close_match_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        close_match_btn.click()

    def close_popup(self):
        close_popup_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        close_popup_btn.click()

    def get_all_img(self,swipe):
        # get the image source
        srcs = []

        try:
            age = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/span').text
        except:
            age = 'none'
        
        img_click_left = ActionChains(self.driver)
        img_click_right = ActionChains(self.driver)
        img_center_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[1]')
        img_click_left.move_to_element_with_offset(img_center_btn,5,5)
        img_click_left.click()
        img_click_right.move_to_element_with_offset(img_center_btn,60,5)
        img_click_right.click()

        first_pic_hit = 0
        for i in list(range(10)):
            if first_pic_hit >= 2: break
            try:
                img_click_left.perform()
            except Exception:
                print('cannot click left')
            try:
                self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div')
                first_pic_hit+=1
            except Exception:
                pass

        imgcount = 1
        while True:
            sleep(0.1)
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[' + str(imgcount) + ']/div/div[1]'
            try:
                img = self.driver.find_element_by_xpath(xpath)
                srcs.append(img.get_attribute('style'))
                print(img.get_attribute('style'))
                img_click_right.perform()
                imgcount+=1
            except Exception:
                print('failed to get img' + str(imgcount))
                break
        
        urls = []
        for src in srcs:
            count = 0
            for c in src:
                count+=1
                if c == '(':
                    start_char = count
                elif c == ')':
                    end_char = count
            urls.append(src[start_char+1:end_char-2])
            
        for url in urls:
            file_name = os.path.basename(url)
            file_name = 'age_' + str(age) + '_' + file_name
            print(file_name) #Output: 09-09-201315-47-571378756077.jpg
            # download the image
            if(swipe == "left"):
                try:
                    urllib.request.urlretrieve(url, "dataset/nope/" + file_name)
                except Exception:
                    print('save gurl failed')
            else:
                try:
                    urllib.request.urlretrieve(url, "dataset/yea/" + file_name)
                except Exception:
                    print('save gurl failed')

    
    def get_first_img(self,swipe):
        # get the image source
        srcs = []
        try:
            img1 = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div')
            srcs.append(img1.get_attribute('style'))
            try:
                img2 = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[2]/div/div')
                srcs.append(img2.get_attribute('style'))
            except Exception:
                try:
                    img2 = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div/main/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[2]/div/div')
                    srcs.append(img2.get_attribute('style'))
                except Exception:
                    print('failed to get img2')
        except Exception:
            print('failed to get img1')

        
        urls = []
        for src in srcs:
            count = 0
            for c in src:
                count+=1
                if c == '(':
                    start_char = count
                elif c == ')':
                    end_char = count

            urls.append(src[start_char+1:end_char-2])
            
        for url in urls:
            file_name = os.path.basename(url)

            print(file_name) #Output: 09-09-201315-47-571378756077.jpg
            # download the image
            if(swipe == "left"):
                try:
                    urllib.request.urlretrieve(url, "nope/" + file_name)
                except Exception:
                    print('save gurl failed')
            else:
                try:
                    urllib.request.urlretrieve(url, "yea/" + file_name)
                except Exception:
                    print('save gurl failed')


    def data_collect_right(self):
        self.get_all_img('right')
        self.like()

    def data_collect_left(self):
        self.get_all_img('left')
        self.dislike()


    def collect_data(self):
        while True:
            kbin = input('press j to swipe left and k to swipe right. press x to exit')
            if kbin == "j":
                self.data_collect_left
            elif kbin == "k":
                self.data_collect_right
            elif kbin == "x":
                break


bot = TinderBot()
bot.login()
        
        




