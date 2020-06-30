from flask import *
from data import *


# Create the flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'CZfad0nceTy19H7HoenUvQlNNCxRl4PmuJpkcRu3pb8rincKsMMovAcoPkmwPd2D' \
                           'finW2FPUX39mH8GrZ3U7o746zCtkxW6tcrdGoJ7enZJZjfdb9Mf30VfLE93wFQiU'
nav_links = [
    Link('Home', '/index'),
    Link('About', '/about')
]
no_user = Link('Login', '/login')


# Routes for the urls


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    maybe_token = request.cookies.get('token')
    if valid_token(maybe_token):
        user_tab = user_link(maybe_token)
    else:
        user_tab = no_user
    index_data = BaseData(title='Home',
                          description='Example flask website',
                          keywords=['Flask', 'Example', 'GitHub', 'Cat', 'Website'],
                          author='Badass Cat')
    index_data.make_keywords()
    return render_template('index.html',
                           data=index_data,
                           nav_links=nav_links,
                           user_tab=user_tab)


@app.route('/about', methods=['GET', 'POST'])
def about():
    maybe_token = request.cookies.get('token')
    if valid_token(maybe_token):
        user_tab = user_link(maybe_token)
    else:
        user_tab = no_user
    about_data = BaseData(title='About The Author',
                          description='Badass cat biography',
                          author='Badass Cat')
    return render_template('about.html',
                           data=about_data,
                           nav_links=nav_links,
                           user_tab=user_tab)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_data = BaseData(title='Login',
                          description='Login overlay',
                          author='Badass Cat')
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']
        valid = valid_login(entered_username, entered_password)
        if valid:
            user_id = get_user_id(entered_username)
            login_token = login_user(user_id)
            response = make_response(redirect(url_for('index')))
            response.set_cookie('token', login_token)
            return response
        else:
            error_message = 'Invalid login credentials'
            return render_template('index.html',
                                   data=login_data,
                                   nav_links=nav_links,
                                   login=True,
                                   error=error_message,
                                   user_tab=no_user)
    return render_template('index.html',
                           data=login_data,
                           nav_links=nav_links,
                           login=True,
                           user_tab=no_user)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    create_account_data = BaseData(title='Create Account',
                                   description='Create account overlay',
                                   author='Badass Cat')
    if request.method == 'POST':
        username = request.form['username']
        confirm_username = request.form['confirm_username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        errors = []
        if not username == confirm_username:
            errors.append('Username and confirmation did not match')
        if not password == confirm_password:
            errors.append('Passwords did not match')
        if account_exists(username):
            errors.append('Account with that username already exists')
        if len(errors) == 0:
            create_new_account(username, password)
            return redirect(url_for('index'))
        else:
            error_message = ''
            error_index = 0
            while error_index < (len(errors) - 1):
                error_message += (errors[error_index] + '\n')
            error_message += (errors[(len(errors) - 1)])
            return render_template('index.html',
                                   data=create_account_data,
                                   nav_links=nav_links,
                                   create_account=True,
                                   user_tab=no_user,
                                   error=error_message)
    return render_template('index.html',
                           data=create_account_data,
                           nav_links=nav_links,
                           create_account=True,
                           user_tab=no_user)


# Flask entry point
if __name__ == '__main__':
    app.run()


