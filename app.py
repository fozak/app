from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
import pandas as pd

app = Flask(__name__)

# Initialize an empty DataFrame to hold the posts
posts_df = pd.DataFrame(columns=["id", "title", "content"])

class Post(BaseModel):
    title: str
    content: str

@app.route("/post/", methods=["POST"])
def add_post():
    try:
        post_data = request.json
        post = Post(**post_data)  # Validate and create Post instance
        global posts_df
        new_id = len(posts_df) + 1
        posts_df.loc[new_id] = [new_id, post.title, post.content]  # Using loc for DataFrame
        return jsonify({"message": "Post added!", "post_id": new_id}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@app.route("/get/", methods=["GET"])
def get_posts():
    return jsonify(posts_df.to_dict(orient="records"))

@app.route("/query_posts/", methods=["GET"])
def query_posts():
    title = request.args.get("title", "")
    filtered_posts = posts_df[posts_df['title'].str.contains(title, case=False)]
    return jsonify(filtered_posts.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)