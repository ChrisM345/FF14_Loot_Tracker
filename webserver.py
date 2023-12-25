from fastapi import FastAPI, HTTPException
import uvicorn
from data_models import *
from typing import List
from loot_tracker import trackLoot

#TotalLoot is a Pydantic Model that currently tracks List[PlayerLoot] which is Name, LootName, Quantity.
loot = TotalLoot() 

#FastAPI to create server and read json
def create_app() -> FastAPI:
    app = FastAPI()
    return app

app = create_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#Manually shutdown server once all data is obtained and call trackLoot to start acting on it.
@app.on_event("shutdown")
def shutdown_event():
    trackLoot(loot)

#Reads json from the loot tracker plug-in in FF14
@app.post("/", tags=["upload"])
async def upload(data_array: List[KaptureModel]):
    for data in data_array:
        #only care about salvage
        if data.LootMessage.ItemId in [22500,22501,22502,22503,22504,22505,22506,22507]:
            #append only the data I want using the PlayerLoot model.
            loot.playerLoot.append(PlayerLoot.model_validate({
                "Name":data.PlayerName,
                "LootName":data.ItemName,
                "Quantity": 1
                if not data.LootMessage.MessageParts[0].split(" ")[2].isdigit()
                else int(data.LootMessage.MessageParts[0].split(" ")[2])
        }))

if __name__ == '__main__':
    uvicorn.run("webserver:app", host="localhost", port=5000)