from telegram_token import getToken, getTestToken

import telegram
import random
import time
import enchant
import re
import zhon.pinyin

from itertools import combinations

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, DictPersistence, PicklePersistence
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request

# import requests
from FiveLetterWords import getWord
from Chinese import getChengYu
import logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DEBUG_MODE = False
MAX_ALLOWED_GAMES_RUNNING = 10000
SUPERUSER_ID = 206450254

usDict = enchant.Dict("en_US")
ukDict = enchant.Dict("en_UK")

class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        try:
            result = super(MQBot, self).send_message(*args, **kwargs)
            return result
        except:
            raise

def new_quordle_game(update, context):
    if (update.message == None):
        return

    NUM_CHOSEN_WORDS = 4

    chat_id = update.message.chat_id
    userId = update.message.from_user.id

    isSuperUser = (userId == SUPERUSER_ID)

    modeText = update.message.text
    modeParams = modeText.split()
    try:
        if len(modeParams) == 3:
            codeword = modeParams[1]
            numWords = int(modeParams[2])
            # Experimental mode
            if codeword == "ohcy" and numWords <= 20:
                NUM_CHOSEN_WORDS = numWords
    except:
        pass

    chosenWords = set()
    while (len(chosenWords) < NUM_CHOSEN_WORDS):
        newChosenWord = getWord()
        chosenWords.add(newChosenWord)
    chosenWords = list(chosenWords)
    # print(chosenWords)
    # chosenWord = "Crowd"

    if (chat_id > 0):
        context.bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel! Create a group chat and add this bot to it to play!", parse_mode=telegram.ParseMode.HTML)
        return

    if "runningChatIds" not in context.bot_data:
        context.bot_data["runningChatIds"] = set()

    if "chat_debug_data" not in context.bot_data:
        context.bot_data["chat_debug_data"] = {}

    if "all_chat_data" not in context.bot_data:
        context.bot_data["all_chat_data"] = {}

    if chat_id in context.bot_data["chat_debug_data"]:
        context.bot_data["chat_debug_data"][chat_id]["title"] = update.message.chat.title
        context.bot_data["chat_debug_data"][chat_id]["chosenWords"] = chosenWords
        context.bot_data["chat_debug_data"][chat_id]["hasSuperUser"] |= isSuperUser
        context.bot_data["chat_debug_data"][chat_id]["mode"] = "quordle"
    else:
        context.bot_data["chat_debug_data"][chat_id] = {"title":update.message.chat.title, "chosenWords":chosenWords, "hasSuperUser":isSuperUser, "mode":"quordle"}

    context.bot_data["all_chat_data"][chat_id] = {"chat_data":context.chat_data, "chat_bot":context.bot}

    context.bot_data["runningChatIds"].add(chat_id)

    totalNumGamesRunning = len(context.bot_data["runningChatIds"])
    #print("--------------------------")
    #print("TOTAL GAMES: %d" % totalNumGamesRunning)
    #print("--------------------------")
    if totalNumGamesRunning >= MAX_ALLOWED_GAMES_RUNNING and (not isSuperUser):
        context.bot.send_message(chat_id=chat_id, text="Sorry! We have hit the server limit of %d games running concurrently. Please try again later!" % MAX_ALLOWED_GAMES_RUNNING, parse_mode=telegram.ParseMode.HTML)
        return

    context.chat_data["gameStarted"] = True
    context.chat_data["mode"] = "quordle"
    context.chat_data["letters_remaining"] = [set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(NUM_CHOSEN_WORDS)]
    context.chat_data["letters_correct"] = [set() for i in range(NUM_CHOSEN_WORDS)]
    context.chat_data["chat_id"] = chat_id
    context.chat_data["chosenWords"] = chosenWords
    context.chat_data["foundWordInRound"] = [float('inf') for i in range(NUM_CHOSEN_WORDS)]
    context.chat_data["attempt"] = 0
    context.chat_data["attempt_words"] = [[] for i in range(NUM_CHOSEN_WORDS)]

    if "scores" not in context.chat_data:
        context.chat_data["scores"] = []
    if "scores_cy" not in context.chat_data:
        context.chat_data["scores_cy"] = []
    if "scores_quordle" not in context.chat_data:
        context.chat_data["scores_quordle"] = []

    context.bot.send_message(chat_id=chat_id, text="New game (quordle mode) has begun! Enjoy the extra challenge of solving 4 words over 9 rounds. Type /enter [WORD] to try a word, /help to see what the different font formats mean, /letters to see remaining letters and /stop to end an existing game", parse_mode=telegram.ParseMode.HTML)

    formatStr = ""
    baseFormatStr = "__ __ __ __ __"
    for i in range(NUM_CHOSEN_WORDS // 2):
        formatStr += baseFormatStr + "    " + baseFormatStr + "\n\n"
    if (NUM_CHOSEN_WORDS % 2) > 0:
        formatStr += baseFormatStr
    else:
        formatStr.rstrip("\n")

    context.bot.send_message(chat_id=chat_id, text=formatStr, parse_mode=telegram.ParseMode.HTML)


def new_cy_game(update, context):
    if (update.message == None):
        return

    chat_id = update.message.chat_id
    userId = update.message.from_user.id
    isSuperUser = (userId == SUPERUSER_ID)

    chosenChengYu = getChengYu()
      # ["似懂非懂", ("si", "dong", "fei", "dong"), "To not fully understand"],

    # print(chosenChengYu)

    wordText = chosenChengYu[0] + "(" + " ".join(chosenChengYu[1]) + ")"

    if (chat_id > 0):
        context.bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel! Create a group chat and add this bot to it to play!", parse_mode=telegram.ParseMode.HTML)
        return

    if "runningChatIds" not in context.bot_data:
        context.bot_data["runningChatIds"] = set()

    if "chat_debug_data" not in context.bot_data:
        context.bot_data["chat_debug_data"] = {}

    if "all_chat_data" not in context.bot_data:
        context.bot_data["all_chat_data"] = {}

    if chat_id in context.bot_data["chat_debug_data"]:
        context.bot_data["chat_debug_data"][chat_id]["title"] = update.message.chat.title
        context.bot_data["chat_debug_data"][chat_id]["word"] = wordText
        context.bot_data["chat_debug_data"][chat_id]["hasSuperUser"] |= isSuperUser
        context.bot_data["chat_debug_data"][chat_id]["mode"] = "CY"
    else:
        context.bot_data["chat_debug_data"][chat_id] = {"title":update.message.chat.title, "word":wordText, "hasSuperUser":isSuperUser, "mode": "CY"}

    context.bot_data["all_chat_data"][chat_id] = {"chat_data":context.chat_data, "chat_bot":context.bot}

    context.bot_data["runningChatIds"].add(chat_id)

    totalNumGamesRunning = len(context.bot_data["runningChatIds"])
    # print("--------------------------")
    # print("TOTAL GAMES: %d" % totalNumGamesRunning)
    # print("--------------------------")
    if totalNumGamesRunning >= MAX_ALLOWED_GAMES_RUNNING and (not isSuperUser):
        context.bot.send_message(chat_id=chat_id, text="Sorry! We have hit the server limit of %d games running concurrently. Please try again later!" % MAX_ALLOWED_GAMES_RUNNING, parse_mode=telegram.ParseMode.HTML)
        return

    context.chat_data["gameStarted"] = True
    context.chat_data["mode"] = "CY"
    context.chat_data["letters_remaining"] = [set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(len(chosenChengYu[1]))]
    context.chat_data["letters_correct"] = [set() for i in range(len(chosenChengYu[1]))]
    context.chat_data["chat_id"] = chat_id
    context.chat_data["chengyu"] = chosenChengYu
    context.chat_data["attempt"] = 0
    context.chat_data["attempt_words"] = []
    context.chat_data["underscores"] = ""

    if "scores" not in context.chat_data:
        context.chat_data["scores"] = []
    if "scores_cy" not in context.chat_data:
        context.chat_data["scores_cy"] = []
    if "scores_quordle" not in context.chat_data:
        context.chat_data["scores_quordle"] = []

    context.bot.send_message(chat_id=chat_id, text="New game (成语 Mode) has begun! Type /enter PINYIN to try a 成语 (e.g. /enter shou zhu dai tu), /help to see what the different font formats mean, /letters to see remaining letters and /stop to end an existing game", parse_mode=telegram.ParseMode.HTML)

    clueMessage = ""
    clueMessage += "Clue: %s\n" % chosenChengYu[2]

    pinyins = chosenChengYu[1]
    # ("si", "dong", "fei", "dong")
    underscores = "   ".join([" ".join(["_" for c in word]) for word in pinyins])
    context.chat_data["underscores"] = underscores
    clueMessage += underscores
    context.bot.send_message(chat_id=chat_id, text=clueMessage, parse_mode=telegram.ParseMode.HTML)


def new_game(update, context):

    if (update.message == None):
        return

    chat_id = update.message.chat_id
    userId = update.message.from_user.id

    isSuperUser = (userId == SUPERUSER_ID)

    chosenWord = getWord()
    # chosenWord = "Crowd"
    # print(chosenWord)

    if (chat_id > 0):
        context.bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel! Create a group chat and add this bot to it to play!", parse_mode=telegram.ParseMode.HTML)
        return

    if "runningChatIds" not in context.bot_data:
        context.bot_data["runningChatIds"] = set()

    if "chat_debug_data" not in context.bot_data:
        context.bot_data["chat_debug_data"] = {}

    if "all_chat_data" not in context.bot_data:
        context.bot_data["all_chat_data"] = {}

    if chat_id in context.bot_data["chat_debug_data"]:
        context.bot_data["chat_debug_data"][chat_id]["title"] = update.message.chat.title
        context.bot_data["chat_debug_data"][chat_id]["word"] = chosenWord
        context.bot_data["chat_debug_data"][chat_id]["hasSuperUser"] |= isSuperUser
        context.bot_data["chat_debug_data"][chat_id]["mode"] = "ENG"
    else:
        context.bot_data["chat_debug_data"][chat_id] = {"title":update.message.chat.title, "word":chosenWord, "hasSuperUser":isSuperUser, "mode":"ENG"}

    context.bot_data["all_chat_data"][chat_id] = {"chat_data":context.chat_data, "chat_bot":context.bot}

    context.bot_data["runningChatIds"].add(chat_id)

    totalNumGamesRunning = len(context.bot_data["runningChatIds"])
    #print("--------------------------")
    #print("TOTAL GAMES: %d" % totalNumGamesRunning)
    #print("--------------------------")
    if totalNumGamesRunning >= MAX_ALLOWED_GAMES_RUNNING and (not isSuperUser):
        context.bot.send_message(chat_id=chat_id, text="Sorry! We have hit the server limit of %d games running concurrently. Please try again later!" % MAX_ALLOWED_GAMES_RUNNING, parse_mode=telegram.ParseMode.HTML)
        return

    context.chat_data["gameStarted"] = True
    context.chat_data["mode"] = "ENG"
    context.chat_data["letters_remaining"] = [set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")]
    context.chat_data["letters_correct"] = [set()]
    context.chat_data["chat_id"] = chat_id
    context.chat_data["word"] = chosenWord
    context.chat_data["attempt"] = 0
    context.chat_data["attempt_words"] = []

    if "scores" not in context.chat_data:
        context.chat_data["scores"] = []
    if "scores_cy" not in context.chat_data:
        context.chat_data["scores_cy"] = []
    if "scores_quordle" not in context.chat_data:
        context.chat_data["scores_quordle"] = []

    context.bot.send_message(chat_id=chat_id, text="New game has begun! Type /enter [WORD] to try a word, /help to see what the different font formats mean, /letters to see remaining letters and /stop to end an existing game", parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(chat_id=chat_id, text="__ __ __ __ __", parse_mode=telegram.ParseMode.HTML)


def reset_scores(update, context):
    if (update.message == None):
        return

    chat_id = update.message.chat_id
    chat_bot = context.bot

    if (chat_id > 0):
        chat_bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)
    else:
        context.chat_data["scores"] = []
        context.chat_data["scores_cy"] = []
        context.chat_data["scores_quordle"] = []
        chat_bot.send_message(chat_id=chat_id, text="Round data has been reset!", parse_mode=telegram.ParseMode.HTML)

def print_scores(update, context):
    if (update.message == None):
        return

    chat_id = update.message.chat_id
    chat_bot = context.bot

    if (chat_id > 0):
        chat_bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)

    message = ""
    if ("scores" not in context.chat_data) or (len(context.chat_data["scores"]) == 0):
        message += "You have no historical round data for regular Wordle mode!\n"
    else:
        message += "You managed to find the word on rounds: \n"
        message += " | ".join(context.chat_data["scores"]) + "\n"

    if ("scores_quordle" in context.chat_data) and (len(context.chat_data["scores_quordle"]) != 0):
        message += "\nYou managed to solve the quordle on rounds: \n"
        message += " | ".join(context.chat_data["scores_quordle"]) + "\n"

    if ("scores_cy" in context.chat_data) and (len(context.chat_data["scores_cy"]) != 0):
        message += "\nYou managed to find the 成语 on rounds: \n"
        message += " | ".join(context.chat_data["scores_cy"]) + "\n"

    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def letters_remaining(update, context):
    if (update.message == None):
        return
    chat_id = update.message.chat_id
    chat_bot = context.bot

    if (chat_id > 0):
        chat_bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)

    message = "The [letters remaining] | <b>[seen letters]</b> are: \n\n"
    if not isinstance(context.chat_data["letters_remaining"], list):
        context.chat_data["letters_remaining"] = [context.chat_data["letters_remaining"]]

    numWords = len(context.chat_data["letters_remaining"])
    prefix = ""
    for i in range(numWords):
        if (numWords > 1):
            prefix = "%d) " % (i+1)
            if (context.chat_data["mode"]=="quordle") and (context.chat_data["foundWordInRound"][i] <= context.chat_data["attempt"]):
                continue
        lettersRemaining = list(context.chat_data["letters_remaining"][i])
        lettersRemaining.sort()
        lettersCorrect = list(context.chat_data["letters_correct"][i])
        lettersCorrect.sort()
        if (len(lettersCorrect) > 0):
            message += prefix + " ".join(lettersRemaining) + "  |  " + "<b>" + " ".join(lettersCorrect) + "</b>\n"
        else:
            message += prefix + " ".join(lettersRemaining) + "\n"


    chat_bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def help(update, context):
    if (update.message == None):
        return

    message = "Welcome to the (Unofficial) Telegram Bot Adaptation of <b>Wordle!</b>\n\n"
    message += "You have six guesses to guess a five letter word. Each time you make a guess, the letters will be formatted:\n\n"

    message += "<u>A</u> if the letter is correct and in the right place\n"
    message += "B if the letter is correct and in the wrong place\n"
    message += "<s>C</s> if the letter is not in the word\n\n"


    message += "Commands:\n"
    message += "/new: Make new game\n"
    message += "/new_cy: Make new 成语 game\n"
    message += "/new_q: Make new quordle game\n"
    message += "/stop: Stop current game\n"
    message += "/enter: Enter a word attempt\n"
    message += "/letters: See any remaining letters\n"
    message += "/scores: See which rounds you found the words in\n"
    message += "/reset_scores: Clear your round data\n"
    message += "/help: See game instructions\n"

    message += "\nEmail wavelengthbot@gmail.com if you have any feedback or bug reports!\n"
    # message += "1) Create a group chat\n"
    # message += "2) Add the bot to your group chat\n"
    # message += "3) Type /new to begin a new game\n"
    # message += "4) Type /in to join the game\n"
    # message += "5) After everyone who wants to join the game has typed /in, type /begin to officially start the game!\n\n"
    # message += "<b>Playing the game:</b>\n"
    # message += "1) Every round, one of the players - the <b>Radio Operator</b> - will be give a spectrum (e.g. <b>Cold [0%] ---> Hot [100%]</b>), as well as a signal percentage along that spectrum (e.g. <b>42%</b>)\n"
    # message += "2) That player must now enter a clue in their private chat with the bot that represents the given percentage on that spectrum. For instance, <b>42%</b> on a <b>Cold [0%] ---> Hot [100%]</b> spectrum might be - '<b>cucumber</b>'\n"
    # message += "3) Once their clue is given, every other player submits their guess as to what percentage he was given into their private chat with the bot\n"
    # message += "4) Each person is then given points for how close they got to actual percentage. The Radio Operator is also given points based on the closest match\n"
    # message += "5) (Optional) Add your own binary pairs using the '/add_pair' command for extra fun!\nExample: '/add_pair Bad Bot, Good Bot'\nYou can do this in either the group chat or your private chat with the bot.\n\n"

    # message += "And that's how you play <b>Wavelength</b>! Have fun, think out of the box, and get ready for some spirited debates about whether Tomatoes are more of a fruit or a vegetable 🍅\n"

    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)
    # context.bot.send_message(chat_id=update.message.chat_id, text="If you like this digital implementation of Wavelength, consider getting the actual board game:\nhttps://boardgamegeek.com/boardgame/262543/wavelength", parse_mode=telegram.ParseMode.HTML)

