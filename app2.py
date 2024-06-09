from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

app = Flask(__name__)

username = 'root'
password = 'Labit#822'
host = 'localhost'
database = 'blog'

def get_db_connection():
    try:
        cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def fetch_all_articles():
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor()
        query = "SELECT id, title FROM articles WHERE is_deleted = FALSE"
        cursor.execute(query)
        articles = cursor.fetchall()
        cursor.close()
        cnx.close()
        return articles
    return []

def fetch_article(article_id):
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor()
        query = """
        SELECT title, category_name, tags, cover_image, short_description, description, author_name, date_published 
        FROM articles 
        WHERE id = %s AND is_deleted = FALSE
        """
        cursor.execute(query, (article_id,))
        article = cursor.fetchone()
        cursor.close()
        cnx.close()
        return article
    return None

def insert_article(title, category_name, tags, cover_image, short_description, description, author_name, date_published):
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor()
        query = """
        INSERT INTO articles (title, category_name, tags, cover_image, short_description, description, author_name, date_published, is_deleted) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
        """
        cursor.execute(query, (title, category_name, tags, cover_image, short_description, description, author_name, date_published))
        cnx.commit()
        cursor.close()
        cnx.close()

def delete_article(article_id):
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor()
        query = "UPDATE articles SET is_deleted = TRUE WHERE id = %s"
        cursor.execute(query, (article_id,))
        cnx.commit()
        cursor.close()
        cnx.close()

@app.route('/')
def index():
    articles = fetch_all_articles()
    return render_template('index1.html', articles=articles)

@app.route('/articles/<int:article_id>')
def article(article_id):
    article = fetch_article(article_id)
    if article:
        return render_template('new_article1.html', article=article)
    return "Article not found", 404

@app.route('/articles/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    delete_article(article_id)
    return redirect(url_for('index'))

@app.route('/articles/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        category_name = request.form['category_name']
        tags = request.form['tags']
        cover_image = request.form['cover_image']
        short_description = request.form['short_description']
        description = request.form['description']
        author_name = request.form['author_name']
        date_published = request.form['date_published']
        insert_article(title, category_name, tags, cover_image, short_description, description, author_name, date_published)
        return redirect(url_for('index'))
    return render_template('new_article1.html')

if __name__ == '__main__':
    app.run(debug=5000)
