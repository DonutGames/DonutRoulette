# -*- coding: utf-8 -*-
import sqlite3


class SQLighter:

    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def check_player(self, chat_id):
        with self.connection:
            player = self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()
            if len(player) == 0:
                return False
            return True

    def insert_new_player(self, chat_id):
        with self.connection:
            self.cursor.execute('INSERT INTO players VALUES(?,?,?,?,?,?,?,?,?)', (chat_id, 100, 0, 0, 0, 0, '', 0, 0))
            self.connection.commit()

    def player_id(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()[0][0]

    def check_balance(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()[0][1]

    def update_balance(self, chat_id, balance):
        with self.connection:
            current_balance = 'UPDATE players SET balance = ? WHERE chat_id = ?'
            self.cursor.execute(current_balance, (balance, chat_id))

    def check_game_flag(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()[0][2]

    def current_bet(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()[0][3]

    def update_current_bet(self, chat_id, chip):
        with self.connection:
            current_bet = self.current_bet(chat_id)
            bet = 'UPDATE players SET current_bet = ? WHERE chat_id = ?'
            self.cursor.execute(bet, (current_bet + chip, chat_id))

    def reset_current_bet(self, chat_id):
        with self.connection:
            bet = 'UPDATE players SET current_bet = ? WHERE chat_id = ?'
            self.cursor.execute(bet, (0, chat_id))
            self.connection.commit()

    def update_flag_up(self, chat_id):
        with self.connection:
            flag = 'UPDATE players SET game_flag = ? WHERE chat_id = ?'
            self.cursor.execute(flag, (1, chat_id))
            self.connection.commit()

    def update_flag_down(self, chat_id):
        with self.connection:
            flag = 'UPDATE players SET game_flag = ? WHERE chat_id = ?'
            self.cursor.execute(flag, (0, chat_id))
            self.connection.commit()

    def choose_bet_msg(self, chat_id):
        with self.connection:
            msg = self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()[0][4]
            if msg > 0:
                return msg
            return

    def update_choose_bet_msg(self, chat_id, msg):
        with self.connection:
            msg_id = 'UPDATE players SET bet_msg_id = ? WHERE chat_id = ?'
            self.cursor.execute(msg_id, (msg, chat_id))
            self.connection.commit()

    def choose_all_bets_msg(self, chat_id):
        with self.connection:
            msg = self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()[0][5]
            if msg > 0:
                return msg
            return

    def update_all_bets_msg(self, chat_id, msg):
        with self.connection:
            msg_id = 'UPDATE players SET all_bets_msg_id = ? WHERE chat_id = ?'
            self.cursor.execute(msg_id, (msg, chat_id))
            self.connection.commit()

    def all_bets(self, chat_id):
        with self.connection:
            s = ''
            a = self.cursor.execute('SELECT * FROM players WHERE chat_id = ? ', (chat_id, )).fetchall()[0][6]
            for x in a.split(','):
                s = s + '\n' + str(x)
            return s[1:]

    def append_data_all_bets(self, chat_id, text):
        with self.connection:
            p = self.all_bets(chat_id)
            if p == '':
                data = text
            else:
                data = p + ',' + str(text)
            bets = 'UPDATE players SET all_bets = ? WHERE chat_id = ?'
            self.cursor.execute(bets, (data, chat_id))
            self.connection.commit()

    def clear_all_bets(self, chat_id):
        with self.connection:
            bets = 'UPDATE players SET all_bets = ? WHERE chat_id = ?'
            self.cursor.execute(bets, (str(), chat_id))

    def choose_make_bet_msg(self, chat_id):
        with self.connection:
            msg = self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()[0][7]
            if msg > 0:
                return msg
            return

    def update_make_bet_msg(self, chat_id, msg):
        with self.connection:
            msg_id = 'UPDATE players SET make_bet_msg_id = ? WHERE chat_id = ?'
            self.cursor.execute(msg_id, (msg, chat_id))
            self.connection.commit()

    def timer(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM players WHERE chat_id = ? ', (chat_id, )).fetchall()[0][8]

    def set_timer(self, chat_id, msg_id):
        with self.connection:
            timer = 'UPDATE players SET timer = ? WHERE chat_id = ?'
            self.cursor.execute(timer, (msg_id, chat_id))

    def close(self):
        self.connection.close()
