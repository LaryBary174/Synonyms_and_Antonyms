from typing import Literal
from langchain_gigachat import GigaChat
from schemas.words_schemas import WordResponse


class AIService:
    def __init__(self, credentials: str):
        self.llm = GigaChat(
            credentials=credentials,
            verify_ssl_certs=False,
            model="GigaChat-2"
        )

    def get_words(self,word: str, word_type: Literal["синоним", "антоним"]) -> WordResponse:
        structured_llm = self.llm.with_structured_output(WordResponse)
        if word_type == "синоним":
            prompt = (f"Найди 10 синонимов для слова {word}. "
                      f"Заполни поле synonyms списком синонимов, а поле antonyms оставь пустым. "
                      f"Если синонимов не найдено, установи found в false и оставь synonyms пустым."
            )
        else:
            prompt = (f"Найди 10 антонимов для слова {word}. "
                      f"Заполни поле antonyms списком антонимов, а поле synonyms оставь пустым."
                      f"Если антонимов не найдено, установи found в false и оставь antonyms пустым.")

        return structured_llm.invoke(prompt)

