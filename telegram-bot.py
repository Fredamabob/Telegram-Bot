from twx.botapi import TelegramBot, InputFile, InputFileInfo
import re

bot = TelegramBot('165023625:AAGcL7UPoQQsuYU1wBdt9oF5TCMTnZ6YaQo') # create bot with the given authorization token
bot.update_bot_info().wait() # setup bot

file = open('Pepe_rare.png', 'rb') # open the image file
file_info = InputFileInfo('Pepe_rare.png', file, 'image/png') # instantiate needed file info for Telegram
photo = InputFile('photo', file_info) # instantiate photo in Telegram's InputFile format


def send_meme(message) :
	bot.send_photo(message.chat, photo)
	print "Photo sent"

def command_response(message) :
	if cur_message.text == "/help" :
		bot.send_message(message.chat, "This is a basic telegram bot. This bot will send a photo if \"dank\" is in the message")
	elif cur_message.text == "/about" :
		bot.send_message(message.chat, "This bot is written in Python using a wrapper for the Telegram API written by datamachine")
	else :
		bot.send_message(message.chat, "That is not a command that this bot knows")
	
updates = bot.get_updates(1, None, None).wait() # get first update
if len(updates) == 1 : # account for bot's first update
	current = updates[0]
else :
	current = updates[-1]

dank_pattern = re.compile('(\w\sdank\s\w)|(dank\s\w)|(\w\sdank)|(Dank)')
command_pattern = re.compile('/\w')

while True : # use long polling
	prev = current.update_id
	updates = bot.get_updates(1, None, None).wait() # get next update
	current = updates[-1]
	if prev == current.update_id : # avoid redundant checks of the update by checking previous and current update_id
		continue

	cur_message = current.message # hold current Message object

	if dank_pattern.search(cur_message.text) : # check message for keywords and send photo
		send_meme(cur_message)

	if command_pattern.match(cur_message.text) : # check message for commands
		command_response(cur_message)
		
# TODO:
# 	-add more photos (or ability to grab a random photo
#	-implement command list as dictionary (try to figure out why it is writing all contents of dictionary instead of only value mapped to key)
