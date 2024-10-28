import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.common.action_chains import ActionChains

from urllib.parse import urlparse
import requests
import time

def checkLink(link: str):
    standardPrefix = "https://tuoitre.vn"

    return (link[:18] == standardPrefix)

def getPostId(link: str):
    splitLinks = link.split('-')
    rawPostId = splitLinks[-1]
    postIdList = rawPostId.split('.')
    return postIdList[0]

def getTitle(element):
    fullTitle = (WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail-title")))).text
    return fullTitle.splitlines()[0]

def getContent(element):
    return (WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail-cmain.clearfix")))).text

def getAuthor(element):
    return (WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "author-info")))).text

def getDate(element):
    return (WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "detail-time")))).text

def getCategories(element):
    categoriesElement = WebDriverWait(element, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item")))
    categories = []
    
    for category in categoriesElement:
        categories.append(category.text)
    
    return categories

def getPostReacts(element):
    reactInfoElement = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "reactinfo")))
    reactElements = WebDriverWait(reactInfoElement, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "span")))
    
    index = 0
    reacts = []
    for reactElement in reactElements:
        if reactElement.get_attribute("data-reactid") is not None:
            index += 1
            reacts.append({index: reactElement.text})
    
    return reacts

def crawlImages(element, postId):
    contentElement = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail-cmain.clearfix")))
    imageElements = WebDriverWait(contentElement, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        
    imageDirectory = os.path.join("images", postId)
    if not os.path.exists(imageDirectory):
        os.makedirs(imageDirectory)
        
    for img in imageElements:
        src = img.get_attribute('src')
        if src:
            imageResponse = requests.get(src)
            imageName = os.path.basename(urlparse(src).path)
            imagePath = os.path.join(imageDirectory, imageName)
            with open(imagePath, 'wb') as file:
                file.write(imageResponse.content)
            print("\nAudio file downloaded successfully!")

def crawlAudio(element, postId):
    audio_element = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.TAG_NAME, "audio")))
    audio_url = audio_element.get_attribute("src")
    print("\nAudio URL:", audio_url)
    
    audioResponse = requests.get(audio_url)
    audioFilePath = os.path.join("audio", postId + ".m4a")
    with open(audioFilePath, "wb") as file:
        file.write(audioResponse.content)
    print("\nAudio file downloaded successfully!")
    
def crawlComments(element):
    try:
        # Attempt to find the element
        showAllCommentsElement = WebDriverWait(element, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'commentpopupall')))
        actions = ActionChains(element)
        actions.click(showAllCommentsElement).perform()
        print("\nShowAllComments Button Clicked!!")
        
    except TimeoutException:
        # Handle the exception when the element is not found
        print("\nShowAllComments Button Not Found, continuing with the program")
        return
        
    try:
        listCommentPopUpElement = WebDriverWait(element, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "lstcommentpopup")))
        commentElements = WebDriverWait(listCommentPopUpElement, 2).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-comment")))
        commentCnt = len(commentElements)
        
        while True:
            element.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", listCommentPopUpElement)
            time.sleep(1)  # Wait for lazy loading
            
            newCommentCnt = len(listCommentPopUpElement.find_elements(By.CLASS_NAME, "item-comment"))
            
            if newCommentCnt == commentCnt:
                break
            
            commentCnt = newCommentCnt
        
        commentElements = WebDriverWait(listCommentPopUpElement, 2).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-comment")))
        for commentElement in commentElements:
            try:
                moreButton = commentElement.find_element(By.TAG_NAME, 'a')
                if moreButton.is_displayed():
                    actions = ActionChains(element)
                    actions.move_to_element(moreButton).click().perform()
            except NoSuchElementException:
                pass
            
            commentId = commentElement.get_attribute('data-cmid')
            author = commentElement.get_attribute('data-replyname')
            text = WebDriverWait(commentElement, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "contentcomment"))).text
            
            dateElement = commentElement.find_element(By.CLASS_NAME, "timeago")
            date = dateElement.get_attribute("title")
            
            reacts = []
            reactListElement = commentElement.find_element(By.CLASS_NAME, "listreact")
            reactElements = reactListElement.find_elements(By.CLASS_NAME, "colreact")
            for reactElement in reactElements:
                num = element.execute_script("return arguments[0].textContent", reactElement)
                reacts.append({reactElement.get_attribute("data-recid") : num})
            
            
            print("\nComment Section: ")
            print("\n\tComment Id: ", commentId)
            print("\n\tComment author: ", author)
            print("\n\tComment text: ", text)
            print("\n\tComment date: ", date)
            print("\n\tComment reacts: ", reacts)
            
            try:
                viewReplyButton = commentElement.find_element(By.CLASS_NAME, "btn-cm.viewreply")
                if viewReplyButton.is_displayed():
                    actions = ActionChains(element)
                    actions.move_to_element(viewReplyButton).click().perform()
                
                    replyElements = WebDriverWait(commentElement, 2).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-comment")))
                    for replyElement in replyElements:
                        replyId = replyElement.get_attribute("data-cmid")
                        replyAuthor = replyElement.get_attribute("data-replyname")
                        replyText = replyElement.find_element(By.CLASS_NAME, "contentcomment").text
                        
                        replyDateElement = replyElement.find_element(By.CLASS_NAME, "timeago")
                        replyDate = replyDateElement.get_attribute("title")
                        
                        replyReacts = []
                        replyReactListElement = replyElement.find_element(By.CLASS_NAME, "listreact")
                        replyReactElements = replyReactListElement.find_elements(By.CLASS_NAME, "colreact")
                        for reactElement in replyReactElements:
                            num = element.execute_script("return arguments[0].textContent", reactElement)
                            replyReacts.append({reactElement.get_attribute("data-recid") : num})
                            
                        print("\n\t\tComment Id: ", replyId)
                        print("\n\t\tComment author: ", replyAuthor)
                        print("\n\t\tComment text: ", replyText)
                        print("\n\t\tComment date: ", replyDate)
                        print("\n\t\tComment reacts: ", replyReacts)
                
            except NoSuchElementException:
                pass
    except TimeoutException:
        print("\nComment not found!")
