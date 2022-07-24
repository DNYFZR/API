from fastapi import FastAPI

from typing import Optional
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI()

# Initialise path operator & function
@app.get('/')
async def root():
    return {'Status': 'Active'}

# Path operators function like f-strings
@app.get("/items/{item_id}")
# Data type enforcement can be applied
async def read_item(item_id: str):
    return {"item_id": item_id}

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post('/items/')
async def create_item(item: Item):
    # Extract as python dict
    item_d = item.dict()

    # Update & add parameters automatically
    item_d['name'].capitalize()
    
    if item.description:
        item_d['description'].capitalize()
    
    if item.tax:
        item_d['with_tax'] = item_d['price'] * (1 + item_d['tax'])
    
    return item_d