def announce(update, context):

    if (update.message == None):
        return

    chat_id = update.message.chat_id
    userId = update.message.from_user.id
    bot_data = context.bot_data

    isSuperUser = (userId == SUPERUSER_ID)
    if isSuperUser:
        if (chat_id < 0):
            return

        messageData = update.message.text.split(" ", 2)
        if len(messageData) < 3:
            context.bot.send_message(chat_id=userId, text="You need a message! Example: '/announce This is my message'", parse_mode=telegram.ParseMode.HTML)
            return

        try:
            send_chat_id = int(messageData[1])
            message = messageData[2]
        except:
            send_chat_id = 0
            message = messageData[1] + " " + messageData[2]

        removedChatIds = []
        newIdPairs = []
        if ("chat_debug_data" in bot_data):
            for chat_id in bot_data["chat_debug_data"]:
                try:
                    if (send_chat_id == 0 or send_chat_id == chat_id):
                        context.bot.send_message(chat_id=chat_id, text="<b>%s</b>" % message, parse_mode=telegram.ParseMode.HTML)
                except Unauthorized:
                    removedChatIds.append(chat_id)
                except ChatMigrated as e:
                    new_chat_id = e.new_chat_id
                    newIdPairs.append((chat_id, new_chat_id))
                except Exception as e:
                    print (e)

            # Handle update and deletion of new ids
            for chat_id_delete in removedChatIds:
                del bot_data["chat_debug_data"][chat_id_delete]

            for (old_chat_id, new_chat_id) in newIdPairs:
                bot_data["chat_debug_data"][new_chat_id] = bot_data["chat_debug_data"][old_chat_id]
                del bot_data["chat_debug_data"][old_chat_id]


