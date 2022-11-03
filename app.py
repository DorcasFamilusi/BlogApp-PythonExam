from functools import wraps
import MySQLdb
from flask import Flask, render_template,flash,redirect, request, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from data import Articles

app = Flask(__name__)

# Config MySQL DB
app.config ['MYSQL_HOST'] = 'localhost'
app.config ["MYSQL_USER"] = 'root'
app.config ["MYSQL_PASSWORD"] = ''
app.config ["MYSQL_DB"] = 'dorcasity'
app.config ["MYSQL_CURSORCLASS"] = 'DictCursor'

# init MYSQL 
mysql = MySQL(app)


@app.route('/')
def index():
    # Articles
    try:
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM articles")
        articles = cur.fetchall()
        if result > 0:
            return render_template('home.html', articles=articles)
        else:
            msg = 'No articles found'
            return render_template('home.html', msg=msg)
        cur.close()
    except:
        return render_template('home.html', articles=Articles())
    
@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=5, max=40)])
    username = StringField('Username', [validators.Length(min=7, max=30)])
    email = StringField('Email', [validators.Length(min=7, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password does not match')
    ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=7, max=30)])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])

class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=5, max=40)])
    body = TextAreaField('Body', [validators.Length(min=30)])
    author = StringField('Author', [validators.Length(min=5, max=40)])
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data 
        email = form.email.data
        username = form.username.data 
        password = sha256_crypt.hash(str(form.password.data))  
        
        # Creates cursor
        cur = mysql.connection.cursor() 
        
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password)) 
        
        # commit to db 
        mysql.connection.commit()
        
        
        #Close db
        cur.close()
        
        flash('You are now registered and may login. Welcome to BlogIt!', 'success')
        
        redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data 
        password_candidate = form.password.data
        
        # Creates cursor
        cur = mysql.connection.cursor() 
        
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            
            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
            else:
                app.logger.info('PASSWORD NOT MATCHED')
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
        
        flash('You are now logged in. Welcome to Dorcasity!', 'success')

        # set session
        session['logged_in'] = True
        
        redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route("/articles")
def articles():
    try:
        # Create cursor
        cur = mysql.connection.cursor()

        # Get articles
        result = cur.execute("SELECT * FROM articles")

        articles = cur.fetchall()

        if result > 0:
            return render_template('articles.html', articles=articles)
        else:
            msg = 'No articles found'
            return render_template('articles.html', msg=msg)
        # Close connection
        cur.close()
    except:
        return render_template('articles.html', articles=Articles())

@app.route("/article/<string:id>/")
def article(id):
    try:
        # Create cursor
        cur = mysql.connection.cursor()

        # Get article
        result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

        article = cur.fetchone()

        return render_template('article.html', article=article)
    except:
        # get article from dummy data
        article = Articles()[int(id)]
        return render_template('article.html', article=article)

# endpoint to get logged in user details
@app.route('/user', methods=['GET'])
def get_logged_in_user():
    return session['username']

# authenticated decorator
def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated

@app.route("/articles", methods=["POST"])
@authenticated
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data 
        body = form.body.data
        author = form.author.data 
        
        # Creates cursor
        cur = mysql.connection.cursor() 
        
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, author)) 
        
        # commit to db 
        mysql.connection.commit()
        
        
        #Close db
        cur.close()
        
        flash('Article Created', 'success')
        
        redirect(url_for('articles'))

@app.route("/article/<string:id>/edit", methods=["GET", "POST"])
@authenticated
def edit_article(id):
    # Create Cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == "POST" and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", (title, body, id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('articles'))

    return render_template('edit_article.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'Secret145'
    app.run(debug=True)