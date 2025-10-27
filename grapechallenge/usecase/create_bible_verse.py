from datetime import date
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.bible import (
    RepoBible,
    Bible,
    Date,
    Content,
    Reference,
)
from grapechallenge.usecase.common.models import UsecaseOutput


class CreateBibleVerseInput(BaseModel):
    date: date
    content: str
    reference: str

async def create_bible_verse(session: AsyncSession, request: Request, input: CreateBibleVerseInput) -> UsecaseOutput:

    # create bible verse
    created = await RepoBible.create(
        session=session,
        bible=Bible.new(
            date=Date.from_date(input.date),
            content=Content.from_str(input.content),
            reference=Reference.from_str(input.reference),
        )
    )

    return UsecaseOutput(
        content={
            **created.summary()
        },
        code=201
    )


# #
# cli

""" example input:
    --date "2025-01-01"
    --content "하나님이 세상을 ..." 
    --reference "요한복음 3:16"
"""

def get_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--content", type=str, required=True, help="Bible verse content")
    parser.add_argument("--reference", type=str, required=True, help="Bible verse reference")

    args = parser.parse_args()

    return args


async def main():
    from grapechallenge.database.database import transactional_session_helper
    from unittest.mock import MagicMock
    from datetime import datetime
    args = get_arguments()

    # Parse date string to date object (strip whitespace)
    verse_date = datetime.strptime(args.date.strip(), "%Y-%m-%d").date()

    async with transactional_session_helper() as session:
        result = await create_bible_verse(
            session=session,
            request=MagicMock(),
            input=CreateBibleVerseInput(
                date=verse_date,
                content=args.content.strip(),
                reference=args.reference.strip(),
            )
        )
        print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())