def server_info(update, context):

    if (update.message == None):
        return

    chat_id = update.message.chat_id
    userId = update.message.from_user.id
    bot_data = context.bot_data

    messageOption = None
    messageOptionData = update.message.text.split()
    specificChatId = 0

    if len(messageOptionData) > 1:
        messageOption = messageOptionData[1]

    if len(messageOptionData) > 2 and (messageOption == "info" or messageOption == "leave"):
        try:
            specificChatId = int(messageOptionData[2])
        except:
            specificChatId = 0


    isSuperUser = (userId == SUPERUSER_ID)
    if isSuperUser:
        if (chat_id < 0):
            return

        if ("chat_debug_data" in bot_data):
            if messageOption == "info":
                context.bot.send_message(chat_id=userId, text="Number of groups: %d\nNumber of games running: %d" % (len(bot_data["chat_debug_data"]), len(context.bot_data["runningChatIds"])), parse_mode=telegram.ParseMode.HTML)

                wordText = "Word Data\n---------------\n"
                count = 0
                for chat_id in bot_data["chat_debug_data"]:
                    if (chat_id == specificChatId or specificChatId >= 0):
                        chat_datum = bot_data["chat_debug_data"][chat_id]
                        title = chat_datum["title"]
                        answer = "NIL"
                        if "mode" in chat_datum:
                            if chat_datum["mode"] == "quordle":
                                answer = " | ".join(chat_datum["chosenWords"])
                            else:
                                answer = chat_datum["word"]
                            wordText += "<b>%s</b> chat: <b>%s</b> [%d]\n" % (title, answer, chat_id)
                            count += 1
                            if count > 50:
                                context.bot.send_message(chat_id=userId, text=wordText, parse_mode=telegram.ParseMode.HTML)
                                wordText = ""
                                count = 0
                if wordText != "":
                    context.bot.send_message(chat_id=userId, text=wordText, parse_mode=telegram.ParseMode.HTML)
            elif messageOption == "refresh":
                context.bot_data["runningChatIds"] = set()
                for chat_id in context.bot_data["all_chat_data"]:
                    chat_data = context.bot_data["all_chat_data"][chat_id]["chat_data"]
                    chat_data["gameStarted"] = False
                    context.bot_data["runningChatIds"].add(chat_id)

