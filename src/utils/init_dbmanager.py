
# ------------------ ! Потом убрать
import sys
from pathlib import Path 

sys.path.append(str(Path(__file__).parent.parent.parent))
# ------------------ ! Потом убрать
from src.utils.dbmanager import DBManager
from src.database import async_session_maker
import asyncio

async def get_db() : 
    async with DBManager(session_factory=async_session_maker) as db : 
        yield db

