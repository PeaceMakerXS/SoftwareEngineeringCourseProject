from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .accounts.controllers.account import account_router


# App initialization
app = FastAPI(swagger_ui_parameters={'syntaxHighlight.theme': 'obsidian'}, openapi_url="/api/account/openapi.json", docs_url="/api/account/docs")
app.include_router(account_router, prefix='/api')

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
