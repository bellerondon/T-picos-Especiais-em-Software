from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'  # Caminho do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o monitoramento de modificações
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.String(50))
    type = db.Column(db.String(50))
    title = db.Column(db.String(100))
    director = db.Column(db.String(100))
    cast = db.Column(db.String(255))
    country = db.Column(db.String(100))
    date_added = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    rating = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    listed_in = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __repr__(self):
        return f'<Movie {self.title}>'


@app.route('/save_movies')
def save_movies():
    
    df = pd.read_csv('data/Amazon.csv')  

    
    for index, row in df.iterrows():
        movie = Movie(
            show_id=row['show_id'],
            type=row['type'],
            title=row['title'],
            director=row['director'],
            cast=row['cast'],
            country=row['country'],
            date_added=row['date_added'],
            release_year=row['release_year'],
            rating=row['rating'] if pd.notna(row['rating']) else 'N/A',
            duration=row['duration'],
            listed_in=row['listed_in'],
            description=row['description']
        )
        db.session.add(movie)  

    db.session.commit()  
    return jsonify({"message": "Movies saved to database!"})


with app.app_context():
    db.create_all() 


if __name__ == '__main__':
    app.run(debug=True)
