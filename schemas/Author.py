from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid1


class Author(BaseModel):

    ''' AUTHOR MODEL '''

    id: Optional[str] = Field(min_length=10, max_length=36)
    fullname: str = Field(min_length=5, max_length=45)
    date_birth: str = Field(
        regexp="\b(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/](19\d\d|20\d\d)\b")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "17738d3c-9f1e-11ec-8d3d-0242ac130004",
                    "fullname": "Nombre del autor",
                    "date_birth": "23-04-2021"
                }
            ]
        }
    }