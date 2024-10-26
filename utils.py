
def getPostId(link: str):
    splitLinks = link.split('-')
    rawPostId = splitLinks[-1]
    postIdList = rawPostId.split('.')
    return postIdList[0]
