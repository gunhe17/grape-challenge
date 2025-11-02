from datetime import date
from pydantic import BaseModel
from typing import List
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
from grapechallenge.usecase.create_bible_verse import CreateBibleVerseInput


class CreateBibleVersesInput(BaseModel):
    verses: List[CreateBibleVerseInput]

async def create_bible_verses(session: AsyncSession, request: Request, input: CreateBibleVersesInput) -> UsecaseOutput:

    # create bible verses
    created_list = []
    for verse_input in input.verses:
        created = await RepoBible.create(
            session=session,
            bible=Bible.new(
                date=Date.from_date(verse_input.date),
                content=Content.from_str(verse_input.content),
                reference=Reference.from_str(verse_input.reference),
            )
        )
        created_list.append(created)

    return UsecaseOutput(
        content={
            "verses": [
                {
                    **created.summary()
                }
                for created in created_list
            ],
            "count": len(created_list)
        },
        code=201
    )


# #
# cli

""" example json file:
    {
        "verses": [
            {
                "date": "2025-01-01", 
                "content": "하나님이 세상을 이처럼 사랑하사 독생자를 주셨으니", 
                "reference": "요한복음 3:16"
            },
            ...
        ]
    }
"""

def get_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="JSON file path containing verses array")

    args = parser.parse_args()

    return args

async def main():
    from grapechallenge.database.database import transactional_session_helper
    from unittest.mock import MagicMock
    from datetime import datetime
    import json

    args = get_arguments()

    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for verse in data['verses']:
        verse['date'] = datetime.strptime(verse['date'], "%Y-%m-%d").date()

    async with transactional_session_helper() as session:
        result = await create_bible_verses(
            session=session,
            request=MagicMock(),
            input=CreateBibleVersesInput(verses=data['verses'])
        )
        print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())