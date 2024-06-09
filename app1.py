from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

username = 'your_actual_mysql_username'
password = 'your_actual_mysql_password'
host = 'localhost'
database = 'beaver' 
class ArticleList(Resource):
    def get(self):
        cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        cursor = cnx.cursor()
        
        query = "SELECT id, title FROM articles WHERE is_deleted = FALSE"
        cursor.execute(query)
        articles = cursor.fetchall()
        
        cursor.close()
        cnx.close()
        
        return jsonify(articles)

    def post(self):
        cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        cursor = cnx.cursor()

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('content', type=str, required=True)
        args = parser.parse_args()

        title = args['title']
        content = args['content']

        query = "INSERT INTO articles (title, content, is_deleted) VALUES (%s, %s, FALSE)"
        cursor.execute(query, (title, content))
        cnx.commit()

        cursor.close()
        cnx.close()

        return {'message': 'Article added successfully'}, 201

class Article(Resource):
    def get(self, article_id):
        cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        cursor = cnx.cursor()

        query = "SELECT * FROM articles WHERE id = %s AND is_deleted = FALSE"
        cursor.execute(query, (article_id,))
        article = cursor.fetchone()
        
        cursor.close()
        cnx.close()

        if article:
            return jsonify(article)
        return {'message': 'Article not found'}, 404

    def put(self, article_id):
        cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        cursor = cnx.cursor()

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('content', type=str, required=True)
        args = parser.parse_args()

        title = args['title']
        content = args['content']

        query = "UPDATE articles SET title = %s, content = %s WHERE id = %s AND is_deleted = FALSE"
        cursor.execute(query, (title, content, article_id))
        cnx.commit()

        cursor.close()
        cnx.close()

        return {'message': 'Article updated successfully'}, 200

    def delete(self, article_id):
        cnx = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        cursor = cnx.cursor()

        query = "UPDATE articles SET is_deleted = TRUE WHERE id = %s"
        cursor.execute(query, (article_id,))
        cnx.commit()

        cursor.close()
        cnx.close()

        return {'message': 'Article deleted successfully'}, 200


api.add_resource(ArticleList, '/articles')
api.add_resource(Article, '/articles/<int:article_id>')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
