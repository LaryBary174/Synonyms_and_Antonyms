from typing import TypedDict
from langchain_gigachat import GigaChat
from langgraph.graph import StateGraph, START, END
from schemas.words_schemas import WordResponse


class State(TypedDict):
    word: str
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

        structured_llm = self.llm.with_structured_output(WordResponse)

        prompt = (
            f"ЗАДАЧА: Для слова '{word}' найди И синонимы И антонимы.\n\n"
            f"ТРЕБОВАНИЯ:\n"
            f"1. synonyms: список синонимов 10 вариантов\n"
            f"2. antonyms: список антонимов 10 вариантов'\n"
            f"3. found: true если найдено что-то из пунктов 1 или 2\n\n"
            f"ВАЖНО: Обе части ОБЯЗАТЕЛЬНЫ к заполнению!\n\n"
            f"ОБЯЗАТЕЛЬНО заполни И synonyms И antonyms (или пустые списки если нет).\n"
        )

        res = structured_llm.invoke(prompt)
        state["result"] = res
        return state

    def get_words(
        self,
        word: str,
    ) -> WordResponse:
        res = self.state_graph.invoke({"word": word, "result": None})
        return res["result"]
