from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from api import router
from contextlib import asynccontextmanager
import sqlite3
import pandas as pd
import numpy as np

anime_df = None  # Global variable to hold the anime DataFrame
feature_matrix = None  # Global variable to hold the feature matrix
knn_model = None  # Global variable to hold the KNN model

# We add asynccontextmanager to the FastAPI app to handle the lifespan of the application. 
# This allows us to perform setup and teardown operations when the application starts and stops, respectively. 
# In this case, we are connecting to the SQLite database and reading the anime data into a pandas DataFrame when the application starts.
@asynccontextmanager
async def lifespan(app: FastAPI):
    global anime_df, feature_matrix, knn_model
    
    # Create a connection to the SQLite database
    conn = sqlite3.connect("animes.db")
    anime_df = pd.read_sql_query("SELECT * FROM animes", conn)
    conn.close()
    
    mlb = MultiLabelBinarizer() # Initialize the MultiLabelBinarizer for one-hot encoding of genres and themes
    
    anime_df['genre_names'] = anime_df['genres'].apply(lambda x: [genre['name'] for genre in eval(x)] if pd.notnull(x) else [])
    genre_matrix = mlb.fit_transform(anime_df['genre_names']) # One-hot encode the 'genres' column
    genre_df = pd.DataFrame(genre_matrix, columns=mlb.classes_)
    anime_df = pd.concat([anime_df, genre_df], axis=1)
    
    anime_df['theme_names'] = anime_df['themes'].apply(lambda x: [theme['name'] for theme in eval(x)] if pd.notnull(x) else [])
    theme_matrix = mlb.fit_transform(anime_df['theme_names']) # One-hot encode the 'themes' column
    theme_df = pd.DataFrame(theme_matrix, columns=mlb.classes_)
    anime_df = pd.concat([anime_df, theme_df], axis=1)
    
    # We do this to make sure there are no null values in the 'rating' column, which could cause issues when we try to use this data later on.
    anime_df['age_rating'] = anime_df['rating'].apply(lambda x: x if pd.notnull(x) else 'Unknown')
    age_df = pd.get_dummies(anime_df['age_rating'], prefix='age_rating').astype(int)  # One-hot encode the 'age_rating' column
    anime_df = pd.concat([anime_df, age_df], axis=1)
    
    # Filling in null values for episodes and year with median values to avoid issues with missing data.
    anime_df['episodes'] = anime_df['episodes'].fillna(anime_df['episodes'].median())
    anime_df['year'] = anime_df['year'].fillna(anime_df['year'].median())
    
    # Scaling numeric columns to ensure that they are on a similar scale, which can improve the performance of machine learning models.
    numeric_cols = ['episodes', 'year']
    scaler = StandardScaler()
    numeric_scaled = scaler.fit_transform(anime_df[numeric_cols])
    
    anime_df['year_scaled'] = numeric_scaled[:, 0]
    anime_df['episodes_scaled'] = numeric_scaled[:, 1]
    
    # Sentence Embedding for syposis
    # We use the 'all-MiniLM-L6-v2' model from the sentence-transformers library to generate embeddings for the 'synopsis' column.
    model = SentenceTransformer('all-MiniLM-L6-v2')
    anime_df['synopsis_embedding'] = anime_df['synopsis'].apply(lambda x: model.encode(x if pd.notnull(x) else ""))
    
    numeric_matrix = anime_df[["year_scaled", "episodes_scaled"]].values
    age_matrix = age_df.values
    synopsis_matrix = np.vstack(anime_df["synopsis_embedding"].values)
    
    # Populating the feature matrix with the relevant features for our KNN model. This includes the one-hot encoded genres and themes, the scaled numeric columns, and the synopsis embeddings.
    feature_matrix = np.hstack([
        genre_df.values,
        theme_df.values,
        age_matrix,
        numeric_matrix,
        synopsis_matrix
    ])
    
    knn_model = NearestNeighbors(n_neighbors=25, metric='cosine')  # Initialize the KNN model with cosine distance metric
    knn_model.fit(feature_matrix)
    
    yield  # This is where the application runs. After this point, the application will start serving requests.

# Main file for the FastAPI application. It initializes the FastAPI app and includes the API router.
app = FastAPI(lifespan=lifespan)

app.include_router(router)