from channels.generic.websocket import AsyncWebsocketConsumer
from .Global_Variable_Manager import GlobalVariable
import asyncio
from .thread import prog




class ProgressConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        global prog
        await self.accept()
        while prog.get_value() <= 10000:
            await self.send(text_data=str(prog.get_value()))  # Send the current value to the client
            await asyncio.sleep(1)  # Sleep for 1 second to avoid busy-waiting  # noqa: F821
            #if prog.get_value() == 100:
                #await asyncio.sleep(10)
                #prog.set_value(0)
        await self.close()
        
            