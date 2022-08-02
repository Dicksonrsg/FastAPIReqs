from typing import Optional
from fastapi import FastAPI, Path
from uuid import uuid4
from pydantic import BaseModel

#TODO Start the server by running "python3 -m uvicorn myapi:app --reload"

app = FastAPI()

phones = {
    1:{
        "brand":"Redmi",
        "model":"Note 10s",
        "year":"2021",
        "memory":"8gb",
        "storage":"128gb",
        "os":"Android 12",
        "serialNumber": uuid4()
    },
    2:{
        "brand":"Redmi",
        "model":"Note 11",
        "year":"2021",
        "memory":"12gb",
        "storage":"256gb",
        "os":"Android 12",
        "serialNumber": uuid4()
    }    
}

class Phone(BaseModel):
    brand: str
    model: str
    year: int
    memory: str
    storage: str
    os: str
    
class UpdatePhone(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    memory: Optional[str] = None
    storage: Optional[str] = None
    os: Optional[str] = None    

@app.get("/")
def index():
    return {"name": "First API data"}  

@app.get("/getPhoneById/{phoneId}")
def get_phone_by_Id(phoneId: int = Path(None, description="Id of the phone you want to view.", gt=0)):
    return phones[phoneId]

@app.get("/get-By-model")
def get_phone_by_model(model: Optional[str] = None): #Add "Optional[str] = None" to make it optional
    for phone_id in phones:
        if phones[phone_id]["model"] == model:
            return phones[phone_id]
    return {"Data": "Phone not found."}

@app.post("/create-phone/{phone_id}")
def create_phone(phone_id: int, phone: Phone):
    if phone_id in phones:
        return {"Error": "Id already in DB."}
    
    #TODO Add a way to save new phones to SQL DB
    phones[phone_id] = phone
    return phones[phone_id]

@app.put("/update_phone/{phone_id}")
def update_phone(phone_id: int, phone: UpdatePhone):
    if phone_id not in phones:
        return {"Error: Id does not exist in DB."}
    
    if phone.brand != None:
        phones[phone_id].brand = phone.brand

    if phone.model != None:
        phones[phone_id].model = phone.model

    if phone.year != None:
        phones[phone_id].year = phone.year   

    if phone.memory != None:
        phones[phone_id].memory = phone.memory
                
    if phone.storage != None:
        phones[phone_id].storage = phone.storage

    if phone.os != None:
        phones[phone_id].os = phone.os
                        
    return phones[phone_id]

@app.delete("/delete-phone/{phone_id}")
def delete_phone(phone_id: int):
    if phone_id not in phones:
        return {"Error": "Phone does not exist in DB."}
    else:
        del phones[phone_id]
        return{"Message": "Phone deleted."}