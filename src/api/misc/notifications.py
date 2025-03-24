import asyncio
from datetime import datetime

class Notifications:
    
    @staticmethod
    async def notifications() : 
        from src.api import setup
        
        while True : 
            notifications = setup.notifications
            tasks = setup.task_buttons
            current_time = datetime.now("%Y-%m-%d-%M-%S")
            for task in tasks:
                if datetime.strptime(task[4], "%Y-%m-%d-%M-%S") >= current_time : 
                    ...
            asyncio.sleep(60)
            
    @staticmethod
    async def bg_notifications() :
        while True : 
            await asyncio.sleep(5)
            print('ТЕСТ')
        
            
