from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from db import conn, commit
from uvicorn import run

# Definir el modelo Pydantic para los productos
class Product(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

app = FastAPI()

@app.get("/products")
async def get_products():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    products = [{"id": row[0], "name": row[1], "description": row[2], "price": row[3], "quantity": row[4]} for row in rows]
    return products

@app.get("/products/{product_id}")
async def get_product(product_id: int = Path(..., title="The ID of the product to get")):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "name": row[1], "description": row[2], "price": row[3], "quantity": row[4]}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
async def create_product(product: Product):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
                   (product.name, product.description, product.price, product.quantity))
    commit()
    return {"message": "Product created successfully"}

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=%s, description=%s, price=%s, quantity=%s WHERE id=%s",
                   (product.name, product.description, product.price, product.quantity, product_id))
    commit()
    return {"message": "Product updated successfully"}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    commit()
    return {"message": "Product deleted successfully"} 

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8001)
