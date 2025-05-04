import praw
import re
import requests


## Reddit Credentials
username = "NAME-OF-REDDIT-ACCOUNT"
password = "PASSWORD-OF-REDDIT-ACCOUNT"
client_id = "CLIENT-ID-OF-REDDIT-ACCOUNT"
client_secret = "CLIENT-SECRET-OF-REDDIT-ACCOUNT"

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    username = username,
    password = password,
    user_agent = "ANYTHING"
)


command = r"\\\[animebot\\\]\s*-synopsis\s+(.+)"


## Getting Synopsis
def getAnimeName(anime_name):
    url = "https://api.jikan.moe/v4/anime?q={0}&limit=1".format(anime_name)
    response = requests.get(url)
    if response.status_code == 200:
        fullAnimeData = response.json() #store json data in anime_data - Dict
        partAnimeData = fullAnimeData['data'][0] #Dict('data') -> List(0) -> Dict(partAnimeData)
        if type(partAnimeData) == dict:
            return partAnimeData['synopsis']
        else:
            ErrorMessageFinding = "Sorry, I could not find this Anime"
            return ErrorMessageFinding
    else:
        ErrorMessageGet = "This Anime could not be found"
        return ErrorMessageGet
    

## Italicize Synopsis
def italicizeSynopsis(synopsis):
    paragraphs = synopsis.strip().split("\n")
    italicized = []
    for paragraph in paragraphs:
        if paragraph.strip():
            italicized.append("*{0}*".format(paragraph.strip()))
    return "\n\n".join(italicized)


## Processing Comment
def process(comment):
    match = re.search(command, comment.body, re.IGNORECASE)
    if match:
        anime_name = match.group(1).strip()
        synopsis = getAnimeName(anime_name)
        italic_synopsis = italicizeSynopsis(synopsis)
        comment.reply("{0}".format(italic_synopsis))


## Check if a comment is already replied by the bot
def alreadyReplied(comment):
    try:
        comment.refresh()
    except praw.exceptions.ClientException: ##if something went wrong -> False
        return False
    for reply in comment.replies:
        author = reply.author
        print(author)
        if author == reddit.user.me():
            return True
    return False


## bot
def main():
    for comment in reddit.subreddit("TARGET-SUBREDDIT").stream.comments():
        if alreadyReplied(comment):
            pass
        elif r"\[animebot\]" in comment.body and "-synopsis" in comment.body:
            process(comment)


## run
if __name__ == "__main__":
    main()






    
