from fastapi import APIRouter, status, Query, Path
from schemas.Book import Book
from json import load, dump
from fastapi.responses import JSONResponse
from operator import itemgetter
from utils.logger import logger
from uuid import uuid1, UUID

book_router = APIRouter(prefix='/books', tags=['books'])


@book_router.get('')
async def get_books():
    ''' ENDPOINT GET ALL BOOKS '''

    with open('data/db.json', 'r', encoding='utf-8') as jsonfile:
        data = load(jsonfile)
        books = data['books']
        if books is None:
            return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=books, status_code=status.HTTP_200_OK)


@book_router.get('/{uid}')
async def get_book_by_id(uid: UUID = Path(min_length=10)):
    ''' ENDPOINT GET BOOK BY UNIQUE ID'''

    with open('data/db.json', 'r', encoding='utf-8') as jsonfile:
        data = load(jsonfile)
        books = data['books']
        for book in books:
            if book['id'] == str(uid):
                return JSONResponse(content=book, status_code=status.HTTP_200_OK)
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)


@book_router.get('/')
async def get_book_by_title(title: str = Query(min_length=5, max_length=20)):
    ''' ENDPOINT GET BOOK BY TITLE '''

    with open('data/db.json', 'r', encoding='utf-8') as jsonfile:
        data = load(jsonfile)
        books = data['books']

    result = list(filter(lambda book: book if title.lower()
                  in book['title'].lower() else False, books))
    if len(result) == 0:
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@book_router.post('/create')
async def create_book(book: Book):
    ''' ENDPOINT CREATE NEW BOOK '''

    title, category, release_date, authors = itemgetter(
        "title", "category", "release_date", "authors")(book.model_dump())

    authors_validation = []

    with open("data/db.json", "r", encoding="utf-8") as jsonfile:
        data = load(jsonfile)

        for author in authors:
            authors_validation = [
                db_author for db_author in data["authors"] if author["id"] == db_author["id"]]

    if len(authors_validation) == 0:
        return JSONResponse(
            content={
                'message': 'El id proporcionado no pertenece a ninguno de los autores.'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    ''' BOOK MODEL '''
    new_book = {
        "id": str(uuid1()),
        "title": title,
        "category": category,
        "release_date": release_date,
        "authors": authors
    }

    data["books"].append(new_book)

    with open('data/db.json', 'w', encoding='utf-8') as file:
        dump(data, file, indent=2)
    return JSONResponse(content={'message': 'El libro se ha creado exitosamente.'}, status_code=status.HTTP_201_CREATED)


@book_router.put('/{uid}')
async def update_book_by_id(uid: UUID, book: Book):
    ''' ENDPOINT UPDATE BOOK BY UNIQUE ID '''

    title, category, release_date, authors = itemgetter(
        'title', 'category', 'release_date', 'authors')(book.model_dump())

    authors_validation = []
    valid_book = []

    with open('data/db.json', 'r', encoding='utf-8') as jsonfile:
        data = load(jsonfile)

        valid_book = [book for book in data["books"] if book["id"] == str(uid)]

        for author in authors:
            authors_validation = [
                db_author for db_author in data['authors'] if author['id'] == db_author['id']]

    if len(authors_validation) == 0:
        return JSONResponse(
            content={
                'message': 'El id proporcionado no pertenece a ninguno de los autores.'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif len(valid_book) == 0:
        return JSONResponse(content={"message": "Libro no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    for book in data['books']:
        if book['id'] == str(uid):
            book['title'] = title
            book['category'] = category
            book['release_date'] = release_date
            book['authors'] = authors

    with open('data/db.json', 'w', encoding='utf-8') as file:
        dump(data, file, indent=2)
    return JSONResponse(content={'message': f'Libro actualizado con exito'}, status_code=status.HTTP_200_OK)


@book_router.delete('/{uid}')
async def delete_book(uid: UUID = Path(min_length=10)):
    ''' ENDPOINT DELETE BOOK BY UNIQUE ID'''

    with open('data/db.json', 'r', encoding='utf-8') as jsonfile:
        data = load(jsonfile)
        books = data['books']

    result = [book for book in books if book['id'] != str(uid)]
    data['books'] = result

    with open('data/db.json', 'w', encoding='utf-8') as file:
        dump(data, file, indent=2)
    return JSONResponse(content={'message': f'Libro con el id {uid} eliminado exitosamente.'})
