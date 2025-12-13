from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission_template import (
    RepoMissionTemplate,
    MissionTemplate,
    Name,
    Content,
    Type,
)
from grapechallenge.usecase.common.models import UsecaseOutput


class CreateMissionTemplateInput(BaseModel):
    name: str
    content: str
    type: str


async def create_mission_template(session: AsyncSession, request: Request, input: CreateMissionTemplateInput) -> UsecaseOutput:

    # create mission template
    created = await RepoMissionTemplate.create(
        session=session,
        mission_template=MissionTemplate.new(
            name=Name.from_str(input.name),
            content=Content.from_str(input.content),
            type=Type.from_str(input.type),
        )
    )

    return UsecaseOutput(
        content={
            **created.summary(),
            "name": created.mission_template.name.to_str(),
            "content": created.mission_template.content.to_str(),
            "type": created.mission_template.type.to_str(),
        },
        code=201
    )


# #
# cli

""" example input:
    --name "bible_reading"
    --content "오늘의 말씀을 읽어보세요"
    --type "bible"
"""

def get_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="Mission template name")
    parser.add_argument("--content", type=str, required=True, help="Mission template content")
    parser.add_argument("--type", type=str, required=True, help="Mission template type")

    args = parser.parse_args()

    return args


async def main():
    from grapechallenge.database.database import transactional_session_helper
    from unittest.mock import MagicMock

    args = get_arguments()

    async with transactional_session_helper() as session:
        result = await create_mission_template(
            session=session,
            request=MagicMock(),
            input=CreateMissionTemplateInput(
                name=args.name.strip(),
                content=args.content.strip(),
                type=args.type.strip(),
            )
        )
        print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
