import sqlite3
import random
import logging
import flask_wtf
import wtforms
import datetime


# UserID is '8-digits' + '_' + '8-digits'
# Token length is 128
# Token time format '%a_%H:%M'


# Static
alphanum_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9', '0']
special_char = [' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '`', '+', ',', '-', '.', '/', ':', ';', '<', '>',
                '=', '?', '@', '[', ']', '\\', '^', '_', '~', '{', '}', '|', ]


# Logging initialization
logging.basicConfig(filename='logs\\site_log.log',
                    format='%(asctime)s: %(message)s',
                    datefmt='%y/%m/%d_%H:%M:%S',
                    filemode='w+',
                    level=logging.INFO)
logging.info('Logging initialized')


# Template and form stuff
class BaseData:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.keywords = kwargs.get('keywords', [])
        self.author = kwargs.get('author', '')
        self.keywords_string = ''

    def make_keywords(self):
        num_keywords = len(self.keywords)
        index = 0
        last_index = num_keywords - 1
        while index < num_keywords:
            add_string = self.keywords[index]
            if index != last_index:
                add_string += ', '
            self.keywords_string += add_string
            index += 1


class Link:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class LoginForm(flask_wtf.FlaskForm):
    errors = []
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])
    submit_button = wtforms.SubmitField('Login')


# Sql stuff
def send_sql(sql_string):
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute(sql_string)
    conn.commit()
    cursor.close()
    conn.close()


def query_sql(sql_string):
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute(sql_string)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Account table methods
def write_new_user(user_id, username, password):
    sql_string = 'INSERT INTO ACCOUNTS (USER_ID, USERNAME, PASSWORD)' \
                 ' VALUES ("{}", "{}", "{}");'.format(user_id, username, password)
    send_sql(sql_string)


def valid_login(username, password):
    res = query_sql('SELECT * FROM ACCOUNTS WHERE USERNAME = "{}";'.format(username))
    if len(res) != 1:
        return False
    result = res[0]
    db_username = result[1]
    db_password = result[2]
    if (db_username == username) and (db_password == password):
        return True
    else:
        return False


def get_user_id(username):
    sql_string = 'SELECT * FROM ACCOUNTS WHERE USERNAME = "{}";'.format(username)
    res = query_sql(sql_string)
    if len(res) < 1:
        return None
    row = res[0]
    return row[0]


def get_username(user_id):
    res = query_sql('SELECT * FROM ACCOUNTS WHERE USER_ID = "{}";'.format(user_id))
    row = res[0]
    return row[1]


def account_exists(username):
    res = query_sql('SELECT * FROM ACCOUNTS WHERE USERNAME = "{}";'.format(username))
    if len(res) < 1:
        return False
    else:
        return True


def create_new_account(username, password):
    new_user_id = (rand_generate(4) + '_' + rand_generate(4))
    write_new_user(new_user_id, username, password)
    log_string = 'Created new user: UserID="{}", Username="{}", Password="{}"'.format(new_user_id, username, password)
    logging.info(log_string)


# Login table methods
def token_exists(token):
    res = query_sql('SELECT * FROM LOGIN;')
    exists = False
    for r in res:
        check_token = r[0]
        if token == check_token:
            exists = True
            break
    return exists


def generate_token():
    token = rand_generate(128)
    while token_exists(token):
        token = rand_generate(128)
    return token


def login_user(user_id):
    # Returns token on login
    res = query_sql('SELECT * FROM LOGIN WHERE USER_ID = "{}";'.format(user_id))
    token = generate_token()
    time_now = datetime.datetime.now()
    time_now = time_now.strftime('%Y%m%d_%H:%M:%S')
    if len(res) < 1:
        send_sql('INSERT INTO LOGIN (TOKEN, TIME, USER_ID) VALUES ("{}", "{}", "{}");'.format(token, time_now, user_id))
    else:
        send_sql('UPDATE LOGIN SET TOKEN = "{}", TIME = "{}" WHERE USER_ID = "{}";'.format(token, time_now, user_id))
    logging.info('Login from UserID "{}"'.format(user_id))
    return token


def update_time(token):
    time_now = datetime.datetime.now()
    send_sql('UPDATE LOGIN SET TIME = "{}" WHERE TOKEN = "{}";'.format(time_now, token))


def fetch_user_id(token):
    res = query_sql('SELECT * FROM LOGIN WHERE TOKEN = "{}";'.format(token))
    row = res[0]
    user_id = row[2]
    return user_id


def valid_token(token):
    res = query_sql('SELECT * FROM LOGIN WHERE TOKEN = "{}";'.format(token))
    if len(res) < 1:
        return False
    row = res[0]
    token_time = row[1]
    token_time = datetime.datetime.strptime(token_time, '%Y%m%d_%H:%M:%S')
    time_now = datetime.datetime.now()
    time_diff = time_now - token_time
    login_time = 1800  # time in seconds
    if time_diff.total_seconds() > login_time:
        return False
    else:
        return True


def fetch_username(token):
    res = query_sql('SELECT * FROM LOGIN WHERE TOKEN = "{}";'.format(token))
    if len(res) < 1:
        return None
    row = res[0]
    user_id = row[2]
    username = get_username(user_id)
    return username


def user_link(token):
    # TODO: Link for user account
    username = fetch_username(token)
    link = Link(username, '/')
    return link


# Other
def rand_generate(num_digits, **kwargs):
    allow_special = kwargs.get('allow_special', False)
    allowed_list = []
    allowed_list.extend(alphanum_char)
    if allow_special:
        allowed_list.extend(special_char)
    last_index = len(allowed_list) - 1
    digit_index = 0
    rand_string = ''
    while digit_index < num_digits:
        pick_index = random.randint(0, last_index)
        add_char = allowed_list[pick_index]
        rand_string += add_char
        digit_index += 1
    return rand_string



