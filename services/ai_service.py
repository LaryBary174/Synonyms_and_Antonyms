from typing import Literal, TypedDict
from langchain_gigachat import GigaChat
from langgraph.graph import StateGraph, START, END
from schemas.words_schemas import WordResponse


class State(TypedDict):
    word: str
    word_type: str
    result: WordResponse


class AIService:
    def __init__(self, credentials: str):
        self.llm = GigaChat(
            credentials=credentials, verify_ssl_certs=False, model="GigaChat-2"
        )
        self.state_graph = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(State)
        workflow.add_node("process", self._process_word)
        workflow.add_edge(START, "process")
        workflow.add_edge("process", END)
        return workflow.compile()

    def _process_word(self, state: State) -> State:
        word = state["word"]
        word_type = state["word_type"]
        structured_llm = self.llm.with_structured_output(WordResponse)
        if word_type == "синоним":
            prompt = (
                f"Найди 10 синонимов для слова {word}. "
                f"Заполни поле synonyms списком синонимов, а поле antonyms оставь пустым. "
                f"Если синонимов не найдено, установи found в false и оставь synonyms пустым."
            )
        else:
            prompt = (
                f"Найди 10 антонимов для слова {word}. "
                f"Заполни поле antonyms списком антонимов, а поле synonyms оставь пустым."
                f"Если антонимов не найдено, установи found в false и оставь antonyms пустым."
            )

        res = structured_llm.invoke(prompt)
        state["result"] = res
        return state

    def get_words(
        self, word: str, word_type: Literal["синоним", "антоним"]
    ) -> WordResponse:
        res = self.state_graph.invoke(
            {"word": word, "word_type": word_type, "result": None}
        )
        return res["result"]
