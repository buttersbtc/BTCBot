import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json
from websockets.sync.client import connect
import websockets
import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
import io

websocket = None
async def send_dm(bot, id, msg, send_file = False, sendChannel = False):
		member = None
		returnChannel = None
		if sendChannel:
			for guild in bot.guilds:
				for gchannel in guild.channels:
					if gchannel.id == int(id):
						returnChannel = gchannel
		else:
			member = await bot.fetch_user(id)
		if member != None:
			channel = await member.create_dm()
			try:
				if send_file:
					await channel.send(msg, files=send_file)
				else:
					await channel.send(msg)
			except:
				await send_channel(bot, id, msg)
		if returnChannel != None:
			if send_file:
				await returnChannel.send(msg, files=send_file)
			else:
				await returnChannel.send(msg)
				
async def send_channel(bot, id, msg):
	member = await bot.fetch_user(id)
	msg = "You must add this bot as a friend or unblock DM's in order to use the tip features on discord"
	msg = member.mention + " " + msg
	if member != None and os.getenv('TIPS_CHANNEL'):
			for guild in bot.guilds:
				for channel in guild.channels:
					if channel.name == os.getenv('TIPS_CHANNEL'):
						await channel.send(msg)
	

async def listen(bot, og_loop):
	global websocket
	print("Starting IPC Watch")
	if(os.getenv('ENABLE_TIPS') == "1"):
		websocket = connect(os.getenv('TIPS_WEBSOCKET'))
		#there's a race condition here, websocket may not be connected in 5 seconds or may be entirely unavailable regardless. It will try again.
		await asyncio.sleep(5)
		while(1):
			try:
				message = websocket.recv()
				print(f"Received: {message}")
				try:
					msg = json.loads(message)
					if not "id" in msg and not "action" in msg:
						print("Invalid message missing id and action fields")
						continue
					if msg["action"] == "registered":
						dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["id"], msg["msg"]), og_loop).result()
					elif "requestId" in msg and "amount" in msg and msg["action"] == "user_unregistered":
						await user_unregistered(msg, bot, og_loop)
					elif "amount" in msg and msg["action"] == "user_offline":
						await user_offline(msg, bot, og_loop)
					elif "amount" in msg and ("data" in msg or "btcAddress" in msg) and msg["action"] == "new_invoice":
						await new_invoice(msg, bot, og_loop)
					elif "requestId" in msg and msg["action"] == "staticBTC":
						await static_btc(msg, bot, og_loop)
					elif "msg" in msg:
						dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["id"], msg["msg"]), og_loop).result()
				except Exception as ex:
					print("IPC processing message error on line " + str(sys.exc_info()[-1].tb_lineno) + ": " + str(ex) + " message: " + message)
			except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK, UnboundLocalError) as ex:
				print("ipc watch failure " + str(ex))
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


async def new_invoice(msg, bot, og_loop):
	receiver = asyncio.run_coroutine_threadsafe(bot.fetch_user(msg["id"]), og_loop).result()
	bufList :list[discord.File] = []
	msg1 = "To tip " + receiver.name + " "
	if msg["amount"] != 0:
		msg1 += str(msg["amount"]) + " satoshi "
	msg1 += "scan or paste the following "
	if "data" in msg:
		msg1 += "lightning invoice in your lightning wallet: **" + msg["data"] + "** "
		qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
		qr.add_data(msg["data"])
		img1 = qr.make_image(image_factory=StyledPilImage, embeded_image_path=os.path.join("images","Bitcoin_lightning_logo.png"))
		buf1 = io.BytesIO()
		img1.save(buf1)
		buf1.seek(0)
		file1 = discord.File(buf1, "invoice.png")
		bufList.append(file1)
	if "data" in msg and "btc" in msg:
		msg1 += "or "
	if "btc" in msg:
		msg1 += "bitcoin address in your bitcoin wallet: **" + msg["btcAddress"] + "** "
		qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
		qr.add_data(msg["btcAddress"])
		img2 = qr.make_image(image_factory=StyledPilImage, embeded_image_path=os.path.join("images","Bitcoin_logo.png"))
		buf2 = io.BytesIO()
		img2.save(buf2)
		buf2.seek(0)
		file2 = discord.File(buf2, "btc.png")
		bufList.append(file2)
	if "channel" in msg:
		dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["channel"], msg1, bufList, True), og_loop).result()
	else:
		dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["requestId"], msg1, bufList), og_loop).result()

async def user_offline(msg, bot, og_loop):
	sender = asyncio.run_coroutine_threadsafe(bot.fetch_user(msg["requestId"]), og_loop).result()
	receiver = asyncio.run_coroutine_threadsafe(bot.fetch_user(msg["id"]), og_loop).result()
	msg1 = receiver.name + " is offline and unable to respond, but we've sent them a message reminding them to come back online and queued your tip request until they do."
	msg2 = sender.name + " is trying to send you " + str(msg["amount"]) + " satoshi but can't because your PayMeBTC server is offline. Please restart PayMeBTC.html or re-register with the  `" + os.getenv('BOT_PREFIX') + "register` command."
	dm1 = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["requestId"], msg1), og_loop).result()
	dm2 = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["id"], msg2), og_loop).result()
	if "channel" in msg:
		dm3 = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["channel"], msg1, True), og_loop).result()

async def user_unregistered(msg, bot, og_loop):
	sender = asyncio.run_coroutine_threadsafe(bot.fetch_user(msg["requestId"]), og_loop).result()
	receiver = asyncio.run_coroutine_threadsafe(bot.fetch_user(msg["id"]), og_loop).result()
	msg1 = receiver.name + " is not currently registered using the `" + os.getenv('BOT_PREFIX') + "register` command on the PayMeBTC Bitcoin tip bot. We have sent them a DM letting them know you are trying to tip them."
	msg2 = sender.name + " is trying to tip you " + str(msg["amount"]) + " satoshi but they can't because you have not registered on the Bitcoin Discord tip bot. Type `" + os.getenv('BOT_PREFIX') + "register` to begin. The tip bot is non-custodial, self hosted, and interfaces with your lightning node. When you register you'll be given a link and setup instructions. You can verify this bot and DM by comparing its user ID to the user ID of BitcoinChat on the Bitcoin discord at <https://bitcointech.help>"
	dm1 = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["requestId"], msg1), og_loop).result()
	dm2 = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["id"], msg2), og_loop).result()
	if "channel" in msg:
		dm3 = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["channel"], msg1, True), og_loop).result()

async def static_btc(msg, bot, og_loop):
	receiver = asyncio.run_coroutine_threadsafe(bot.fetch_user(msg["id"]), og_loop).result()
	msg1 = receiver.name + " is offline and unable to respond, but they have a static Bitcoin address available to send funds to and we've queued a request for a lightning invoice when they come back online. Bitcoin address for " + receiver.name + ": **" + msg['staticBTC'] + "**"
	qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
	qr.add_data(msg["staticBTC"])
	img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=os.path.join("images","Bitcoin_logo.png"))
	buf = io.BytesIO()
	img.save(buf)
	buf.seek(0)
	file = discord.File(buf, "btc.png")
	if "channel" in msg:
		dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["channel"], msg1, [file], True), og_loop).result()
	else:
		dm = asyncio.run_coroutine_threadsafe(send_dm(bot, msg["requestId"], msg1, [file]), og_loop).result()