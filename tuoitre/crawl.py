import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
from utils import getPostId, getTitle, getContent, getAuthor, getCategory, getDate, getPostReacts
from utils import checkLink, crawlImages, crawlAudio, crawlComments

from selenium.common.exceptions import TimeoutException

import json, time

def postCrawling(browser, num):
    if not os.path.exists('audio'):
        os.makedirs('audio')
    
    if not os.path.exists('images'):
        os.makedirs('images')
        
    if not os.path.exists('data'):
        os.makedirs('data')
        
    listPostsElement = browser.find_elements(By.CLASS_NAME, "list__listing")
    
    while True:
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", listPostsElement)
        time.sleep(1)  # Wait for lazy loading
        
        numPosts = len(browser.find_elements(By.CLASS_NAME, "box-category-item"))
        # print("\nNumber of posts: ", numPosts)
        
        if numPosts >= int(num):
            break

    posts = browser.find_elements(By.CLASS_NAME, "box-category-item")
    # # print("This is our posts: ", posts)

    cnt = 0
    for post in posts:
        if (cnt == int(num)):
            break 
        
        link_element = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        link = link_element.get_attribute("href")
        # link = "https://tuoitre.vn/chu-doanh-nghiep-lap-bat-chong-nang-noi-gi-ve-viec-hieu-truong-ke-khai-gia-bat-gap-3-lan-20241025142325469.htm"
        
        if checkLink(link) == False:
            continue
        
        # print("\n Link of post: ", link)

        postId = getPostId(link)
        # print(postId)

        actions = ActionChains(browser)
        actions.key_down(Keys.LEFT_CONTROL).click(link_element).key_up(Keys.LEFT_CONTROL).perform()

        windows = browser.window_handles
        browser.switch_to.window(windows[-1])
        
        currentUrl = browser.current_url
        if (checkLink(currentUrl) == False): 
            if (len(windows) == 1):
                browser.back()
            
            else:
                browser.close()
                browser.switch_to.window(windows[0])
                
            continue
        
        cnt += 1

        title = getTitle(browser)
        # print("\nPost title: ", title)
        
        content = getContent(browser)
        # print("\nContent: ", content)

        author = getAuthor(browser)
        # print("\nAuthor: ", author)

        date = getDate(browser)
        # print("\nDate: ", date)

        category = getCategory(browser)
        # print("\nCategories of Post: ", categories)
        
        postReacts = getPostReacts(browser)
        # print("\nPost Reactions: ", postReacts)
        
        crawlImages(browser, postId)
        audioUrl = crawlAudio(browser, postId)
            
        comments = crawlComments(browser)

        post = {}
        post["postId"] = postId
        post["title"] = title
        post["content"] = content
        post["author"] = author
        post["date"] = date
        post["category"] = category
        post["audioUrl"] = audioUrl
        post["reactions"] = postReacts
        post["comments"] = comments
        
        json_post = json.dumps(post, indent = 4)
        
        postFilePath = os.path.join('data', postId + ".json")
        with open(postFilePath, "w") as file:
            file.write(json_post)
            
        print("Post " + postId + " has been written into json file!!")
        
        browser.close()
        browser.switch_to.window(windows[0])
        
        

    