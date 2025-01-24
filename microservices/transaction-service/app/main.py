from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .transactions.controllers.transaction import transaction_router


# App initialization
app = FastAPI(swagger_ui_parameters={'syntaxHighlight.theme': 'obsidian'}, openapi_url="/api/transaction/openapi.json", docs_url="/api/transaction/docs")
app.include_router(transaction_router, prefix='/api')

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
