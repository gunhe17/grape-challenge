import os
from io import BytesIO
from typing import List, Tuple, Union
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont


# Configuration
CONFIG = {
    "background": "background1.jpg",
    "text_area": {"x": 160, "y": 670, "width": 1470, "height": 1380},
    "font_size": 48,
    "author_font_size": 36,
    "line_spacing": 60,
    "text_color": "#2C1810",
}


def load_background_image(base_dir: str) -> Image.Image | None:
    """Load background image"""
    image_path = os.path.join(base_dir, "template", "images", CONFIG["background"])
    if not os.path.exists(image_path):
        return None
    with Image.open(image_path) as img:
        return img.copy()


def load_font(base_dir: str, size: int) -> Union[FreeTypeFont, ImageFont.ImageFont]:
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


def wrap_text(text: str, font: Union[FreeTypeFont, ImageFont.ImageFont], max_width: int) -> List[str]:
    """Wrap text to fit within max_width (character-by-character for Korean support)"""
    if not text:
        return []

    # Normalize line breaks (handle both \r\n and \n)
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # First split by newlines to handle explicit line breaks
    paragraphs = text.split('\n')
    lines = []

    for paragraph in paragraphs:
        # Strip whitespace from paragraph
        paragraph = paragraph.strip()

        if not paragraph:
            # Empty line from consecutive newlines - skip to avoid extra spacing
            continue

        current_line = ""
        for char in paragraph:
            test_line = current_line + char
            bbox = font.getbbox(test_line)
            line_width = bbox[2] - bbox[0]

            if line_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = char
                else:
                    # Single character is too wide - force add it anyway
                    lines.append(char)
                    current_line = ""

        if current_line:
            lines.append(current_line)

    return lines


def prepare_text_blocks(
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
        user_name = (found.get("user_name") or "Unknown").strip()
        content = (found.get("mission_content") or "").strip()

        # Skip if no actual content
        if not content:
            continue

        # Prepare author line with smaller font
        author_text = f"{user_name}의 감사일기:"
        author_lines = wrap_text(author_text, author_font, max_width)

        # Prepare content lines with regular font
        content_lines = wrap_text(content, content_font, max_width)

        # Skip if no lines generated
        if not author_lines and not content_lines:
            continue

        # Create block with font type markers
        block = []
        for line in author_lines:
            block.append((line, 'author'))
        for line in content_lines:
            block.append((line, 'content'))

        if block:
            text_blocks.append(block)

    return text_blocks


def calculate_block_height(block: List[Tuple[str, str]]) -> int:
    """Calculate total height needed for a text block"""
    line_spacing = CONFIG["line_spacing"]
    return len(block) * line_spacing + line_spacing


def create_blank_page(original_image: Image.Image, width: int, height: int) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    """Create a new blank page with background image"""
    page_image = Image.new('RGB', (width, height), color='white')
    page_image.paste(original_image, (0, 0))
    return page_image, ImageDraw.Draw(page_image)


def render_pages(
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

    # Return empty list if no text blocks
    if not text_blocks:
        return pages

    current_page, current_draw = create_blank_page(original_image, width, height)
    y_offset = text_y

    for block in text_blocks:
        block_height = calculate_block_height(block)

        # Check if block fits in current page
        if y_offset + block_height > text_y + text_height:
            pages.append(current_page)
            current_page, current_draw = create_blank_page(original_image, width, height)
            y_offset = text_y

        for line_text, font_type in block:
            font = author_font if font_type == 'author' else content_font
            # Ensure line_text is not empty to avoid rendering issues
            if line_text:
                current_draw.text((text_x, y_offset), line_text, fill=text_color, font=font)
            y_offset += line_spacing

        # Add extra spacing between different user entries
        y_offset += line_spacing

    # Only add the last page if it has content
    if current_page and pages or text_blocks:
        pages.append(current_page)

    return pages


def convert_pages_to_bytes(pages: List[Image.Image]) -> List[bytes]:
    """Convert PIL Image pages to JPEG bytes"""
    image_bytes_list = []

    for page in pages:
        output_buffer = BytesIO()
        page.save(output_buffer, format="JPEG", quality=95)
        output_buffer.seek(0)
        image_bytes_list.append(output_buffer.read())

    return image_bytes_list


def generate_report_images(founds: List[dict], background_image: str = "background1.jpg") -> dict:
    """Generate report images from mission data"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Update CONFIG with custom background image
    CONFIG["background"] = background_image

    original_image = load_background_image(base_dir)

    if original_image is None:
        return {"error": "Background image not found", "code": 404}

    # Calculate canvas size
    text_area = CONFIG["text_area"]
    required_width = max(original_image.width, text_area["x"] + text_area["width"])
    required_height = max(original_image.height, text_area["y"] + text_area["height"])

    if required_width > original_image.width or required_height > original_image.height:
        expanded_image = Image.new('RGB', (required_width, required_height), color='white')
        expanded_image.paste(original_image, (0, 0))
        original_image = expanded_image

    # Load fonts and prepare content
    content_font = load_font(base_dir, CONFIG["font_size"])
    author_font = load_font(base_dir, CONFIG["author_font_size"])

    text_blocks = prepare_text_blocks(
        founds=founds,
        content_font=content_font,
        author_font=author_font,
        max_width=text_area["width"]
    )

    if not text_blocks:
        return {"error": "No valid mission content to display", "code": 404}

    pages = render_pages(
        text_blocks=text_blocks,
        original_image=original_image,
        canvas_size=(required_width, required_height),
        content_font=content_font,
        author_font=author_font,
    )

    if not pages:
        return {"error": "Failed to generate report pages", "code": 500}

    image_bytes_list = convert_pages_to_bytes(pages)

    return {
        "image_bytes_list": image_bytes_list,
        "page_count": len(pages)
    }
