import uvicorn
import mysql.connector 
import json

from typing import Optional


from typing import Optional
from enum import Enum
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


mydb = mysql.connector.connect(
    host="localhost",
    port='3307',
    user="root",
    password="ilovetea",
    database="key_station")
mycursor = mydb.cursor()
    

@app.get("/api/keys/{key_id}")
def key_get(key_id):
    
    mycursor.execute(f'SELECT id,Name,en,Comment FROM key_station.Keys WHERE id = "{key_id}" ')
    restuple = mycursor.fetchall()
    json_dict = {}
    for z in restuple:
        json_dict[z[0]] = ({"id": z[0],"real_name": z[1],"en":z[2],"comment": z[3]})
    json_compatible_item_data = jsonable_encoder(json_dict)
    print(json_compatible_item_data)
    return JSONResponse(content=json_compatible_item_data)

class UserName(BaseModel):
    name: str


@app.post("/api/users/add_user")
def userDelPost(uname:UserName):
    print(type(uname))
    print(uname.name)
    temp = uname.name
    mycursor.execute(f'INSERT INTO key_station.Teachers (FIO,en) VALUES ("{temp}",1);')
    mydb.commit()
    return uname.name

class UserId(BaseModel):
    user_id:int

@app.post("/api/users/del_user")
def userDelPost(uid:UserId):
    print(uid.user_id)
    mycursor.execute(f'DELETE FROM key_station.Teachers WHERE id={uid.user_id};')
    mydb.commit()


    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)


