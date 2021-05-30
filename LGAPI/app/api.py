from fastapi import FastAPI, Body, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from app.model import PostSchema, UserSchema, UserLoginSchema, DeviceStatusSchema, DeviceSchema
from app.auth.auth_handler import signJWT, JWT_SECRET, JWT_ALGORITHM
from app.auth.auth_bearer import JWTBearer
import datetime
from typing import Optional
import jwt


posts = []  # DB 대신 쓰는 배열
users = []  # DB 대신 쓰는 배열
deviceDatas = []
devices= []

app = FastAPI()

origins = ["*", "localhost:3000",
           "localhost:8000", "localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "WORKING !!!"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)  # 여기서는 데이터를 그저 배열에 저장할뿐 나중에 DB에 해쉬 해서 저장할것
    return signJWT(user.email)

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Login Failed"
    }


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }

@app.post("/deviceData", tags=["deviceData"])
async def add_data(deviceData: DeviceStatusSchema) -> dict:
    deviceData.id = len(deviceDatas) + 1
    deviceDatas.append(deviceData.dict())
    for device in devices:
        if device["deviceSerial"] == deviceData["deviceSerial"]:
            device["lastStatus"] = deviceData.id
            return {
                "data": "deviceData added."
            }
    return {
        "error": "No such device with that supplied ID."
    }


@app.post("/device", dependencies=[Depends(JWTBearer())], tags=["device"])
async def add_device(device: DeviceSchema) -> dict:
    device.id = len(devices) + 1
    device.lastStatus = 0
    now = datetime.datetime.now()
    nowstr = "%04d%02d%02d" % (now.year, now.month, now.day)
    device.addedDate = nowstr
    devices.append(device.dict())
    return{
        "data": "device added."
    }

@app.get("/device/{id}", dependencies=[Depends(JWTBearer())], tags=["device"])
async def get_single_device(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such device with that supplied ID."
        }

    for device in devices:
        if device["id"] == id:
            return {
                "data": device
            }


@app.get("/device", dependencies=[Depends(JWTBearer())], tags=["device"])
async def get_device_list(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    user_id = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])["user_id"]
    list = []
    organization = ""
    for user in users:
        if user["email"] == user_id:
            organization = user["organization"]
            break
    for device in devices:
        if device["organization"] == organization:
            list.append(device)
    return {
        "data": list
    }

@app.get("/deviceData", dependencies=[Depends(JWTBearer())], tags=["deviceData"])
async def get_deviceData_list(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    user_id = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])["user_id"]
    organization = ""
    list = []
    list2 = []
    for user in users:
        if user["email"] == user_id:
            organization = user["organization"]
            break
    for device in devices:
        if device["organization"] == organization:
            list.append(device["lastStatus"])
    for value in list:
        list2.append(deviceDatas[value - 1])
    return {
        "data": list2
    }