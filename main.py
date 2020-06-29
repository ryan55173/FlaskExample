from flask import *
from data import *


# Create the flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'CZfad0nceTy19H7HoenUvQlNNCxRl4PmuJpkcRu3pb8rincKsMMovAcoPkmwPd2Df' \
                           'inW2FPUX39mH8GrZ3U7o746zCtkxW6tcrdGoJ7enZJZjfdb9Mf30VfLE93wFQiU'
nav_links = [
    Link('Home', '/index'),
    Link('About', '/about')
]

# Routes for the urls


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    index_data = BaseData(title='Home',
                          description='Example flask website',
                          keywords=['Flask', 'Example', 'GitHub', 'Cat', 'Website'],
                          author='Badass Cat')
    index_data.make_keywords()
    return render_template('index.html',
                           data=index_data,
                           nav_links=nav_links,
                           user_tab=Link('Login', '/login'))  # TODO: Get if recent login


@app.route('/about', methods=['GET', 'POST'])
def about():
    about_data = BaseData(title='About The Author',
                          description='Badass cat biography',
                          author='Badass Cat')
    return render_template('about.html',
                           data=about_data,
                           nav_links=nav_links,
                           user_tab=Link('Login', '/login'))  # TODO: Get if recent login


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_data = BaseData(title='Login',
                          description='Login overlay',
                          author='Badass Cat')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # TODO: Write cookie and validate with db
    return render_template('index.html',
                           data=login_data,
                           nav_links=nav_links,
                           user_tab=Link('Login', '/login'),  # TODO: Get if recent login
                           login=True,
                           login_form=login_form)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    pass


# Flask entry point
if __name__ == '__main__':
    app.run()


