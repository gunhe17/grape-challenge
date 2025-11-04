from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission import RepoMission, Interaction
from grapechallenge.usecase.common.models import UsecaseOutput


class InteractionMissionInput(BaseModel):
    mission_id: str
    emoji: str

async def interaction_mission(session: AsyncSession, request: Request, input: InteractionMissionInput) -> UsecaseOutput:
    user_id = request.cookies.get("user_id", None)
    if not user_id:
        return UsecaseOutput(content={"message": "not authenticated"}, code=401)

    # validate emoji
    if input.emoji not in Interaction.allowed():
        return UsecaseOutput(
            content={
                "message": f"Invalid emoji. Allowed: {', '.join(Interaction.allowed())}"
            },
            code=400
        )

    # get mission
    found_mission = await RepoMission.get_by_id(session=session, id=input.mission_id)
    if not found_mission:
        return UsecaseOutput(
            content={
                "message": "No matched mission found"
            },
            code=404
        )

    # add interaction
    new_interaction = (
        found_mission.mission.interaction.add(input.emoji, user_id)
        if found_mission.mission.interaction
        else Interaction.from_list([{"icon": input.emoji, "user_id": user_id}])
    )

    # update mission
    updated = await RepoMission.update(
        session=session,
        mission=found_mission.mission.update_interaction(new_interaction),
        id=found_mission.id
    )

    return UsecaseOutput(
        content={
            **updated.summary(),
        },
        code=200
    )
