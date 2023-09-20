from typing import Optional
from pydantic import BaseModel

class Path(BaseModel):
    # id: Optional[int]
    id: int

# class ErrorSchema(BaseModel):
#     """ Schema de retorno de erros
#     """
#     mesage: str