# *****************************************************************************************
            elif messageOption == "leave":
                leftSuccess = False
                title = "NIL"
                if specificChatId < 0:
                    for chat_id in bot_data["chat_debug_data"]:
                        if chat_id == specificChatId:
                            leftSuccess = context.bot.leave_chat(specificChatId, timeout=None, api_kwargs=None)
                            title = bot_data["chat_debug_data"][chat_id]["title"]
                            del bot_data["chat_debug_data"][specificChatId]
                            break
                    context.bot.send_message(chat_id=userId, text="Attempt to leave Chat %s (%d) = %s" % (title, specificChatId, leftSuccess), parse_mode=telegram.ParseMode.HTML)
                else:
                    context.bot.send_message(chat_id=userId, text="Chat ID %d not found" % specificChatId, parse_mode=telegram.ParseMode.HTML)

# *****************************************************************************************

            elif messageOption == "self":
                context.bot.send_message(chat_id=userId, text="Number of groups: %d\nNumber of games running: %d" % (len(bot_data["chat_debug_data"]), len(context.bot_data["runningChatIds"])), parse_mode=telegram.ParseMode.HTML)
                wordText = ""
                percentageText = "Word Data\n---------------\n"
                for chat_id in bot_data["chat_debug_data"]:
                    chat_datum = bot_data["chat_debug_data"][chat_id]
                    try:
                        if chat_datum["hasSuperUser"]:
                            title = chat_datum["title"]
                            answer = "NIL"
                            if "mode" in chat_datum:
                                if chat_datum["mode"] == "quordle":
                                    answer = " | ".join(chat_datum["chosenWords"])
                                else:
                                    answer = chat_datum["word"]
                            wordText += "<b>%s</b> chat: <b>%s</b>\n" % (title, answer)
                    except:
                        continue

                if len(wordText) > 0:
                    context.bot.send_message(chat_id=userId, text=wordText, parse_mode=telegram.ParseMode.HTML)

