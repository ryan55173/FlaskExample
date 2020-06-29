import sqlite3
import random
import logging
import datetime
import flask_wtf
import wtforms


# UserID is '8-digits' + '_' + '8-digits'
# Token length is 128


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


def write_new_user(user_id, username, password):
    sql_string = 'INSERT INTO ACCOUNTS (USER_ID, USERNAME, PASSWORD)' \
                 ' VALUES ("{}", "{}", "{}");'.format(user_id, username, password)
    send_sql(sql_string)
    log_string = 'Created new user: UserID="{}", Username="{}", Password="{}"'.format(user_id, username, password)
    logging.info(log_string)


def write_login(user_id):
    # Get time
    time = datetime.datetime.now()
    time_now = time.strftime('%a_%H:%M:%S')
    token = generate_token()
    # Make token
    sql_string = 'INSERT INTO LOGINS (USER_ID, TIME, TOKEN)' \
                 ' VALUES ("{}", "{}", "{}");'.format(user_id, time_now, token)
    send_sql(sql_string)
    logging.info('Login from user_id: "{}"'.format(user_id))


def token_exists(check_token):
    results = query_sql('SELECT * FROM LOGINS;')
    exists = False
    for r in results:
        if check_token == r[2]:
            exists = True
    return exists


def generate_token():
    token = rand_generate(128)
    while token_exists(token):
        token = rand_generate(128)
    return token


def username_to_user_id(username):
    results = query_sql('SELECT * FROM ACCOUNTS;')
    ret_user_id = None
    for r in results:
        name = r[1]
        user_id = r[0]
        if username == name:
            ret_user_id = user_id
            break
    return ret_user_id


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


def token_to_user_id(token):
    res = query_sql('SELECT * FROM LOGINS WHERE TOKEN = "{}";'.format(token))
    if len(res) < 1:
        return None
    result = res[0]
    user_id = result[0]
    return user_id


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



