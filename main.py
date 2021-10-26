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

            if "!pass " in body:
                body = body.split(" ")

                for i in range(len(body)):

                    if body[i] == "!pass":
                        user_hash = hashlib.sha256(bytes(body[i+1] + str(comment.author) , "utf-8" )).hexdigest()

                        body.pop(i)
                        body.pop(i)


                        body = "*USERHASH: " + str(user_hash) + "*" + " \n\n " + " ".join(body)
                        body = body[:10000]

                        break

            parent.reply(body)

def post_stream(r, subreddit):
    for post in subreddit.stream.submissions(skip_existing=True):
        if not str(post.author) == "Anon-Bot":
            title = post.title
            body = post.selftext

            post.mod.remove()

            if "!pass " in body:

                body = body.split(" ")

                for i in range(len(body)):
                    if body[i] == "!pass":
                        user_hash = hashlib.sha256(bytes(body[i+1] + str(post.author) , "utf-8" )).hexdigest()

                        body.pop(i)
                        body.pop(i)


                        body = "*USERHASH: " + str(user_hash) + "*" + " \n\n " + " ".join(body)
                        body = body[:10000]

                        break

            subreddit.submit(title, selftext = body)



comment_thread = threading.Thread(target=comment_stream, args=(r, subreddit,))
post_thread = threading.Thread(target=post_stream, args=(r, subreddit,))

comment_thread.start()
post_thread.start()

while True:
  pass
