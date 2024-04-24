from pydantic import BaseModel, Field
from typing import Optional
from schemas.Author import Author
from uuid import uuid1


class Book(BaseModel):

    ''' BOOK MODEL '''

    title: str = Field(min_length=5, max_length=20)
    category: str = Field(min_length=5, max_length=20)
    release_date: int = Field(le=2024)
    authors: list[Author] = Field()
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Titulo del libro",
                    "category": "Categoria del libro",
                    "release_date": 2022,
                    "authors": [
                        {
                            "id": "17738d3c-9f1e-11ec-8d3d-0242ac130004",
                            "fullname": "Nombre del autor",
                            "date_birth": "23-04-2021"
                        }
                    ]
                }
            ]
        }
    }

    