def stop(update, context):

    if (update.message == None):
        return

    chat_id = update.message.chat_id
    stopGame(context.chat_data, context.bot_data, update.message.chat_id, context.bot)

def stopGame(chat_data, bot_data, chat_id, chat_bot):

    if (chat_id > 0):
        chat_bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)
        return

    if ("gameStarted" not in chat_data):
        chat_bot.send_message(chat_id=chat_id, text="Type /new to create a new standard Wordle game, /new_cy for 成语 mode or /new_q for an extra challenging Quordle game!", parse_mode=telegram.ParseMode.HTML)
        return

    if chat_id in bot_data["runningChatIds"]:
        bot_data["runningChatIds"].remove(chat_id)

    if chat_id in bot_data["chat_debug_data"]:
        bot_data["chat_debug_data"][chat_id]["word"] = ""

    # Reset data
    chat_data["gameStarted"] = False
    chat_data["word"] = ""
    chat_data["chengyu"] = ""
    chat_data["mode"] = ""

    # bot_data["chat_debug_data"][chat_id]["hasSuperUser"] = False
    chat_bot.send_message(chat_id=chat_id, text="Game ended. Type /new to create a new standard Wordle game, /new_cy for 成语 mode or /new_q for an extra challenging Quordle game!", parse_mode=telegram.ParseMode.HTML)

CORRECT_LETTER_CORRECT_PLACE = 0
CORRECT_LETTER_WRONG_PLACE = 1
WRONG_LETTER_WRONG_PLACE = 2
MAX_ATTEMPTS = 6
MAX_CY_ATTEMPTS = 6

