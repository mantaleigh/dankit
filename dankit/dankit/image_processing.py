# last update: 2/17/16 by svoigt
# TODO: error checking and message for bad photos
# TODO: remove hard coded strings
# TODO: error checking error checking error checking
# TODO: pull it out of development mode
# TODO: make an admin account on the server
# TODO: get rid of print statements
# TODO: get rid of hard coding
# TODO: improve what happens when the giphy api doesn't have any results (pick the most prevalent emotion?) 

import httplib, urllib, base64, json, random, ast

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '0fe9b3c39d684f888e777f2b109922ad',
}

params = urllib.urlencode({
    # Request parameters
    # 'faceRectangles': '{string}',
})


def get_search_terms(url):
    synonyms = {"anger":["angry","frustrated","mad"],"contempt":["disappointed","contempt","disapprove","eyeroll"],"disgust":["disgust","disgusted","ew","eww"],"fear":["scared","wtf","shocked"],"happiness":["happy","dance","excited"],"neutral":["meme","internet"],"sadness":["sad","cry","upset"],"surprise":["surprise","omg","shock"]}
    try:
        if not url.startswith('http://'): 
            url = 'http://' + url
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        print url
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, json.dumps({ 'url': url }), headers)
        response = conn.getresponse()
        data = ast.literal_eval(response.read())
        print "Data: "
        print(data)
        print type(data)
        conn.close()
        searchTerms = list()
        allEmotions = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]
        for person in data: 
            print person
            if person["scores"]["neutral"]>.70:
                searchTerms.extend(["internet","meme"])
            else:
                for emo in allEmotions:
                    print emo
                    found = False
                    for emo in person["scores"]:
                        if person["scores"][emo] >= .30:
                            searchTerms.append(emo)
                            found = True
                        print searchTerms
                    if not found:
                        print "Error: did not find emotion: " + emo
        return find_gif(set(searchTerms))
    except Exception as e:
        raise


def find_gif(searchTerms, lastTry=False):
    synonyms = {"anger":["angry","frustrated","mad"],"contempt":["disappointed","contempt","disapprove","eyeroll"],"disgust":["disgust","disgusted","ew","eww"],"fear":["scared","wtf","shocked"],"happiness":["happy","dance","excited"],"neutral":["meme","internet"],"sadness":["sad","cry","upset"],"surprise":["surprise","omg","shock"]}
    searchTerms = list(searchTerms)
    search_string = searchTerms[0]
    for term in searchTerms: 
        if term in synonyms:
            search_string = search_string + '+' + term + '+' + random.choice(synonyms[term])
    print search_string
    print searchTerms
    gif_data = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/random?tag=" + search_string + "&api_key=dc6zaTOxFJmzC").read())
    #chosen_image = random.choice(gif_data["data"])
    
    if gif_data['data']:
        return gif_data["data"]["image_original_url"] #chosen_image["images"]["original"]["url"]
    else:
        if lastTry: 
            return ''
        return find_gif(random.choice(searchTerms), lastTry=True)


