from fastapi import FastAPI, Path, Query
from typing import Optional

app = FastAPI()

# Changed from items to products in path and parameter names
@app.get("/products/{product_id}")
def read_product(
    product_id: int = Path(
        ...,
        title="The ID of the product",
        description="The ID of the product to read",
        gt=0,
    ),
    price: Optional[int] = None
):
    return {"product_id": product_id, "price": price}

# Blog endpoint remains unchanged as it wasn't related to items
@app.get("/blog")
def read_blog(
    search_term: str = Query(
        ...,
        max_length=200,
        min_length=3
    )
):
    if search_term:
        return f"Search term: {search_term}, FOUND!!!"