def enterChinese(update, context):

    chat_data = context.chat_data
    user_data = context.user_data
    chat_id = update.message.chat_id
    userId = update.message.from_user.id
    msgText = update.message.text

    msgText = msgText.upper()
    words = msgText.split()

    NUM_WORDS = len(context.chat_data["chengyu"][0])

    if len(words) != (NUM_WORDS+1):
        context.bot.send_message(chat_id=chat_id, text="Please enter only four pinyins", parse_mode=telegram.ParseMode.HTML)
    else:
        chengyuString = " ".join(words[1:])

        if not "".join(words[1:]).isalpha():
            context.bot.send_message(chat_id=chat_id, text="Please ensure your pinyins only have letters [A to Z]", parse_mode=telegram.ParseMode.HTML)
            return

        chengyuParsed = re.findall(zhon.pinyin.syllable, chengyuString, re.IGNORECASE)

        if len(chengyuParsed) != NUM_WORDS:
            context.bot.send_message(chat_id=chat_id, text="Please ensure your chengyu has exactly %d words (pinyins), only %d words detected" % (NUM_WORDS, len(chengyuParsed)), parse_mode=telegram.ParseMode.HTML)
        else:
          # ["似懂非懂", ("si", "dong", "fei", "dong"), "To not fully understand"],

            actualWordsChinese = context.chat_data["chengyu"][0]
            actualWords = context.chat_data["chengyu"][1]
            listAllActualLetters = list("".join(actualWords).strip())
            numAllLetters = len(listAllActualLetters)
            # print(listAllActualLetters)

            meaning = context.chat_data["chengyu"][2]

            numCorrect = 0
            # allOutput = [[] for i in range(NUM_WORDS)]
            allWordsFormatted = []

            for wordIdx in range(NUM_WORDS):
                actualWord = actualWords[wordIdx].upper()
                word = chengyuParsed[wordIdx].upper()
                listActualLetters = list(actualWord)

                # print(actualWord, word)

                if len(word) != len(actualWord):
                    context.bot.send_message(chat_id=chat_id, text="Please ensure your pinyin matches the provided pinyin lengths:\n" + context.chat_data["underscores"], parse_mode=telegram.ParseMode.HTML)
                    return
                else:
                    listLetters = list(word)
                    # output = allOutput[wordIdx]
                    wordFormatted = ""

                    allLettersCorrect = True

                    # Remove all letters that match exactly from pool of "right letter wrong place" letters first
                    for charIdx in range(len(word)):
                        if word[charIdx] == actualWord[charIdx]:
                            listActualLetters.remove(word[charIdx])

                        if word[charIdx] in context.chat_data["letters_remaining"][wordIdx]:
                            context.chat_data["letters_remaining"][wordIdx].remove(word[charIdx])
                        if word[charIdx] in actualWord:
                            context.chat_data["letters_correct"][wordIdx].add(word[charIdx])

                    # Remove all letters that match exactly from pool of "right letter wrong place" letters first
                    for charIdx in range(len(word)):
                        # print(listAllActualLetters, word[i], actualWord[i])
                        if word[charIdx] == actualWord[charIdx]:
                            # output.append((word[charIdx], CORRECT_LETTER_CORRECT_PLACE))
                            wordFormatted += ("<u>" + word[charIdx] + "</u>  ")
                        else:
                            allLettersCorrect = False
                            if word[charIdx] in listActualLetters:
                                listActualLetters.remove(word[charIdx])
                                # output.append((word[charIdx], CORRECT_LETTER_WRONG_PLACE))
                                wordFormatted += (word[charIdx] + "  ")
                            else:
                                # output.append((word[charIdx], WRONG_LETTER_WRONG_PLACE))
                                wordFormatted += ("<s>" + word[charIdx] + "</s>  ")
                                # if word[charIdx] in context.chat_data["letters_remaining"][wordIdx]:
                                #     context.chat_data["letters_remaining"][wordIdx].remove(word[charIdx])

                    if allLettersCorrect:
                        numCorrect += 1

                    allWordsFormatted.append(wordFormatted)

            answerKey = actualWordsChinese + " (" + " ".join(actualWords) + ")"
            if numCorrect == 4:
                context.chat_data["attempt"] += 1
                context.bot.send_message(chat_id=chat_id, text="Correct!! The 成语 is " + answerKey, parse_mode=telegram.ParseMode.HTML)
                context.chat_data["scores_cy"].append(str(context.chat_data["attempt"]))
                stopGame(context.chat_data, context.bot_data, chat_id, context.bot)
            else:
                context.chat_data["attempt"] += 1
                context.chat_data["attempt_words"].append("     ".join(allWordsFormatted))

                message = "-------------------\nAttempt " + str(context.chat_data["attempt"]) + " (" + meaning + "):\n-------------------\n"
                count = 0
                for word_str in context.chat_data["attempt_words"]:
                    message += word_str + "\n"

                context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

                if (context.chat_data["attempt"] == MAX_CY_ATTEMPTS):
                    context.bot.send_message(chat_id=chat_id, text="Last attempt failed. Game Over. The 成语 is: " + answerKey, parse_mode=telegram.ParseMode.HTML)

                    stopGame(context.chat_data, context.bot_data, chat_id, context.bot)
                    context.chat_data["scores_cy"].append("❌")

