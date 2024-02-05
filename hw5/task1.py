# Создать API для получения списка фильмов по жанру. Приложение должно
# иметь возможность получать список фильмов по заданному жанру.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Movie с полями id, title, description и genre.

# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
#  Для этого использовать библиотеку Pydantic.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

movies = []

class Movie(BaseModel):
    id: int
    title: str
    description: str
    genre: str
    status: str

@app.get("/movie/", response_model=Movie)  
async def get_movies(): 
    for movie in movies:
        return movie.title
    return HTTPException(status_code=404, detail="No movies yet")


@app.get("/movie/{genre}/", response_model=Movie)  
async def get_movie(genre: str): 
    for movie in movies:
        if movie.genre == genre:
            return movie.title
    return HTTPException(status_code=404, detail="No movies of this genre")

@app.post("/movie/", response_model=Movie)
async def add_movie(movie: Movie):
    movies.append(movie)
    return movie

@app.put("/movie/{movie_id}", response_model=Movie)
async def update_description(movie_id: int, description: str):
    for i, movie in enumerate(movies):
        if movie.id == movie_id:
            movies[i].description = description
        return movie
    return HTTPException(status_code=404, detail="Movie hasn't been found")

@app.delete("/movie/{movie_id}", response_model=Movie)
async def delete_movie(movie_id: int):
    for i, movie in enumerate(movies):
        if movie.id == movie_id:
            movies[i].status = "deleted"
        return movie
    return HTTPException(status_code=404, detail="Movie hasn't been found")



























