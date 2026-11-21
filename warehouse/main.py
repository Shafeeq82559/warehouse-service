from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from warehouse.api import orders, products
from warehouse.errors import DomainError

app = FastAPI(title="Warehouse service")
app.include_router(products.router)
app.include_router(orders.router)


@app.exception_handler(DomainError)
async def handle_domain_error(_: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})
