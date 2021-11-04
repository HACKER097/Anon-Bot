import praw
import os
import threading 

import hashlib

from keep_alive import keep_alive

keep_alive()

r = praw.Reddit(client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret"), user_agent="<console:HAPPY:1.0>", password=os.getenv("password"), username=os.getenv("username"))


subreddit = r.subreddit("AnonReddit")

def comment_stream(r, subreddit):
    for comment in subreddit.stream.comments(skip_existing=True):
        if not str(comment.author) == "Anon-Bot":
            body = comment.body
            parent = r.comment(comment.parent_id)
            comment.mod.remove()

            if "||password||" in body:
                body = body.split("||")

                print(body)

                for i in range(len(body)):
                    if body[i] == "password":
                        password = body[i+1]
                        user_hash = hashlib.sha256(bytes(password + str(comment.author) , "utf-8" )).hexdigest()

                        body.pop(i)
                        body.pop(i)

                        break

                body = "USERHASH:" + user_hash + "\n\n" +  " ".join(body)
                body = body[:10000]

            else:
                user_hash = hashlib.sha256(bytes(str(comment.author) + str(random.random()), "utf-8" )).hexdigest()
                body = "USERHASH:" + user_hash + "\n\n" + body

            parent.reply(body)
            comment.author.message("YOUR (u/" + str(comment.author) + ") COMMENT HAS BEEN REMOVED AND POSTED BY u/Anon-Bot", body)



#user_hash = hashlib.sha256(bytes(body[i+1].split("\n")[0] + str(comment.author) , "utf-8" )).hexdigest()


def post_stream(r, subreddit):
    for post in subreddit.stream.submissions(skip_existing=True):
        if not str(post.author) == "Anon-Bot":
            title = post.title
            body = post.selftext

            post.mod.remove()

            if "||password||" in body:
                body = body.split("||")

                print(body)

                for i in range(len(body)):
                    if body[i] == "password":
                        password = body[i+1]
                        user_hash = hashlib.sha256(bytes(password + str(post.author) , "utf-8" )).hexdigest()

                        body.pop(i)
                        body.pop(i)

                        break

                body = "USERHASH:" + user_hash + "\n\n" +  " ".join(body)
                body = body[:10000]

            else:
                user_hash = hashlib.sha256(bytes(str(post.author) + str(random.random()) , "utf-8" )).hexdigest()
                body = "USERHASH:" + user_hash + "\n\n" + body

            subreddit.submit(title, selftext = body)

            reply = "Title:" + title + "\n\n" + "Body:" + body
            reply = reply[:10000]
            post.author.message("YOUR (u/" + str(post.author) + ") POST HAS BEEN REMOVED AND POSTED BY u/Anon-Bot", reply)





comment_thread = threading.Thread(target=comment_stream, args=(r, subreddit,))
post_thread = threading.Thread(target=post_stream, args=(r, subreddit,))

comment_thread.start()
post_thread.start()

while True:
  pass
