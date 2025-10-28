from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from grapechallenge.domain.mission import RepoMission
from grapechallenge.usecase.common.models import UsecaseOutput
from grapechallenge.usecase.write_daily_mission_report_helper import generate_report_images


class WriteDailyMissionReportInput(BaseModel):
    background_image: str = "background1.jpg"


async def write_daily_mission_report(
    session: AsyncSession,
    request: Request,
    input: WriteDailyMissionReportInput
) -> UsecaseOutput:
    """Generate daily mission report as multiple page images"""

    # get missions
    founds = await RepoMission.get_by_template_name(
        session=session,
        name="감사 일기 작성하기",
        date="report"
    )

    if not founds:
        return UsecaseOutput(
            content={"message": "No missions found for the report period"},
            code=404
        )

    # generate images
    result = generate_report_images(founds, background_image=input.background_image)

    if result.get("error"):
        return UsecaseOutput(
            content={"message": result["error"]},
            code=result.get("code", 500)
        )

    return UsecaseOutput(
        content={
            "image_bytes_list": result["image_bytes_list"],
            "page_count": result["page_count"]
        },
        code=200
    )


# #
# cli

async def main():
    import argparse
    from grapechallenge.database.database import transactional_session_helper
    from unittest.mock import MagicMock

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="./mission_report", help="Output file prefix")
    parser.add_argument("--background", default="background1.jpg", help="Background image filename")
    args = parser.parse_args()

    async with transactional_session_helper() as session:
        result = await write_daily_mission_report(
            session=session,
            request=MagicMock(),
            input=WriteDailyMissionReportInput(background_image=args.background)
        )

        if result.code != 200:
            print(f"Error: {result.content.get('message')}")
            return

        image_bytes_list = result.content.get('image_bytes_list', [])
        if not image_bytes_list:
            print("No images generated")
            return

        output_prefix = args.output.removesuffix('.jpg').removesuffix('.jpeg')
        page_count = len(image_bytes_list)

        for i, image_bytes in enumerate(image_bytes_list, 1):
            output_path = f"{output_prefix}.jpg" if page_count == 1 else f"{output_prefix}_page{i}.jpg"
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            print(f"Saved: {output_path}")

        print(f"Generated {page_count} page(s)")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
