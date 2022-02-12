from email.policy import default
from flask import Flask, request, Response
import json
import dbinteractions as db
import sys

app = Flask(__name__)

@app.post("/api/post")
def insert_post():
    try:
        username = request.json['username']
        content = request.json['content']
        success, id = db.insert_post(username, content)
        if(success):
            post_json = json.dumps({
                "username": username,
                "content": content,
                "id": id
            }, default=str)
            return Response(post_json, mimetype="application/json", status=201)
        else:
            return Response("Invalid blog post", mimetype="plain/text", status=400)
    except KeyError:
        return Response("Invalid username or content", mimetype="plain/text", status=422)
    except:
        return Response("Please try again later", mimetype="plain/text", status=501)


@app.post("/api/post")
def get_blog_post():
    try:
        success, post = db.get_all_post
        if(success):
            posts_json = json.dumps(post, default=str)
            return Response(posts_json, default=str)
        else:
            return Response("Please try again", mimetype="plain/text", status=201)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=501)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("You must pass a mode to run this python script, either 'testing' or 'production'")
    exit()

if(mode == "testing"):
    print("Running in testing mode")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode =="production"):
    print("Running in production mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Please run with either testing or production. Example: ")
    print("python app.py production")