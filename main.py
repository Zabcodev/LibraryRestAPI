from fastapi import FastAPI
from routes.book import book_router
from routes.author import author_router
import uvicorn

''' REST-API '''

app = FastAPI()
app.title = 'LIBRARY API-REST'
app.description = 'REST-API para una libreria'
app.version = '1.0.0'

app.include_router(book_router)
app.include_router(author_router)

if __name__ == '__main__':
    uvicorn.run(app='main:app', port=5000, reload=True, host='0.0.0.0')