def enterEnglishQuordle(update, context):

    chat_data = context.chat_data
    user_data = context.user_data
    chat_id = update.message.chat_id
    userId = update.message.from_user.id
    msgText = update.message.text

    words = msgText.split()
    if len(words) != 2:
        context.bot.send_message(chat_id=chat_id, text="Please enter only a single word", parse_mode=telegram.ParseMode.HTML)
    else:
        word = words[1].upper()

        if not word.isalpha():
            context.bot.send_message(chat_id=chat_id, text="Please ensure your word only has letters [A to Z]", parse_mode=telegram.ParseMode.HTML)
        elif len(word) != 5:
            context.bot.send_message(chat_id=chat_id, text="Please ensure your word has exactly 5 letters", parse_mode=telegram.ParseMode.HTML)
        else:
            actualWords = context.chat_data["chosenWords"]
            NUM_CHOSEN_WORDS = len(actualWords)
            ACTUAL_MAX_ATTEMPTS = 5 + NUM_CHOSEN_WORDS

            isReallyLegal = False
            for i in range(NUM_CHOSEN_WORDS):
                actualWord = actualWords[i].upper()
                if (actualWord == word):
                    isReallyLegal = True
                    break

            if not (usDict.check(word) or ukDict.check(word) or isReallyLegal):
                context.bot.send_message(chat_id=chat_id, text="Please ensure your word is actually a word", parse_mode=telegram.ParseMode.HTML)
                return
            else:
                context.chat_data["attempt"] += 1
                for wordIdx in range(NUM_CHOSEN_WORDS):
                    if (context.chat_data["foundWordInRound"][wordIdx] <= context.chat_data["attempt"]):
                        continue

                    actualWord = actualWords[wordIdx].upper()

                    if (actualWord == word):
                        wordFormatted = "<u>" + "  ".join(list(actualWord)) + "</u>"
                        context.chat_data["foundWordInRound"][wordIdx] = context.chat_data["attempt"]
                    else:
                        listActualLetters = list(actualWord)
                        listLetters = list(word)
                        # output = []
                        wordFormatted = ""

                        # Remove all letters that match exactly from pool of "right letter wrong place" letters first
                        for charIdx in range(len(word)):
                            if word[charIdx] == actualWord[charIdx]:
                                listActualLetters.remove(word[charIdx])

                            if word[charIdx] in context.chat_data["letters_remaining"][wordIdx]:
                                context.chat_data["letters_remaining"][wordIdx].remove(word[charIdx])
                            if word[charIdx] in actualWord:
                                context.chat_data["letters_correct"][wordIdx].add(word[charIdx])

                        for i in range(len(word)):
                            # print(listActualLetters, word[i], actualWord[i])
                            if word[i] == actualWord[i]:
                                # output.append((word[i], CORRECT_LETTER_CORRECT_PLACE))
                                wordFormatted += "<u>" + word[i] + "</u>  "
                            else:
                                if word[i] in listActualLetters:
                                    listActualLetters.remove(word[i])
                                    # output.append((word[i], CORRECT_LETTER_WRONG_PLACE))
                                    wordFormatted += word[i] + "  "
                                else:
                                    # output.append((word[i], WRONG_LETTER_WRONG_PLACE))
                                    wordFormatted += "<s>" + word[i] + "</s>  "
                                    # if word[i] in context.chat_data["letters_remaining"][wordIdx]:
                                    #     context.chat_data["letters_remaining"][wordIdx].remove(word[i])

                        wordFormatted = wordFormatted.rstrip()

                    context.chat_data["attempt_words"][wordIdx].append(wordFormatted)

            numCorrect = sum(x <= ACTUAL_MAX_ATTEMPTS for x in context.chat_data["foundWordInRound"])
            if (numCorrect == NUM_CHOSEN_WORDS):
                context.bot.send_message(chat_id=chat_id, text="Correct!! The words are " + " | ".join(actualWords), parse_mode=telegram.ParseMode.HTML)
                context.chat_data["scores_quordle"].append(str(context.chat_data["attempt"]))
                stopGame(context.chat_data, context.bot_data, chat_id, context.bot)
                return
            else:
                message = "-------------------\nAttempt " + str(context.chat_data["attempt"]) + ":\n-------------------\n"
                ALL_CORRECT_PLACEHOLDER = "-------------------"
                count = 0

                wordIdx = 0
                # while wordIdx < range(NUM_CHOSEN_WORDS):
                for wordIdx in range(NUM_CHOSEN_WORDS // 2):
                    attemptWordsLeft = context.chat_data["attempt_words"][wordIdx*2]
                    attemptWordsRight = context.chat_data["attempt_words"][wordIdx*2+1]
                    for wordAttemptIdx in range(context.chat_data["attempt"]):
                        if wordAttemptIdx < context.chat_data["foundWordInRound"][wordIdx*2]:
                            wordStrLeft = attemptWordsLeft[wordAttemptIdx]
                        else:
                            wordStrLeft = ALL_CORRECT_PLACEHOLDER

                        if wordAttemptIdx < context.chat_data["foundWordInRound"][wordIdx*2+1]:
                            wordStrRight = attemptWordsRight[wordAttemptIdx]
                        else:
                            wordStrRight = ALL_CORRECT_PLACEHOLDER
                        message += wordStrLeft + "            " + wordStrRight + "\n"
                        count += 2
                    message += "\n"

                    if count >= 10:
                        count = 0
                        context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)
                        message = ""

                # If odd number, print the last word to the left
                if (NUM_CHOSEN_WORDS % 2 == 1):
                    attemptWords = context.chat_data["attempt_words"][-1]
                    for wordAttemptIdx in range(context.chat_data["attempt"]):
                        if wordAttemptIdx < context.chat_data["foundWordInRound"][-1]:
                            wordStr = attemptWords[wordAttemptIdx]
                        else:
                            wordStrLeft = ALL_CORRECT_PLACEHOLDER
                        message += wordStr + "\n"

                if len(message) > 0:
                    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

                if (context.chat_data["attempt"] == ACTUAL_MAX_ATTEMPTS):
                    context.bot.send_message(chat_id=chat_id, text="Last attempt failed. Game Over. The words were: [" + "  ".join(actualWords) + "]\nType /new to create a new standard Wordle game, /new_cy for 成语 mode or /new_q for an extra challenging Quordle game!", parse_mode=telegram.ParseMode.HTML)

                    stopGame(context.chat_data, context.bot_data, chat_id, context.bot)
                    context.chat_data["scores_quordle"].append("❌")

