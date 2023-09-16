from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Schema de retorno de erros
    """
    mesage: str