import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json
from websockets.sync.client import connect
class ipc():
	async def listen(self, bot):
			print("Started IPC Watch")
			with connect(os.getenv('TIPS_WEBSOCKET')) as websocket:
				#websocket.send('{"action":"register", "msg":"please"}')
				while(1):
					try:
						message = await websocket.recv()
						print(f"Received: {message}")
						try:
							msg = json.loads(message)
						except:
							print("IPC Error, not JSON")
							return
					except:
						print("ipc watch fail")
