import uvicorn
from fastapi import FastAPI

from app.model import PostSchema

posts = [
    {
        "id": 1,
        "title": "x-egg",
        "content": "A haburguer with eggs"
    },
    {
        "id": 2,
        "title": "x-salad",
        "content": "A haburguer with lettuce, tomate, onion "
    },
    {
        "id": 3,
        "title": "water",
        "content": "clean water "
    }
]

users = []


app = FastAPI()

# get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

# get posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data" : posts}

# get single post {id}

@app.get("/posts/{id}", tags=[posts])
def get_one_post(id: int):
    if id> len(posts):
        return{
            "error": "Post with ID does not exist"

        }
    for post in posts:
        if post["id"] == id:
            return{
                "data": post
            }

# Post a food to menu

@app.post("/posts", tags= ["posts"])
def add_post(post: PostSchema):
    post.id = len(post) + 1
    posts.append(post.dict())
    return {
        "info":"Post Added!"
    }
