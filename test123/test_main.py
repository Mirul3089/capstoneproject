import pytest
from httpx import AsyncClient
from json import dumps
from test123.db import pretty_print

from .main123 import app

import warnings
from trio import TrioDeprecationWarning
warnings.filterwarnings(action='ignore', category=TrioDeprecationWarning)

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/select/sp12")
        text=response.json()
        pretty_print(text)
    # assert response.status_code == 200
    #assert response.json() == {"message": "Tomato"}
