from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from time import sleep, strftime
from random import randint
import pandas as pd

class InstaBot:
    def __init__(self, username, pwd):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pwd)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(4)



    # def browser_discover(self):
    #     driver = self.driver
    #     driver.find_element_by_xpath("//a[@href= \"/explore/\"]")\
    #         .click()
    #     sleep(4)
    #     pics = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]')\
    #         .click()
    #     links = pics.find_elements_by_tag_name('a')
    #     #get one or more random pics
    #     num_pic = floor(random() * 10)
    #     print(num_pic)
    #     pic_href = links[num_pic].get_attribute('href')
    #     print(pic_href)
    #     driver.Navigate().GoToUrl(pic_href)
    #     sleep(3)
    #     driver.find_element_by_xpath("//a[@aria-label=\"Like\"]")\
    #         .click()
    #     sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()    
        self.driver.implicitly_wait(20)
        
        ##get following list
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names()

        # ##get followers list
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()

        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def _get_names(self):
        # sleep(2)
        # sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        # self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        return names


    def like_and_follow(self):
        hashtag_list = ['Actress', 'MadridActor', 'theatre']

        # prev_user_list = [] 
        # - if it's the first time you run it, use this line and comment the two below
        prev_user_list = pd.read_csv('20200525-162126_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
        prev_user_list = list(prev_user_list['0'])
        new_followed = []
        tag = -1
        followed = 0
        likes = 0
        comments = 0    

        for hashtag in hashtag_list:
            tag += 1
            self.driver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
            sleep(5)
            first_thumbnail = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

            first_thumbnail.click()
            sleep(randint(10,40))
            try:
                for x in range(1,10):
                    
                    username = self.driver.find_element_by_xpath('//html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a').text
                    print('USERNAME')
                    print(username)

                    if username not in prev_user_list:
                        # # If we already follow, do not unfollow
                        if self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == "Follow":
                            self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                            print('DID FOLLOW')
                            print(username)
                            new_followed.append(username)
                            followed += 1
                            sleep(randint(10,20))

                            # Liking the picture
                            button_like = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
                            likes += 1
                            print('DID like')
                            print(likes)
                            sleep(randint(18,25))

                            # Comments and tracker
                            comm_prob = randint(1,10)
                            print('{}_{}: {}'.format(hashtag, x,comm_prob))
                            if comm_prob > 7:
                                comments += 1
                                self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]').click()
                                comment_box = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea')

                                if (comm_prob < 7):
                                    comment_box.send_keys('Really cool!')
                                    sleep(5)
                                elif (comm_prob > 6) and (comm_prob < 9):
                                    comment_box.send_keys('Nice work :)')
                                    sleep(5)
                                elif comm_prob == 9:
                                    comment_box.send_keys('Nice gallery!!')
                                    sleep(5)
                                elif comm_prob == 10:
                                    comment_box.send_keys('So cool! :)')
                                    sleep(5)
                                #Enter to post comment
                                comment_box.send_keys(Keys.ENTER)
                                sleep(randint(22,28))

                            # Next picture
                            self.driver.find_element_by_link_text('Next').click()
                            sleep(randint(25,29))

                    else:
                        self.driver.find_element_by_link_text('Next').click()
                        sleep(randint(20,26))
            #some hashtag stops refreshing photos (it may happen sometimes), it continues to the next 
            except:
                print("WAS UNABLE TO TRY")
                continue

        for n in range(0,len(new_followed)):
            prev_user_list.append(new_followed[n])
            print("PREVIOUS USERlist IS NOW")
            print(prev_user_list)

        updated_user_df = pd.DataFrame(prev_user_list)
        updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
        print('Liked {} photos.'.format(likes))
        print('Commented {} photos.'.format(comments))
        print('Followed {} new people.'.format(followed))





##tester account 
##tarshatester TD011795
## tarsha17, TD011795!
##memes101spain
##TD011795

##bobbygreenmemes
##TD011795

my_bot = InstaBot('memes101spain', 'TD011795')
# my_bot.get_unfollowers()
my_bot.like_and_follow()