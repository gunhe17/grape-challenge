from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.bible import RepoBible
from grapechallenge.usecase.common.models import UsecaseOutput


class GetTodayBibleVerseInput(BaseModel):
    pass

async def get_today_bible_verse(session: AsyncSession, request: Request, input: GetTodayBibleVerseInput) -> UsecaseOutput:

    # get today's bible verse
    found = await RepoBible.get_today_bible_verse(session=session)

    if not found:
        return UsecaseOutput(
            content={
                "message": "No bible verse found for today"
            },
            code=404
        )

    return UsecaseOutput(
        content={
            "id": found.id,
            "date": found.bible.date.to_date().isoformat(),
            "content": found.bible.content.to_str(),
            "reference": found.bible.reference.to_str(),
            **found.summary()
        },
        code=200
    )
