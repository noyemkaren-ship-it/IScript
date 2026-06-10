from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    lex: Optional[str] = None
    content: str
    indent: str = ""  # Добавляем поле для отступов