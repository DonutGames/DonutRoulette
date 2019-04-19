# -*- coding: utf-8 -*-
import SQLighter
from telebot import types
from config import database_name
from SQLighter import SQLighter


def solo_mode_markup():

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    num_btn = types.KeyboardButton(text='Bet on number')
    red_btn = types.KeyboardButton(text='Red')
    black_btn = types.KeyboardButton(text='Black')
    keyboard.add(red_btn, black_btn)

    first_12 = types.KeyboardButton(text='1st 12')
    second_12 = types.KeyboardButton(text='2nd 12')
    third_12 = types.KeyboardButton(text='3rd 12')
    keyboard.add(first_12, second_12, third_12)

    even_btn = types.KeyboardButton(text='Even')
    odd_btn = types.KeyboardButton(text='Odd')
    keyboard.add(even_btn, odd_btn)

    from_19_to_36 = types.KeyboardButton(text='19 to 36')
    from_1_to_18 = types.KeyboardButton(text='1 to 18')
    keyboard.add(from_1_to_18, from_19_to_36)
    return keyboard


def solo_mode_bet():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    make_bet = types.InlineKeyboardButton(text='Choose bet', callback_data='choose_bet')
    cancel_bet = types.InlineKeyboardButton(text='Make bet', callback_data='make_bet')
    keyboard.add(make_bet, cancel_bet)
    return keyboard


def solo_mode_choose_bet():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    bet_1 = types.InlineKeyboardButton(text='1$', callback_data='bet_1_chip')
    bet_5 = types.InlineKeyboardButton(text='5$', callback_data='bet_5_chips')
    bet_25 = types.InlineKeyboardButton(text='25$', callback_data='bet_25_chips')
    keyboard.add(bet_1, bet_5, bet_25)

    bet_50 = types.InlineKeyboardButton(text='50$', callback_data='bet_50_chips')
    bet_100 = types.InlineKeyboardButton(text='100$', callback_data='bet_100_chips')
    bet_500 = types.InlineKeyboardButton(text='500$', callback_data='bet_500_chips')
    keyboard.add(bet_50, bet_100, bet_500)

    back_to_bets = types.InlineKeyboardButton(text='« Back', callback_data='back_to_bets')
    keyboard.add(back_to_bets)
    return keyboard


def solo_reset_all(chat_id):
    base = SQLighter(database_name)
    base.update_flag_down(chat_id)
    base.reset_current_bet(chat_id)
    base.clear_all_bets(chat_id)


def check_num(num, bets):
    num = int(num)
    total_win = 0
    color_flag = ''  # x2
    even_odd_flag = ''  # x2
    every_12_flag = ''  # x3
    half_nums_flag = ''  # x2
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

    if num in red:
        color_flag = 'Red'
    elif num not in red:
        color_flag = 'Black'

    if num < 13:
        every_12_flag = '1st 12'
    elif 12 < num < 25:
        every_12_flag = '2nd 12'
    elif 24 < num < 37:
        every_12_flag = '3rd 12'

    if num % 2 == 0:
        even_odd_flag = 'Even'
    elif num % 2 == 1:
        even_odd_flag = 'Odd'

    if num < 19:
        half_nums_flag = '1 to 18'
    elif 18 < num:
        half_nums_flag = '19 to 36'

    for i in range(len(bets)):
        current_bet = bets[i][:bets[i].find('$')]
        try:
            current_bet = int(current_bet)
        except ValueError:
            current_bet = 0
        if color_flag in bets[i]:
            current_bet *= 2
        elif even_odd_flag in bets[i]:
            current_bet *= 2
        elif half_nums_flag in bets[i]:
            current_bet *= 2
        elif every_12_flag in bets[i]:
            current_bet *= 3
        else:
            current_bet = 0

        total_win += current_bet

    return total_win
