from facebook_scraper import get_posts
import os
import openai
import re
from cleantext import clean
import time

openai.api_base = "http://llama.qrt.services:8000/v1" # point to the local server
openai.api_key = "" # no need for an API key

colleges = ["collingwood","cuths","johns","chads","hatfield","castle","marys","ustinov","grey","trevs","south","john snow","mildert","bede","stevo","aidans"]
clubs = ["Klute","klute","jimmies","jimmys","Jimmies","babylon","babs","loft","osbournes"]
positives = ["yes","Yes","positive","Positive"]
negatives = ["No","no","negative","Negative"]

dict = {}
for i in clubs:
    dict[i] = 0

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u200e"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

email = "procreate_antiquely086@simplelogin.com"
password = "qawsedrftg"

with open("./durfess2.txt","w") as file:
    for post in get_posts("durfess", pages=100, timeout=120, credentials=(email,password)):

        time.sleep(2)
        print("New post!")

        text = remove_emojis(post["text"])
        for club in clubs:
            if club in text:
                print("Found club!")
                file.write(text + "\n" +"\n")

                completion = openai.ChatCompletion.create(
                    model="local-model", # this field is currently unused
                    messages=[
                    
                    {"role": "user", "content": f"Is this message positive? {text}"}
                    ],
                    n_ctx=4096,
                    max_tokens=150
                )
                
                res = completion.choices[0].message
                
                for pos in positives:
                    if pos in res:
                        print("Positive :)")
                        dict[club] += 1
                    
                    else:
                        for neg in negatives:
                            if neg in res:
                                print("Negative :(")
                                dict[club] -= 1
print(dict)
file.write(dict)

# {"role": "system", "content": "Always answer in rhymes."},    
# llama.qrt.services:8000/v1
