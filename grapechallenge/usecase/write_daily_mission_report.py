import os
from io import BytesIO
from typing import List, Tuple, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from grapechallenge.domain.mission import RepoMission
from grapechallenge.usecase.common.models import UsecaseOutput
from grapechallenge.usecase.common.kst import kst


class WriteDailyMissionReportInput(BaseModel):
    pass


# Configuration
CONFIG = {
    "background": "background1.jpg",
    "text_area": {"x": 160, "y": 670, "width": 1470, "height": 1380},
    "font_size": 48,
    "author_font_size": 36,
    "line_spacing": 60,
    "text_color": "#2C1810",
}


def _load_background_image(base_dir: str) -> Image.Image | None:
    """Load background image"""
    image_path = os.path.join(base_dir, "template", "images", CONFIG["background"])
    if not os.path.exists(image_path):
        return None
    with Image.open(image_path) as img:
        return img.copy()


def _load_font(base_dir: str, size: int) -> Union[FreeTypeFont, ImageFont.ImageFont]:
    """Load Korean-compatible font"""
    fonts_dir = os.path.join(base_dir, "template", "fonts")
    font_paths = [
        os.path.join(fonts_dir, "BMHANNAProOTF.otf"),
        "/System/Library/Fonts/Supplemental/NanumGothic.ttc",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue

    return ImageFont.load_default()


def _wrap_text(text: str, font: Union[FreeTypeFont, ImageFont.ImageFont], max_width: int) -> List[str]:
    """Wrap text to fit within max_width (character-by-character for Korean support)"""
    lines = []
    current_line = ""

    for char in text:
        test_line = current_line + char
        bbox = font.getbbox(test_line)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char

    if current_line:
        lines.append(current_line)

    return lines


def _prepare_text_blocks(
    founds: List[dict],
    content_font: Union[FreeTypeFont, ImageFont.ImageFont],
    author_font: Union[FreeTypeFont, ImageFont.ImageFont],
    max_width: int
) -> List[List[Tuple[str, str]]]:
    """Prepare text blocks for each mission entry (each block should stay together)

    Returns list of blocks, where each block contains tuples of (text, font_type)
    font_type can be 'author' or 'content'
    """
    text_blocks = []

    for found in founds:
        user_name = found.get("user_name", "Unknown")
        content = found.get("mission_content", "")

        # Prepare author line with smaller font
        author_text = f"{user_name}의 감사일기:"
        author_lines = _wrap_text(author_text, author_font, max_width)

        # Prepare content lines with regular font
        content_lines = _wrap_text(content, content_font, max_width)

        # Create block with font type markers
        block = []
        for line in author_lines:
            block.append((line, 'author'))
        for line in content_lines:
            block.append((line, 'content'))

        text_blocks.append(block)

    return text_blocks


def _calculate_block_height(block: List[Tuple[str, str]]) -> int:
    """Calculate total height needed for a text block"""
    line_spacing = CONFIG["line_spacing"]
    return len(block) * line_spacing + line_spacing


def _create_blank_page(original_image: Image.Image, width: int, height: int) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    """Create a new blank page with background image"""
    page_image = Image.new('RGB', (width, height), color='white')
    page_image.paste(original_image, (0, 0))
    return page_image, ImageDraw.Draw(page_image)


def _render_pages(
    text_blocks: List[List[Tuple[str, str]]],
    original_image: Image.Image,
    canvas_size: Tuple[int, int],
    content_font: Union[FreeTypeFont, ImageFont.ImageFont],
    author_font: Union[FreeTypeFont, ImageFont.ImageFont],
) -> List[Image.Image]:
    """Render text blocks into multiple pages"""
    text_area = CONFIG["text_area"]
    line_spacing = CONFIG["line_spacing"]
    text_color = CONFIG["text_color"]

    pages = []
    width, height = canvas_size
    text_x, text_y = text_area["x"], text_area["y"]
    text_height = text_area["height"]

    current_page, current_draw = _create_blank_page(original_image, width, height)
    y_offset = text_y

    for block in text_blocks:
        block_height = _calculate_block_height(block)

        if y_offset + block_height > text_y + text_height:
            pages.append(current_page)
            current_page, current_draw = _create_blank_page(original_image, width, height)
            y_offset = text_y

        for line_text, font_type in block:
            font = author_font if font_type == 'author' else content_font
            current_draw.text((text_x, y_offset), line_text, fill=text_color, font=font)
            y_offset += line_spacing

        y_offset += line_spacing

    if current_page:
        pages.append(current_page)

    return pages


def _convert_pages_to_bytes(pages: List[Image.Image]) -> List[bytes]:
    """Convert PIL Image pages to JPEG bytes"""
    image_bytes_list = []

    for page in pages:
        output_buffer = BytesIO()
        page.save(output_buffer, format="JPEG", quality=95)
        output_buffer.seek(0)
        image_bytes_list.append(output_buffer.read())

    return image_bytes_list


async def write_daily_mission_report(
    session: AsyncSession,
    request: Request,
    input: WriteDailyMissionReportInput
) -> UsecaseOutput:
    """Generate daily mission report as multiple page images"""

    # Fetch missions from database
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

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    original_image = _load_background_image(base_dir)

    if original_image is None:
        return UsecaseOutput(
            content={"message": "Background image not found"},
            code=404
        )

    # Calculate canvas size
    text_area = CONFIG["text_area"]
    required_width = max(original_image.width, text_area["x"] + text_area["width"])
    required_height = max(original_image.height, text_area["y"] + text_area["height"])

    if required_width > original_image.width or required_height > original_image.height:
        expanded_image = Image.new('RGB', (required_width, required_height), color='white')
        expanded_image.paste(original_image, (0, 0))
        original_image = expanded_image

    # Load fonts and prepare content
    content_font = _load_font(base_dir, CONFIG["font_size"])
    author_font = _load_font(base_dir, CONFIG["author_font_size"])

    text_blocks = _prepare_text_blocks(
        founds=founds,
        content_font=content_font,
        author_font=author_font,
        max_width=text_area["width"]
    )

    pages = _render_pages(
        text_blocks=text_blocks,
        original_image=original_image,
        canvas_size=(required_width, required_height),
        content_font=content_font,
        author_font=author_font,
    )

    image_bytes_list = _convert_pages_to_bytes(pages)

    return UsecaseOutput(
        content={
            "missions": [
                {
                    "id": found.get("mission_id", None),
                    "name": found.get("template_name", None),
                    "content": found.get("mission_content", None),
                    "content_created_at": kst(found.get("mission_created_at")),  # type:ignore
                    "user_id": found.get("user_id", None),
                    "user_cell": found.get("user_cell", None),
                    "user_name": found.get("user_name", None),
                }
                for found in founds
            ],
            "count": len(founds),
            "message": "Report image generated successfully",
            "image_bytes_list": image_bytes_list,
            "page_count": len(pages)
        },
        code=200
    )


# CLI
async def main():
    import argparse
    from grapechallenge.database.database import transactional_session_helper
    from unittest.mock import MagicMock

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="./mission_report", help="Output file prefix")
    args = parser.parse_args()

    async with transactional_session_helper() as session:
        result = await write_daily_mission_report(
            session=session,
            request=MagicMock(),
            input=WriteDailyMissionReportInput()
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

        print(f"Generated {page_count} page(s) from {result.content.get('count')} mission(s)")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
