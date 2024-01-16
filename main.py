from fastapi import FastAPI
from server.server import ControlServer
from pydantic import BaseModel


app = FastAPI()

server = ControlServer()

class PublicKey(BaseModel):
    user_name: str
    p:int
    g:int
    h:int
    iNumBits:int

class Mesage(BaseModel):
    sender: str
    receiver: str
    msg: str
    token : str

class GetSomething(BaseModel):
    receiver: str
    token: str

class Verify(BaseModel):
    user_name: str
    number: int


@app.post("/make_login/")
def connection(item:PublicKey):
    res = server.make_login(item.user_name,item)
    return res

@app.post("/send_msg/")
def connection(item:Mesage):
    return server.send_msg(item.sender,item.receiver,item.msg,item.token)

@app.get("/get_msg/")
def connection(item:GetSomething):
    return server.get_msg(item.receiver,item.token)

@app.get("/get_public_key/{who}")
def connection(item:GetSomething,who:str):
    return server.get_public_key(item.receiver,item.token,who)




# @app.post("/connection/")
# def connection(item:PublicKey):
#     res = server.receive_request(item.user_name,item)
#     return res

# @app.post("/verify_number/")
# def connection(item:Verify):
#     res = server.verify_number(item.user_name,item.number)
#     if(res):
#         return {"status":"Adicionado"}
#     else:
#         return {"status":"Recusado"}

# @app.get("/update_msg/{user_name}")
# def connection(user_name:str):
#     print(server.keys_authentication)
#     return server.is_msg(user_name=user_name)
     

# @app.post("/send_msg/")
# def connection(item:Verify):
#     pass