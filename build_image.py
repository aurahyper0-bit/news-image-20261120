"""Draw the 20 November 2026 world-news front page as a 1024x1024 PNG.

Layout: black masthead, red date line, one lead story, three columns of
secondary stories, a dark "also today" strip and a small footer line.
Run:  python3 build_image.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SIZE = 1024
MARGIN = 48
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (198, 12, 12)
INK = (30, 30, 30)
GREY = (105, 105, 105)
NAVY = (18, 18, 46)


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, width):
    """Greedy word wrap returning a list of lines that fit in width."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=font) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def para(draw, text, font, x, y, width, colour, spacing=8):
    """Draw wrapped paragraph starting at (x, y); return y after it."""
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=colour)
        y += font.size + spacing
    return y


def main():
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)

    bold_big = load("DejaVuSans-Bold.ttf", 66)
    bold_date = load("DejaVuSans-Bold.ttf", 34)
    bold_head = load("DejaVuSans-Bold.ttf", 46)
    bold_col = load("DejaVuSans-Bold.ttf", 27)
    body = load("DejaVuSans.ttf", 27)
    body_small = load("DejaVuSans.ttf", 22)
    bold_strip = load("DejaVuSans-Bold.ttf", 26)
    strip = load("DejaVuSans.ttf", 24)
    foot = load("DejaVuSans.ttf", 20)

    # Masthead.
    draw.rectangle([0, 0, SIZE, 96], fill=BLACK)
    draw.text((SIZE / 2, 48), "WORLD NEWS", font=bold_big, fill=WHITE,
              anchor="mm")

    # Date line.
    draw.text((SIZE / 2, 128), "FRIDAY, 20 NOVEMBER 2026", font=bold_date,
              fill=RED, anchor="mm")
    draw.line([MARGIN, 160, SIZE - MARGIN, 160], fill=BLACK, width=3)

    # Lead story.
    draw.text((MARGIN, 182), "TRUMP HAILS \u2018MOMENTOUS\u2019", font=bold_head,
              fill=BLACK)
    draw.text((MARGIN, 238), "SHENZHEN PACT", font=bold_head, fill=BLACK)
    lead = (
        "Donald Trump hailed the first-ever US\u2013Russia\u2013China trilateral "
        "summit at the White House on Friday. The leaders\u2019 \u2018Declaration "
        "toward Peace\u2019 says a nuclear war \u2018cannot be won and must never "
        "be fought\u2019 \u2014 though critics note few concrete results."
    )
    para(draw, lead, body, MARGIN, 306, SIZE - 2 * MARGIN, INK, spacing=6)
    draw.line([MARGIN, 452, SIZE - MARGIN, 452], fill=BLACK, width=2)

    # Three secondary stories in columns.
    col_w = 304
    col_x = [MARGIN, 360, 672]
    stories = [
        ("RUSSIA\u2019S BIGGEST BARRAGE HITS KYIV",
         "More than 400 drones and 110 missiles struck Ukraine on Friday; "
         "three Kyiv bridges hit, 8 killed. Two Russian missiles also landed "
         "in Poland."),
        ("CYCLONE AKVAN MAKES LANDFALL",
         "The storm crossed India\u2019s Andhra Pradesh\u2013Odisha coast near "
         "Gopalpur, bringing heavy rain and coastal danger."),
        ("ANTHROPIC DEBUTS ON NASDAQ",
         "The AI firm\u2019s shares closed above their $83 offer price on "
         "their first day of trading."),
    ]
    top = 478
    for x, (headline, text) in zip(col_x, stories):
        draw.rectangle([x, top, x + 64, top + 5], fill=RED)
        y = top + 18
        y = para(draw, headline, bold_col, x, y, col_w, BLACK, spacing=4)
        para(draw, text, body_small, x, y + 6, col_w, INK, spacing=5)

    # Dark strip: also today.
    draw.rectangle([0, 760, SIZE, 950], fill=NAVY)
    draw.text((MARGIN, 782), "ALSO TODAY", font=bold_strip, fill=WHITE)
    strip_text = (
        "Myanmar rejects world court genocide ruling  \u2022  California "
        "probes Nvidia  \u2022  Stocks slide for a 7th day  \u2022  COP31 "
        "fossil-fuel talks stall"
    )
    para(draw, strip_text, strip, MARGIN, 822, SIZE - 2 * MARGIN, WHITE,
         spacing=4)

    # Footer.
    draw.text((SIZE / 2, 972),
              "\u2014 compiled from major wire reports  \u2022  20 November 2026",
              font=foot, fill=GREY, anchor="mm")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
