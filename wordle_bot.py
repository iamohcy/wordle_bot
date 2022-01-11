from telegram_token import getToken

import telegram
import random
import time
import enchant

from itertools import combinations

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, DictPersistence, PicklePersistence
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request

# import requests
from FiveLetterWords import getWord
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


def new_game(update, context):

    if (update.message == None):
        return

    chat_id = update.message.chat_id
    userId = update.message.from_user.id

    isSuperUser = (userId == SUPERUSER_ID)
    chosenWord = getWord()
    # chosenWord = "Crowd"
    print(chosenWord)

    if (chat_id > 0):
        context.bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel! Create a group chat and add this bot to it to play!", parse_mode=telegram.ParseMode.HTML)
        return

    if "runningChatIds" not in context.bot_data:
        context.bot_data["runningChatIds"] = set()

    if "chat_debug_data" not in context.bot_data:
        context.bot_data["chat_debug_data"] = {}

    if "all_chat_data" not in context.bot_data:
        context.bot_data["all_chat_data"] = {}

    context.bot_data["chat_debug_data"][chat_id] = {"title":update.message.chat.title, "word":chosenWord, "hasSuperUser":False}
    context.bot_data["all_chat_data"][chat_id] = {"chat_data":context.chat_data, "chat_bot":context.bot}

    context.bot_data["runningChatIds"].add(chat_id)

    totalNumGamesRunning = len(context.bot_data["runningChatIds"])
    print("--------------------------")
    print("TOTAL GAMES: %d" % totalNumGamesRunning)
    print("--------------------------")
    if totalNumGamesRunning >= MAX_ALLOWED_GAMES_RUNNING and (not isSuperUser):
        context.bot.send_message(chat_id=chat_id, text="Sorry! We have hit the server limit of %d games running concurrently. Please try again later!" % MAX_ALLOWED_GAMES_RUNNING, parse_mode=telegram.ParseMode.HTML)
        return

    context.chat_data["gameStarted"] = True
    context.chat_data["letters_remaining"] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    context.chat_data["chat_id"] = chat_id
    context.chat_data["word"] = chosenWord
    context.chat_data["attempt"] = 0
    context.chat_data["attempt_words"] = []

    if "scores" not in context.chat_data:
        context.chat_data["scores"] = []

    context.bot.send_message(chat_id=chat_id, text="New game has begun! Type /enter [WORD] to try a word, /help to see what the different font formats mean, /letters to see remaining letters and /stop to end an existing game", parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(chat_id=chat_id, text="__ __ __ __ __", parse_mode=telegram.ParseMode.HTML)

    # if (DEBUG_MODE):
    #     context.bot.send_message(chat_id=chat_id, text="For completely new players, please remember to add the bot by clicking @wavelength_test_bot before joining the game!", parse_mode=telegram.ParseMode.HTML)
    # else:
    #     context.bot.send_message(chat_id=chat_id, text="For completely new players, please remember to add the bot by clicking @wavelength_boardgame_bot before joining the game!", parse_mode=telegram.ParseMode.HTML)

    # context.bot.send_message(chat_id=chat_id, text="If you experience any bugs or issues during your use of this bot, feel free to send a message/screenshot describing the error to wavelengthbot@gmail.com", parse_mode=telegram.ParseMode.HTML)

def reset_scores(update, context):
    if (update.message == None):
        return

    chat_id = update.message.chat_id
    chat_bot = context.bot

    if (chat_id > 0):
        chat_bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)
    else:
        context.chat_data["scores"] = []
        chat_bot.send_message(chat_id=chat_id, text="Round data has been reset!", parse_mode=telegram.ParseMode.HTML)

