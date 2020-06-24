from flask import *
from data import *


# Create the flask object
app = Flask(__name__)
nav_links = [
    Link('Home', '/index'),
    Link('About', '/about')
]

# Routes for the urls


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    index_data = HeadData(title='Home',
                          description='Example flask website',
                          keywords=['Flask', 'Example', 'GitHub', 'Cat', 'Website'],
                          author='Badass Cat')
    index_data.make_keywords()
    return render_template('index.html',
                           data=index_data,
                           nav_links=nav_links)


@app.route('/about', methods=['GET', 'POST'])
def about():
    about_data = HeadData(title='About Author',
                          description='Badass cat biography',
                          author='Badass Cat')
    return render_template('about.html',
                           data=about_data,
                           nav_links=nav_links)


# Flask entry point
if __name__ == '__main__':
    app.run()


