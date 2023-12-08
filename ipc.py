import threading
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
async def send_dm(bot, msg, send_file = False):
	for guild in bot.guilds:
		member = guild.get_member_named(msg["id"])
		if member != None:
			channel = await member.create_dm()
			if send_file:
				r = requests.get("https://raw.githubusercontent.com/MrRGnome/PayMeBTC/master/client/client.html")
				r.text
				await channel.send(msg["msg"], file=discord.File(r.text, 'PayMeBTC.html'))
			else:
				await channel.send(msg["msg"])
			return

async def listen(bot, og_loop):
	global websocket
	print("Starting IPC Watch")
	if(os.getenv('ENABLE_TIPS') == "1"):
		websocket = connect(os.getenv('TIPS_WEBSOCKET'))
	await asyncio.sleep(5)
	while(1):
		try:
			message = websocket.recv()
			print(f"Received: {message}")
			try:
				msg = json.loads(message)
				if msg["id"] != None and msg["action"] == "registered":
					dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg, True), og_loop)
					dm.result()
				if msg["id"] != None and msg["action"] == "new_invoice":
					dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg), og_loop)
					dm.result()
			except Exception as ex:
				print("IPC processing message error: " + str(ex) + " message: " + message)
		except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK, UnboundLocalError) as ex:
			print("ipc watch fail " + str(ex))
			disconnected = True
			while disconnected:
				await asyncio.sleep(5)
				try:
					websocket = connect(os.getenv('TIPS_WEBSOCKET'))
					disconnected = False
				except Exception as ex:
					print("ipc reconnect fail " + str(ex))
		except Exception as ex:
			print("ipc watch fail " + str(ex))

