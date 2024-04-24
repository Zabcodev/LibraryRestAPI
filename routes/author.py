from fastapi import APIRouter, status, Path
from json import load
from fastapi.responses import JSONResponse
from uuid import UUID

author_router = APIRouter(prefix='/authors', tags=['authors'])


@author_router.get('')
async def get_authors():
    ''' ENDPOINT GET ALL AUTHORS FROM DB.JSON '''

    with open('data/db.json', 'r', encoding="utf-8") as jsonfile:
        data = load(jsonfile)
        authors = data['authors']
        if authors is None:
            return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=authors, status_code=status.HTTP_200_OK)


@author_router.get('/{uid}')
async def get_author_by_id(uid: UUID = Path(min_length=10)):
    ''' ENDPOINT GET AUTHOR BY UNIQUE ID '''

    with open('data/db', 'r', encoding="utf-8") as jsonfile:
        data = load(jsonfile)
        authors = data['authors']
        for author in authors:
            if author['id'] == str(uid):
                return JSONResponse(content=author, status_code=status.HTTP_200_OK)
        return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
