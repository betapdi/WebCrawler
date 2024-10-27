import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
from utils import getPostId, getTitle, getContent, getAuthor, getCategories, getDate, getPostReacts
from utils import checkLink, crawlImages, crawlAudio, crawlComments

from selenium.common.exceptions import TimeoutException

def postCrawling(browser, num):
    if not os.path.exists('audio'):
        os.makedirs('audio')
    
    if not os.path.exists('images'):
        os.makedirs('images')
                    
    posts = browser.find_elements(By.CLASS_NAME, "box-category-item")

    # print("This is our posts: ", posts)

    cnt = 0
    for post in posts:
        if (cnt == num):
            break 
        cnt += 1
        
        link_element = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        link = link_element.get_attribute("href")
        
        if checkLink(link) == False:
            continue
        
        print("\n Link of post: ", link)

        postId = getPostId(link)
        print(postId)

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

        title = getTitle(browser)
        print("\nPost title: ", title)
        
        content = getContent(browser)
        print("\nContent: ", content)

        author = getAuthor(browser)
        print("\nAuthor: ", author)

        date = getDate(browser)
        print("\nDate: ", date)

        categories = getCategories(browser)
        print("\nCategories of Post: ", categories)
        
        postReacts = getPostReacts(browser)
        print("\nPost Reactions: ", postReacts)
        
        crawlImages(browser, postId)
        crawlAudio(browser, postId)
        
        try:
            # Attempt to find the element
            showAllCommentsElement = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'commentpopupall')))
            actions = ActionChains(browser)
            actions.click(showAllCommentsElement).perform()
            print("\nShowAllComments Button Clicked!!")
            
        except TimeoutException:
            # Handle the exception when the element is not found
            print("\nShowAllComments Button Not Found, continuing with the program")
            
        crawlComments(browser)

        browser.close()
        browser.switch_to.window(windows[0])

    