def enterEnglish(update, context):

    chat_data = context.chat_data
    user_data = context.user_data
    chat_id = update.message.chat_id
    userId = update.message.from_user.id
    msgText = update.message.text

    words = msgText.split()
    if len(words) != 2:
        context.bot.send_message(chat_id=chat_id, text="Please enter only a single word", parse_mode=telegram.ParseMode.HTML)
    else:
        word = words[1].upper()

        if not word.isalpha():
            context.bot.send_message(chat_id=chat_id, text="Please ensure your word only has letters [A to Z]", parse_mode=telegram.ParseMode.HTML)
        elif len(word) != 5:
            context.bot.send_message(chat_id=chat_id, text="Please ensure your word has exactly 5 letters", parse_mode=telegram.ParseMode.HTML)
        else:
            actualWord = context.chat_data["word"].upper()

            if (actualWord == word):
                context.chat_data["attempt"] += 1
                context.bot.send_message(chat_id=chat_id, text="Correct!! The word is " + actualWord, parse_mode=telegram.ParseMode.HTML)
                context.chat_data["scores"].append(str(context.chat_data["attempt"]))
                stopGame(context.chat_data, context.bot_data, chat_id, context.bot)
                return

            elif not (usDict.check(word) or ukDict.check(word)):
                context.bot.send_message(chat_id=chat_id, text="Please ensure your word is actually a word", parse_mode=telegram.ParseMode.HTML)
                return

            else:
                context.chat_data["attempt"] += 1

                listActualLetters = list(actualWord)
                listLetters = list(word)
                # output = []
                wordFormatted = ""

                # Remove all letters that match exactly from pool of "right letter wrong place" letters first
                for charIdx in range(len(word)):
                    if word[charIdx] == actualWord[charIdx]:
                        listActualLetters.remove(word[charIdx])

                    if word[charIdx] in context.chat_data["letters_remaining"][0]:
                        context.chat_data["letters_remaining"][0].remove(word[charIdx])
                    if word[charIdx] in actualWord:
                        context.chat_data["letters_correct"][0].add(word[charIdx])

                for i in range(len(word)):
                    # print(listActualLetters, word[i], actualWord[i])
                    if word[i] == actualWord[i]:
                        # output.append((word[i], CORRECT_LETTER_CORRECT_PLACE))
                        wordFormatted += "<u>" + word[i] + "</u>  "
                    else:
                        if word[i] in listActualLetters:
                            listActualLetters.remove(word[i])
                            # output.append((word[i], CORRECT_LETTER_WRONG_PLACE))
                            wordFormatted += word[i] + "  "
                        else:
                            # output.append((word[i], WRONG_LETTER_WRONG_PLACE))
                            wordFormatted += "<s>" + word[i] + "</s>  "
                            # if word[i] in context.chat_data["letters_remaining"]:
                            #     context.chat_data["letters_remaining"].remove(word[i])

                wordFormatted = wordFormatted.rstrip()
                context.chat_data["attempt_words"].append(wordFormatted)

                message = "-------------------\nAttempt " + str(context.chat_data["attempt"]) + ":\n-------------------\n"
                for word_str in context.chat_data["attempt_words"]:
                    message += word_str + "\n"
                context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

                if (context.chat_data["attempt"] == MAX_ATTEMPTS):
                    context.bot.send_message(chat_id=chat_id, text="Last attempt failed. Game Over. The word was: " + actualWord + "\nType /new to create a new standard Wordle game, /new_cy for 成语 mode or /new_q for an extra challenging Quordle game!", parse_mode=telegram.ParseMode.HTML)

                    stopGame(context.chat_data, context.bot_data, chat_id, context.bot)
                    context.chat_data["scores"].append("❌")


def enter(update, context):

    if (update.message == None):
        return

    chat_data = context.chat_data
    user_data = context.user_data
    chat_id = update.message.chat_id
    userId = update.message.from_user.id
    msgText = update.message.text

    # Reply in the group chat
    if (chat_id < 0):
        if ("gameStarted" in chat_data) and (chat_data["gameStarted"]):
            if (context.chat_data["mode"] == "CY"):
                enterChinese(update,context)
            elif (context.chat_data["mode"] == "quordle"):
                enterEnglishQuordle(update,context)
            else:
                enterEnglish(update,context)
        else:
            context.bot.send_message(chat_id=chat_id, text="Type /new to create a new standard Wordle game, /new_cy for 成语 mode or /new_q for an extra challenging Quordle game!", parse_mode=telegram.ParseMode.HTML)

    # Guarantees that this is private chat with player, rather than a group chat
    elif (chat_id > 0):
        context.bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)

def main():

    # # for test purposes limit global throughput to 18 messages per 1 seconds
    # q = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1017, group_burst_limit=18, group_time_limit_ms = 60000)
    # # set connection pool size for bot
    # request = Request(con_pool_size=8)
    # queued_bot = MQBot(getToken(), request=request, mqueue=q)

    persistence_pickle = PicklePersistence(filename='persistence_pickle')
    # persistence_pickle = DictPersistence()
    # updater = telegram.ext.updater.Updater(bot=queued_bot, use_context=True, persistence=persistence_pickle)

    # updater = Updater(token=getToken(), use_context=True, persistence=persistence_pickle)
    updater = Updater(token=getTestToken(), use_context=True, persistence=persistence_pickle)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('new',new_game))
    dispatcher.add_handler(CommandHandler('new_cy',new_cy_game))
    dispatcher.add_handler(CommandHandler('new_q',new_quordle_game))
    # dispatcher.add_handler(CommandHandler('enter',enter))
    # dispatcher.add_handler(CommandHandler('e',enter))
    dispatcher.add_handler(CommandHandler('help',help))
    dispatcher.add_handler(CommandHandler('letters',letters_remaining))
    dispatcher.add_handler(CommandHandler('enter',enter))
    dispatcher.add_handler(CommandHandler('scores',print_scores))
    dispatcher.add_handler(CommandHandler('reset_scores',reset_scores))

    dispatcher.add_handler(CommandHandler('stop',stop))
    dispatcher.add_handler(CommandHandler('server',server_info))
    dispatcher.add_handler(CommandHandler('announce',announce))

    # dispatcher.add_handler(MessageHandler(Filters.text, enter))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
