import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse
import requests

def checkLink(link: str):
    standardPrefix = "https://tuoitre.vn"

    return (link[:18] == standardPrefix)

def getPostId(link: str):
    splitLinks = link.split('-')
    rawPostId = splitLinks[-1]
    postIdList = rawPostId.split('.')
    return postIdList[0]

def getTitle(element):
    fullTitle = (WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail-title.article-title")))).text
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
    if not os.path.exists('images'):
        os.makedirs('images')
        
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
    listCommentPopUpElement = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lstcommentpopup")))
    commentElements = WebDriverWait(listCommentPopUpElement, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-comment")))
    
    for commentElement in commentElements:
        print("\nComment Text:", commentElement.text)
