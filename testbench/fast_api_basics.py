from fastapi import FastAPI
import uvicorn

app = FastAPI()
products = []
# decorator to define a GET endpoint.
# Test the application at http://127.0.0.1:4444/docs
@app.get("/")
async def get_products(): # no asyncio is needed, but it is a good practice to use async def for better performance
    return products

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product.get("id") == product_id:
            return product
    return {"error": "Produkt nicht gefunden"}

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: dict):
    for index, p in enumerate(products): # use index to with product
        if p.get("id") == product_id:
            products[index] = product # update with new product when condition is fullfilled
            return {"success": "Produkt geupdated"}
    return {"error": "Produkt nicht gefunden"} # temporary solution for error handling. In production you should use proper error handling with HTTPException and status codes.

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product.get("id") == product_id:
            products.pop(index) # delete product when condition is fullfilled
            return {"success": "Produkt gelöscht"}
    return {"error": "Produkt nicht gefunden"}

@app.post("/products")
async def create_product(product: dict):
    products.append(product)
    return {"success": "Produkt erstellt"}



# if __name__ == "__main__": # start application when it's main module. Otherwise you have to use the terminal to start the app.
#     uvicorn.run(app, host="127.0.0.1", port=4444)

# run in shell uvicorn fast_api_basics:app --port 4444
