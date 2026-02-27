from fastapi import APIRouter, HTTPException, status, Depends, Request

from services.ai_service import AIService
from schemas.words_schemas import WordResponse, WordRequest


router = APIRouter(prefix="/api/words", tags=["words"])


def get_ai_service(request: Request) -> AIService:
    return request.app.state.ai_service


@router.post("/", response_model=WordResponse, status_code=status.HTTP_200_OK)
def get_synonyms_and_antonyms(
    word_request: WordRequest, ai_service: AIService = Depends(get_ai_service)
):
    res = ai_service.get_words(word_request.word)
    if not res.found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Для слова {word_request.word} не найдено синонимов и антонимов",
        )
    return res
