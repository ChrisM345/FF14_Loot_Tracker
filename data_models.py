from typing import List, Optional
from pydantic import BaseModel, Field
import csv
import requests



#Currently tracking my character name, loot, and quantity of loot.
class PlayerLoot(BaseModel):
    Name: str = Field(default=None, alias='Name')
    LootName: str = Field(default=None, alias='LootName')
    Quantity: int = Field(default=None, alias='Quantity')


class TotalLoot(BaseModel):
    playerLoot: List[PlayerLoot] = []


class LootMessageModel(BaseModel):
    XivChatType: int = Field(alias="xivChatType")
    LogKind: int = Field(alias="logKind")
    LogKindName: str = Field(alias="logKindName")
    LootMessageType: int = Field(alias="lootMessageType")
    LootMessageTypeName: str = Field(alias="lootMessageTypeName")
    Message: str = Field(alias="message")
    MessageParts: List[str] = Field(alias="messageParts")
    ItemId: int = Field(alias="itemId")
    ItemName: str = Field(alias="itemName")
    IsHq: bool = Field(alias="isHq")

#Convert json into Pydantic model
class KaptureModel(BaseModel):
    Timestamp: int = Field(alias="timestamp")
    LootMessage: LootMessageModel = Field(alias="lootMessage") #Separate this into a second Pydantic model
    LootEventType: int = Field(alias="lootEventType")
    LootEventTypeName: str = Field(alias="lootEventTypeName")
    IsLocalPlayer: bool = Field(alias="isLocalPlayer")
    PlayerName: str = Field(alias="playerName")
    World: str = Field(alias="world")
    Roll: int = Field(alias="roll")
    TerritoryTypeId: int = Field(alias="territoryTypeId")
    ContentId: int = Field(alias="contentId")
    LootEventId: str = Field(alias="lootEventId")
    ItemName: str = Field(alias="itemName")