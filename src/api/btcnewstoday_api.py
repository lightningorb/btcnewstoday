from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler

import auth_routes
import main_routes
import bounty_routes
import nostr_routes

from fastapi import FastAPI
from limiter import limiter


app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_routes.router)
app.include_router(main_routes.router)
app.include_router(nostr_routes.router)
app.include_router(bounty_routes.router)


origins = ["http://127.0.0.1:5173", "https://btcnews.today", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