def print_scores(update, context):
    if (update.message == None):
        return

    chat_id = update.message.chat_id
    chat_bot = context.bot

    if (chat_id > 0):
        chat_bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)

    if len(context.chat_data["scores"]) == 0:
        message = "You have no historical round data!\n"
    else:
        message = "You managed to find the word on rounds: \n\n"
        message += " | ".join(context.chat_data["scores"]) + "\n"

    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def letters_remaining(update, context):
    if (update.message == None):
        return
    chat_id = update.message.chat_id
    chat_bot = context.bot

    if (chat_id > 0):
        chat_bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)

    message = "The letters remaining are: \n\n"
    message += " ".join(context.chat_data["letters_remaining"]) + "\n"

    chat_bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def help(update, context):
    if (update.message == None):
        return

    message = "Welcome to the (Unofficial) Telegram Bot Adaptation of <b>Wordle!</b>\n\n"
    message += "You have six guesses to guess a five letter word. Each time you make a guess, the letters will be formatted:\n\n"

    message += "<b><u>A</u></b> if the letter is correct and in the right place\n"
    message += "<b>B</b> if the letter is correct and in the wrong place\n"
    message += "<s>C</s> if the letter is not in the word\n\n"


    message += "Commands:\n"
    message += "/new: Make new game\n"
    message += "/stop: Stop current game\n"
    message += "/enter: Enter a word attempt\n"
    message += "/letters: See any remaining letters\n"
    message += "/scores: See which rounds you found the words in\n"
    message += "/reset_scores: Clear your round data\n"
    message += "/help: See game instructions\n"
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
    if len(messageOptionData) > 1:
        messageOption = messageOptionData[1]

    isSuperUser = (userId == SUPERUSER_ID)
    if isSuperUser:
        if (chat_id < 0):
            return

        if ("chat_debug_data" in bot_data):
            if messageOption == "info":
                context.bot.send_message(chat_id=userId, text="Number of games running: %d" % len(context.bot_data["runningChatIds"]), parse_mode=telegram.ParseMode.HTML)

                wordText = "Word Data\n---------------\n"
                count = 0
                for chat_id in bot_data["chat_debug_data"]:
                    chat_datum = bot_data["chat_debug_data"][chat_id]
                    title = chat_datum["title"]
                    word = chat_datum["word"]

                    wordText += "<b>%s</b> chat: <b>%s</b> [%d]\n" % (title, word, chat_id)
                    if count > 50:
                        context.bot.send_message(chat_id=userId, text=wordText, parse_mode=telegram.ParseMode.HTML)
                        wordText = ""
                if wordText != "":
                    context.bot.send_message(chat_id=userId, text=wordText, parse_mode=telegram.ParseMode.HTML)
            elif messageOption == "update_running":

                context.bot_data["runningChatIds"] = set()
                for chat_id in bot_data["chat_debug_data"]:
                    chat_datum = bot_data["chat_debug_data"][chat_id]
                    word = chat_datum["word"]
                    if len(word) >= 0:
                        context.bot_data["runningChatIds"].add(chat_id)

            elif messageOption == "self":
                context.bot.send_message(chat_id=userId, text="Number of games running: %d" % len(context.bot_data["runningChatIds"]), parse_mode=telegram.ParseMode.HTML)

                percentageText = "Percentage Data\n---------------\n"
                for chat_id in bot_data["chat_debug_data"]:
                    chat_datum = bot_data["chat_debug_data"][chat_id]
                    title = chat_datum["title"]
                    word = chat_datum["word"]

                    try:
                        if chat_datum["hasSuperUser"]:
                            wordText += "<b>%s</b> chat at <b>%d%%</b>\n" % (title, word)
                    except:
                        continue

                context.bot.send_message(chat_id=userId, text=percentageText, parse_mode=telegram.ParseMode.HTML)

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
        chat_bot.send_message(chat_id=chat_id, text="Type /new to create a new game!", parse_mode=telegram.ParseMode.HTML)
        return

    if chat_id in bot_data["runningChatIds"]:
        bot_data["runningChatIds"].remove(chat_id)

    if chat_id in bot_data["chat_debug_data"]:
        bot_data["chat_debug_data"][chat_id]["word"] = ""

    # Reset data
    chat_data["gameStarted"] = False
    chat_data["word"] = ""

    bot_data["chat_debug_data"][chat_id]["hasSuperUser"] = False
    chat_bot.send_message(chat_id=chat_id, text="Game ended. Type /new to create a new game!", parse_mode=telegram.ParseMode.HTML)

