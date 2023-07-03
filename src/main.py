from bson import ObjectId
import motor.motor_asyncio
from typing import Optional ,List
import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import  JSONResponse ,Response
from pydantic import BaseModel,Field

'''
uvicorn  : uvicorn is an ASGI (async server gateway interface) compatible web server for python. (mutipleparalle thread without blocking )
fastapi  : modern web framework for building restfull API 
bson     : format used for data storage and n/w transfer in Mongodb
motor    : async python driver for mongo db
typing   : standard notation for python  . documenting , type checkers iDE 
pydantic : for data modeling/parsing that has efficient error handling. it allows you to define the structure of your data in a declarative way . 
'''

app= FastAPI()
CONNECTION_STRING = "mongodb+srv://vishaljudoka:79pGwBMXf2aZQSTG@cluster0.1o44czu.mongodb.net"
client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
db = client.product

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ItemModel(BaseModel):
    item_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name:str = Field(...)
    price:float = Field(...)
    brand: Optional[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Milk",
                "price": 4.5,
                "brand": "Pil",
            }
        }

class UpdateItemModel(BaseModel):
    name: str = Field(...)
    price: float = Field(...)
    brand: Optional[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Milk",
                "price": 4.5,
                "brand": "Pil",
            }
        }

@app.get("/")
def central_function():
    return {'family' : 'vksh'}

#path parameter
@app.get("/get-item/{item_id}")
async def get_item (item_id: str = Path(description="The item-id you would like to fetch"  )):
    if (item := await db["item"].find_one({"_id": item_id})) is not None:
        return item
    raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,detail="Item does not Exist")

@app.get("/all-item", response_description="List all students", response_model=List[ItemModel])
async def list_items():
    items = await db["item"].find().to_list(1000)
    return items

#querry paramter
@app.get("/get-by-name/{item_id}")
async def get_item (*,item_id : str , name: str = Query(None,title="name" ,description="name of item" ) ):
    if (item := await db["item"].find_one({"name": name})) is not None:
        return item
    raise HTTPException (status_code=404 ,detail="Item name not found")

#post method
@app.post("/create-item/" ,response_description="Add new Item", response_model=ItemModel ,status_code=201)
async def create_item(item : ItemModel = Body(...)):
    item_name = db["item"].find({}, {'name': 1, '_id': 0}).to_list(length=1000)
    name_list = list()
    for dic in await item_name:
        for i in dic :
            name_list.append(dic[i])
    if str(item.name) not in name_list:
        inventory_item = jsonable_encoder(item)
        new_inventory_item = await db["item"].insert_one(inventory_item)
        created_item = await db["item"].find_one({"_id": new_inventory_item.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Item creted successfully")
    else:
        raise HTTPException(status_code=400, detail="Item ID already exist")

@app.put('/update-item/{item_id}')
async def update_item(item_id : str ,item : UpdateItemModel):
    item_update = {k: v for k, v in item.dict().items() if v is not None}

    if len(item_update) >= 1:
        update_result = await db["item"].update_one({"_id": item_id}, {"$set": item_update})

        if update_result.modified_count == 1:
            if (
                    updated_item := await db["item"].find_one({"_id": item_id})
            ) is not None:
                return updated_item

    if (existing_item := await db["item"].find_one({"_id": item_id})) is not None:
        return existing_item

    raise HTTPException(status_code=404, detail=f"Item {id} not found")

@app.delete("/{id}", response_description="Delete")
async def delete_item(item_id: str ):
    delete_result = await db["item"].delete_one({"_id": item_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"product {id} not found")

@app.delete("/delete/{name}", response_description="Delete")
async def delete_item_by_name(name: str ):
    delete_result = await db["item"].delete_one({"name": name})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"product {name} not found")


@app.delete("/delete-price/{price}", response_description="Delete")
async def delete_item_by_name(price: float ):
    delete_result = await db["item"].delete_many({"price": price})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)




if __name__=="__main__":
    uvicorn.run(app ,port=8000 ,host="0.0.0.0" )

# command to run from  local : http://127.0.0.1:8000