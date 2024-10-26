from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
from utils import getPostId

def postCrawling(browser, num):
    posts = browser.find_elements(By.CLASS_NAME, "box-category-item")

    print("This is our posts: ", posts)

    for post in posts:
        link_element = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        link = link_element.get_attribute("href")
        
        print("\n Link of post: ",link)

        postId = getPostId(link)
        print(postId)

        actions = ActionChains(browser)
        actions.key_down(Keys.LEFT_CONTROL).click(link_element).key_up(Keys.LEFT_CONTROL).perform()

        windows = browser.window_handles
        browser.switch_to.window(windows[-1])

        fullText = (WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail-title.article-title")))).text
        title = fullText.splitlines()[0]
        print("\nPost title: ", title)

        author = (WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "author-info")))).text
        print("\nAuthor: ", author)

        date = (WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "detail-time")))).text
        print("\nDate: ", date)

        categoriesElement = (WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item"))))
        categories = []
        
        for category in categoriesElement:
            categories.append(category.text)
        
        print("\nCategories of Post: ", categories)

        browser.close()
        browser.switch_to.window(windows[0])

    