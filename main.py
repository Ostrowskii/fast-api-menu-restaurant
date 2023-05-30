import uvicorn
from fastapi import FastAPI, Body, Depends

from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

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


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

# get posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data" : posts}

# get single post {id}

@app.get("/posts/{id}", tags=["posts"])
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

@app.post("/posts", tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info":"Post Added!"
    }


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }