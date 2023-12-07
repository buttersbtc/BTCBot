import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json
from websockets.sync.client import connect
import websockets

websocket = None

async def listen(bot):
		global websocket
		print("Starting IPC Watch in 5 seconds")
		if(os.getenv('ENABLE_TIPS') == "1"):
			websocket = connect(os.getenv('TIPS_WEBSOCKET'))
		await asyncio.sleep(5)

		#websocket.send('{"action":"register", "msg":"please"}')
		while(1):
			try:
				message = websocket.recv()
				print(f"Received: {message}")
				try:
					msg = json.loads(message)
				except:
					print("IPC Error, not JSON")
					return
			except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK, UnboundLocalError) as ex:
				print("ipc watch fail " + str(ex))
				disconnected = True
				while disconnected:
					await asyncio.sleep(5)
					websocket = connect(os.getenv('TIPS_WEBSOCKET'))
					disconnected = False
			#except Exception as ex:
				#print("ipc watch fail " + str(ex))

