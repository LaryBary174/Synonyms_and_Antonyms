from pydantic import BaseModel, Field, field_validator
import re


class WordResponse(BaseModel):
    """Ответ со списком синонимов и антонимов для слова."""

    synonyms: list[str] = Field(description="Список синонимов")
    antonyms: list[str] = Field(description="Список антонимов")
    found: bool = Field(description="Найдены ли слова ")


class WordRequest(BaseModel):
    word: str = Field(min_length=1, description="Слово для поиска синонимов/антонимов")

    @field_validator("word")
    @classmethod
    def validate_no_digits(cls, v: str) -> str:
        if re.search(r"\d", v):
            raise ValueError("Слово не должно содержать цифры")
        return v
