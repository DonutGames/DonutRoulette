# -*- coding: utf-8 -*-
import telebot
import utils
import time
import random
from telebot import types
from SQLighter import SQLighter
from config import database_name, token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_command(message):
    base = SQLighter(database_name)
    chat_id = message.chat.id
    base.update_flag_down(chat_id)
    base.reset_current_bet(chat_id)
    if not base.check_player(chat_id):
        base.insert_new_player(chat_id)
        base.close()
    text = '/help - get commands list.'
    bot.send_message(chat_id, text)


@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    text = u"Commands list:" \
           u"\n\n/start - run bot." \
           u"\n/help - get commands list." \
           u"\n/play - play roulette."
    bot.send_message(chat_id, text)


@bot.message_handler(commands=['play'])
def play_command(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    solo_mode = types.InlineKeyboardButton(text='Play solo', callback_data='solo_mode')
    mult_mode = types.InlineKeyboardButton(text='With friends', callback_data='mult_mode')
    keyboard.add(solo_mode, mult_mode)
    bot.send_message(chat_id, 'Choose game mode', reply_markup=keyboard)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def text_query(message):
    chat_id = message.chat.id
    text = message.text
    base = SQLighter(database_name)
    current_bet = base.current_bet(chat_id)
    choose_bet_msg = base.choose_bet_msg(chat_id)
    all_bets_msg = base.choose_all_bets_msg(chat_id)
    make_bet_msg = base.choose_make_bet_msg(chat_id)
    balance = base.check_balance(chat_id)
    if base.check_game_flag(chat_id):
        possible_bets = ['Red', 'Black', '1st 12', '2nd 12', '3rd 12', 'Even', 'Odd', '1 to 18', '19 to 36']
        if text in possible_bets:
            bet = str(current_bet) + '$' + ' on ' + str(text)
            base.append_data_all_bets(chat_id, bet)
            balance = balance - current_bet
            base.reset_current_bet(chat_id)
            current_bet = base.current_bet(chat_id)
            base.update_balance(chat_id, balance)
            balance = base.check_balance(chat_id)
            bot.edit_message_text('Your balance: ' + str(balance) + '$' + '\n'
                                    + 'Your current bet: ' + str(current_bet) + '$',
                                    chat_id, message_id=choose_bet_msg,
                                    reply_markup=utils.solo_mode_bet())

            text = base.all_bets(chat_id)
            bot.edit_message_text('Your bets:' + '\n\n' + text, chat_id, message_id=all_bets_msg)
            bot.delete_message(chat_id, message_id=make_bet_msg)
            bot.delete_message(chat_id, message_id=make_bet_msg+1)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    base = SQLighter(database_name)
    chat_id = call.message.chat.id
    current_bet = base.current_bet(chat_id)
    choose_bet_msg = base.choose_bet_msg(chat_id)
    balance = base.check_balance(chat_id)
    make_bet_msg = base.choose_make_bet_msg(chat_id)

    if call.message:
        if call.data == 'mult_mode':
            utils.solo_reset_all(chat_id)
            bot.send_message(chat_id, 'Sorry, does not work for now')

        elif call.data == 'solo_mode':
            utils.solo_reset_all(chat_id)
            base.update_flag_up(chat_id)
            bot.send_video(chat_id, data='https://i.gifer.com/8C5T.mp4')
            msg = bot.send_message(chat_id,
                                   'Your balance: ' + str(balance) + '$' + '\n'
                                   + 'Your current bet: ' + str(current_bet) + '$',
                                   reply_markup=utils.solo_mode_bet()).message_id

            base.update_choose_bet_msg(chat_id, msg)
            msg = bot.send_message(chat_id, 'Your bets:').message_id
            base.update_all_bets_msg(chat_id, msg)
            msg = bot.send_message(chat_id, 'Make your bets!' + '\n' + '30s left').message_id
            base.set_timer(chat_id, msg)
            timer = base.timer(chat_id)

            def timer_():
                t = 30
                while t != 0:
                    t -= 1
                    time.sleep(1)
                    bot.edit_message_text(str(t) + 's left', chat_id, message_id=timer)
                if t == 0:
                    bot.edit_message_text('Bets are made, there are no bets anymore.', chat_id, message_id=timer)
                    time.sleep(1)
                    bot.edit_message_text('Spinning roulette...', chat_id, message_id=timer)
                    time.sleep(2)
                    num = random.randint(0, 36)
                    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
                    if num in red and num != 0:
                        bot.edit_message_text(str(num) + ' - red!', chat_id, message_id=timer)
                    elif num not in red and num != 0:
                        bot.edit_message_text(str(num) + ' - black!', chat_id, message_id=timer)
                    else:
                        bot.edit_message_text(str(num) + ' - ZERO!', chat_id, message_id=timer)
                    if num != 0:
                        bets = base.all_bets(chat_id).split('\n')
                        win = utils.check_num(str(num), bets)
                        print(win)
                        base.reset_current_bet(chat_id)
                        base.clear_all_bets(chat_id)
                        base.update_balance(chat_id, (base.check_balance(chat_id) + win))
                        balance_ = base.check_balance(chat_id)
                        print(balance_)
                        current_bet_ = base.current_bet(chat_id)
                        choose_bet_msg = base.choose_bet_msg(chat_id)
                        print(choose_bet_msg)
                        bot.edit_message_text('Your balance: ' + str(balance_) + '$' + '\n'
                                              + 'Your current bet: ' + str(current_bet_) + '$',
                                              chat_id, message_id=choose_bet_msg,
                                              reply_markup=utils.solo_mode_bet())
                        text = base.all_bets(chat_id)
                        all_bets_msg = base.choose_all_bets_msg(chat_id)
                        bot.edit_message_text('Your bets:' + '\n\n' + text, chat_id, message_id=all_bets_msg)
                        time.sleep(3)
                return timer_()
            timer_()

        elif call.data == 'choose_bet':
            bot.edit_message_reply_markup(chat_id, message_id=choose_bet_msg,
                                          reply_markup=utils.solo_mode_choose_bet())

        elif call.data == 'bet_1_chip':
            current_bet = base.current_bet(chat_id) + 1
            if balance < current_bet:
                bot.answer_callback_query(call.id, 'You can not raise your bet!')
            else:
                base.update_current_bet(chat_id, 1)
                current_bet = base.current_bet(chat_id)
                bot.edit_message_text('Your balance: ' + str(balance) + '$' + '\n'
                                      + 'Your current bet: ' + str(current_bet) + '$', chat_id,
                                      message_id=choose_bet_msg,
                                      reply_markup=utils.solo_mode_choose_bet())

        elif call.data == 'bet_5_chips':
            current_bet = base.current_bet(chat_id) + 5
            if balance < current_bet:
                bot.answer_callback_query(call.id, 'You can not raise your bet!')
            else:
                base.update_current_bet(chat_id, 5)
                current_bet = base.current_bet(chat_id)
                bot.edit_message_text('Your balance: ' + str(balance) + '$' + '\n'
                                      + 'Your current bet: ' + str(current_bet) + '$', chat_id,
                                      message_id=choose_bet_msg,
                                      reply_markup=utils.solo_mode_choose_bet())

        elif call.data == 'bet_25_chips':
            current_bet = base.current_bet(chat_id) + 25
            if balance < current_bet:
                bot.answer_callback_query(call.id, 'You can not raise your bet!')
            else:
                base.update_current_bet(chat_id, 25)
                current_bet = base.current_bet(chat_id)
                bot.edit_message_text('Your balance: ' + str(balance) + '$' + '\n'
                                      + 'Your current bet: ' + str(current_bet) + '$', chat_id,
                                      message_id=choose_bet_msg,
                                      reply_markup=utils.solo_mode_choose_bet())

        elif call.data == 'bet_50_chips':
            current_bet = base.current_bet(chat_id) + 50
            if balance < current_bet:
                bot.answer_callback_query(call.id, 'You can not raise your bet!')
            else:
                base.update_current_bet(chat_id, 50)
                current_bet = base.current_bet(chat_id)
                bot.edit_message_text('Your balance: ' + str(balance) + '$' + '\n'
                                      + 'Your current bet: ' + str(current_bet) + '$', chat_id,
                                      message_id=choose_bet_msg,
                                      reply_markup=utils.solo_mode_choose_bet())

        elif call.data == 'bet_100_chips':
            current_bet = base.current_bet(chat_id) + 100
            if balance < current_bet:
                bot.answer_callback_query(call.id, 'You can not raise your bet!')
            else:
                base.update_current_bet(chat_id, 100)
                current_bet = base.current_bet(chat_id)
                bot.edit_message_text('Your balance: ' + str(balance) + '$' + '\n'
                                      + 'Your current bet: ' + str(current_bet) + '$', chat_id,
                                      message_id=choose_bet_msg,
                                      reply_markup=utils.solo_mode_choose_bet())

        elif call.data == 'bet_500_chips':
            current_bet = base.current_bet(chat_id) + 500
            if balance < current_bet:
                bot.answer_callback_query(call.id, 'You can not raise your bet!')

            else:
                base.update_current_bet(chat_id, 500)
                current_bet = base.current_bet(chat_id)
                bot.edit_message_text('Your balance: ' + str(balance) + '$' + '\n'
                                      + 'Your current bet: ' + str(current_bet) + '$', chat_id,
                                      message_id=choose_bet_msg,
                                      reply_markup=utils.solo_mode_choose_bet())

        elif call.data == 'back_to_bets':
            bot.edit_message_reply_markup(chat_id,
                                          message_id=choose_bet_msg,
                                          reply_markup=utils.solo_mode_bet())

        elif call.data == 'make_bet':
            if current_bet < 1:
                bot.answer_callback_query(call.id, 'Choose your bet first !')
            else:
                msg = bot.send_message(chat_id, 'Make your bet !',
                                       reply_markup=utils.solo_mode_markup()).message_id
                base.update_make_bet_msg(chat_id, msg)


if __name__ == "__main__":
    bot.polling(none_stop=True)