CORRECT_LETTER_CORRECT_PLACE = 0
CORRECT_LETTER_WRONG_PLACE = 1
WRONG_LETTER_WRONG_PLACE = 2
MAX_ATTEMPTS = 6

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
            words = msgText.split()
            if len(words) != 2:
                context.bot.send_message(chat_id=chat_id, text="Please enter only a single word", parse_mode=telegram.ParseMode.HTML)
            else:
                word = words[1].upper()

                if not word.isalpha():
                    context.bot.send_message(chat_id=chat_id, text="Please ensure your word only has letters [A to Z]", parse_mode=telegram.ParseMode.HTML)
                elif len(word) != 5:
                    context.bot.send_message(chat_id=chat_id, text="Please ensure your word has exactly 5 letters", parse_mode=telegram.ParseMode.HTML)
                elif not (usDict.check(word) or ukDict.check(word)):
                    context.bot.send_message(chat_id=chat_id, text="Please ensure your word is actually a word", parse_mode=telegram.ParseMode.HTML)
                else:
                    actualWord = context.chat_data["word"].upper()
                    context.chat_data["attempt"] += 1

                    if (actualWord == word):
                        context.bot.send_message(chat_id=chat_id, text="Correct!! The word is " + actualWord, parse_mode=telegram.ParseMode.HTML)
                        context.chat_data["scores"].append(str(context.chat_data["attempt"]))
                        stopGame(context.chat_data, context.bot_data, chat_id, context.bot)

                        return

                    listActualLetters = list(actualWord)
                    listLetters = list(word)
                    output = []
                    wordFormatted = ""

                    # Remove all letters that match exactly from pool of "right letter wrong place" letters first
                    for i in range(len(word)):
                        if word[i] == actualWord[i]:
                            listActualLetters.remove(word[i])

                    for i in range(len(word)):
                        # print(listActualLetters, word[i], actualWord[i])
                        if word[i] == actualWord[i]:
                            output.append((word[i], CORRECT_LETTER_CORRECT_PLACE))
                            wordFormatted += "<b><u>" + word[i] + "</u></b>  "
                        else:
                            if word[i] in listActualLetters:
                                listActualLetters.remove(word[i])
                                output.append((word[i], CORRECT_LETTER_WRONG_PLACE))
                                wordFormatted += "<b>" + word[i] + "</b>  "
                            else:
                                output.append((word[i], WRONG_LETTER_WRONG_PLACE))
                                wordFormatted += "<s>" + word[i] + "</s>  "
                                if word[i] in context.chat_data["letters_remaining"]:
                                    context.chat_data["letters_remaining"].remove(word[i])

                    wordFormatted = wordFormatted.rstrip()
                    context.chat_data["attempt_words"].append(wordFormatted)

                    message = "-------------------\nAttempt " + str(context.chat_data["attempt"]) + ":\n-------------------\n"
                    for word_str in context.chat_data["attempt_words"]:
                        message += word_str + "\n"

                    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

                    if (context.chat_data["attempt"] == MAX_ATTEMPTS):
                        context.bot.send_message(chat_id=chat_id, text="Last attempt failed. Game Over. The word was: " + actualWord + "\nType /new to begin a new round.", parse_mode=telegram.ParseMode.HTML)

                        stopGame(context.chat_data, context.bot_data, chat_id, context.bot)
                        context.chat_data["scores"].append("❌")

                        return

            return
        else:
            context.bot.send_message(chat_id=chat_id, text="Type /new to create a new game!", parse_mode=telegram.ParseMode.HTML)
            return

    # Guarantees that this is private chat with player, rather than a group chat
    elif (chat_id > 0):
        context.bot.send_message(chat_id=chat_id, text="This command can only be sent in a group channel!", parse_mode=telegram.ParseMode.HTML)
        return

def main():

    # # for test purposes limit global throughput to 18 messages per 1 seconds
    # q = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1017, group_burst_limit=18, group_time_limit_ms = 60000)
    # # set connection pool size for bot
    # request = Request(con_pool_size=8)
    # queued_bot = MQBot(getToken(), request=request, mqueue=q)

    persistence_pickle = PicklePersistence(filename='persistence_pickle')
    # persistence_pickle = DictPersistence()
    # updater = telegram.ext.updater.Updater(bot=queued_bot, use_context=True, persistence=persistence_pickle)

    updater = Updater(token=getToken(), use_context=True, persistence=persistence_pickle)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('new',new_game))
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
