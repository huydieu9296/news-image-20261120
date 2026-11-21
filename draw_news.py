#!/usr/bin/env python3
"""Render one newspaper front page for Friday 20 November 2026.

A navy masthead, a red rule, and six story cards in a 2x3 grid. Each
card carries a coloured spine, a line glyph, a kicker, a headline that
shrinks to fit two lines, a two-line deck and a key-fact strip, with a
centred footer underneath. The script is deterministic: fixed fonts,
fixed geometry, no randomness, no clock, no network. It writes
entry.png beside itself.
"""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER_BG = (246, 241, 227)
CARD_BG = (255, 253, 246)
CARD_LINE = (220, 213, 194)
MASTHEAD_BG = (22, 35, 63)
MASTHEAD_SUB = (201, 210, 224)
RULE_RED = (180, 35, 24)
BODY_INK = (28, 28, 26)
DECK_INK = (74, 70, 62)
FOOT_INK = (122, 114, 100)
DIVIDER = (214, 207, 188)
TITLE_INK = (250, 247, 238)

HEADLINE = "THE WORLD IN ONE DAY"
DATELINE = "FRIDAY, 20 NOVEMBER 2026"
FOOTLINE = "Six stories from a single day  ·  Compiled from verified reports  ·  20 November 2026"


@dataclass
class Story:
    tag: str
    title: str
    body: str
    note: str
    color: tuple
    glyph: str


STORIES = [
    Story("DIPLOMACY  ·  SHENZHEN",
          "Trump, Xi and Putin sign a peace declaration",
          "Three nuclear powers pledge talks to cut nuclear risks — but announce no arms cuts or timetables.",
          "No breakthrough on Ukraine", (14, 124, 123), "world"),
    Story("WAR  ·  MIDDLE EAST",
          "Houthi missile hits Riyadh's tallest tower",
          "Blast blows out windows across seven floors of the Saudi wealth fund's HQ; no one is hurt.",
          "2nd strike on district in 12 days", (166, 28, 28), "fire"),
    Story("WEATHER  ·  INDIA",
          "Cyclone Akvan slams India's east coast",
          "Storm crosses near Gopalpur in the morning with 80 km/h winds gusting to 90 after 300,000 people are moved to safety.",
          "300,000 evacuated", (21, 101, 192), "storm"),
    Story("BUSINESS  ·  WALL STREET",
          "Anthropic soars in biggest IPO ever",
          "Claude maker's shares open 34% up at $111.50 and close 17% higher, valuing it near $1.3 trillion.",
          "$81.3bn raised — a record", (106, 63, 181), "chart"),
    Story("DIPLOMACY  ·  UKRAINE",
          "Russia 'comfortable' with NATO-style guarantees",
          "Kushner says Moscow accepts Article 5-style pledges for Kyiv; Trump is open to the idea.",
          "Berlin talks, 19 November", (27, 125, 61), "balance"),
    Story("WAR  ·  GAZA",
          "Gazans return as Israeli tank raid ends",
          "Families walk home after the first ground crossing of the ceasefire line since October 2025.",
          "Raid lasted two days", (178, 106, 0), "home"),
]


def typeface(px, weight="plain"):
    path = FONT_BOLD if weight == "bold" else FONT_PLAIN
    return ImageFont.truetype(path, px)


def centred(draw, text, fnt, y, fill):
    """Draw text horizontally centred on the page at height y."""
    left, _, right, _ = draw.textbbox((0, 0), text, font=fnt)
    draw.text(((W - (right - left)) / 2 - left, y), text, font=fnt, fill=fill)


def shrink_to_fit(draw, text, box_w, most_lines, px0, px_floor, weight):
    """Pick the largest size whose wrap fits, else clip the tail."""
    px = px0
    while px > px_floor:
        fnt = typeface(px, weight)
        # measure with a word wrap on pixel width
        words = text.split()
        cur, out = "", []
        for word in words:
            trial = word if not cur else cur + " " + word
            if draw.textlength(trial, font=fnt) <= box_w:
                cur = trial
            else:
                out.append(cur)
                cur = word
        out.append(cur)
        if len(out) <= most_lines:
            return out, fnt
        px -= 1
    fnt = typeface(px_floor, weight)
    words = text.split()
    cur, out = "", []
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= box_w:
            cur = trial
        else:
            out.append(cur)
            cur = word
    out.append(cur)
    if len(out) > most_lines:
        out = out[:most_lines]
        tail = out[-1]
        while tail and draw.textlength(tail + "…", font=fnt) > box_w:
            tail = tail.rsplit(" ", 1)[0] if " " in tail else tail[:-1]
        out[-1] = tail + "…"
    return out, fnt


def glyph(draw, kind, x, y, side, color):
    """Line glyphs, each drawn inside the square (x, y, side)."""
    x2, y2 = x + side, y + side
    mx, my = x + side // 2, y + side // 2
    if kind == "world":
        draw.ellipse([x + 4, y + 4, x2 - 4, y2 - 4], outline=color, width=3)
        draw.ellipse([mx - 9, y + 4, mx + 9, y2 - 4], outline=color, width=2)
        draw.line([x + 4, my, x2 - 4, my], fill=color, width=2)
        draw.arc([x + 4, y + 12, x2 - 4, y2 - 12], 200, 340,
                 fill=color, width=2)
    elif kind == "pad":
        draw.rounded_rectangle([x + 4, y + 14, x2 - 4, y2 - 8], radius=10,
                               outline=color, width=3)
        draw.line([x + 14, y + 24, x + 14, y + 34], fill=color, width=2)
        draw.line([x + 9, y + 29, x + 19, y + 29], fill=color, width=2)
        draw.ellipse([x2 - 24, y + 22, x2 - 18, y + 28], fill=color)
        draw.ellipse([x2 - 14, y + 28, x2 - 8, y + 34], fill=color)
    elif kind == "brush":
        draw.line([x + 8, y2 - 6, x + 26, y + 20], fill=color, width=5)
        draw.line([x + 24, y + 12, x + 34, y + 6], fill=color, width=3)
        draw.polygon([(x + 30, y + 8), (x + 40, y + 4), (x + 34, y + 16)],
                     fill=color)
    elif kind == "balance":
        draw.line([mx, y + 6, mx, y2 - 8], fill=color, width=3)
        draw.line([x + 8, y + 12, x2 - 8, y + 12], fill=color, width=3)
        for sx in (x + 8, x2 - 8):
            draw.line([sx, y + 12, sx - 2, y + 26], fill=color, width=2)
            draw.line([sx, y + 12, sx + 6, y + 26], fill=color, width=2)
            draw.arc([sx - 6, y + 22, sx + 10, y + 32], 0, 180,
                     fill=color, width=2)
        draw.line([x + 10, y2 - 8, x2 - 10, y2 - 8], fill=color, width=3)
    elif kind == "fire":
        draw.pieslice([x + 10, y + 10, x2 - 10, y2 - 4], 0, 180, fill=color)
        draw.polygon([(mx - 8, y + 26), (mx, y + 4), (mx + 8, y + 26)],
                     fill=color)
        draw.ellipse([mx - 5, y + 26, mx + 5, y + 38], fill=CARD_BG)
    elif kind == "ship":
        draw.polygon([(mx, y + 4), (mx + 8, y + 22), (mx, y + 18),
                      (mx - 8, y + 22)], outline=color, width=3)
        draw.line([mx - 6, y + 26, mx - 12, y + 36], fill=color, width=2)
        draw.line([mx + 6, y + 26, mx + 12, y + 36], fill=color, width=2)
        draw.line([mx, y + 30, mx, y + 40], fill=color, width=3)
        draw.ellipse([mx - 3, y + 10, mx + 3, y + 16], outline=color, width=2)
    elif kind == "storm":
        draw.ellipse([x + 6, y + 8, x + 26, y + 26], outline=color, width=3)
        draw.ellipse([x + 18, y + 4, x + 40, y + 26], outline=color, width=3)
        draw.line([x + 8, y + 26, x + 38, y + 26], fill=color, width=3)
        for rx in (x + 12, x + 22, x + 32):
            draw.line([rx, y + 32, rx - 3, y + 42], fill=color, width=3)
    elif kind == "chart":
        draw.line([x + 8, y + 8, x + 8, y2 - 8], fill=color, width=3)
        draw.line([x + 8, y2 - 8, x2 - 6, y2 - 8], fill=color, width=3)
        draw.line([x + 12, y + 32, x + 21, y + 24, x + 29, y + 28,
                   x + 38, y + 12], fill=color, width=3)
        draw.polygon([(x + 38, y + 12), (x + 30, y + 12), (x + 38, y + 20)],
                     fill=color)
    elif kind == "home":
        draw.line([x + 6, y + 24, mx, y + 8, x2 - 6, y + 24],
                  fill=color, width=3)
        draw.rectangle([x + 12, y + 24, x2 - 12, y2 - 6], outline=color,
                       width=3)
        draw.rectangle([mx - 5, y + 30, mx + 5, y2 - 6], fill=color)


def card(draw, story, rect):
    """One story card: spine, kicker+glyph, headline, deck, fact strip."""
    bx, by, bw, bh = rect
    draw.rectangle([bx, by, bx + bw, by + bh], fill=CARD_BG,
                   outline=CARD_LINE, width=1)
    draw.rectangle([bx + 1, by + 1, bx + 10, by + bh - 1], fill=story.color)

    tx = bx + 26
    tw = bw - 26 - 20
    draw.text((tx, by + 18), story.tag, font=typeface(16, "bold"),
              fill=story.color)
    glyph(draw, story.glyph, bx + bw - 20 - 46, by + 14, 46, story.color)

    rows, fnt = shrink_to_fit(draw, story.title, tw, 2, 31, 19, "bold")
    yy = by + 64
    for row in rows:
        draw.text((tx, yy), row, font=fnt, fill=BODY_INK)
        yy += fnt.size + 8

    rows, fnt = shrink_to_fit(draw, story.body, tw, 2, 17, 13, "plain")
    yy = by + 150
    for row in rows:
        draw.text((tx, yy), row, font=fnt, fill=DECK_INK)
        yy += fnt.size + 8

    draw.line([tx, by + bh - 42, bx + bw - 20, by + bh - 42],
              fill=DIVIDER, width=1)
    draw.text((tx, by + bh - 32), story.note, font=typeface(16, "bold"),
              fill=story.color)


def render():
    page = Image.new("RGB", (W, H), PAPER_BG)
    draw = ImageDraw.Draw(page)

    draw.rectangle([0, 0, W, 148], fill=MASTHEAD_BG)
    centred(draw, HEADLINE, typeface(54, "bold"), 26, TITLE_INK)
    centred(draw, DATELINE, typeface(22), 100, MASTHEAD_SUB)
    draw.rectangle([0, 148, W, 153], fill=RULE_RED)

    margin, gap = 30, 24
    top, bottom = 172, 956
    cw = (W - 2 * margin - gap) // 2
    ch = (bottom - top - 2 * 18) // 3
    for pos, story in enumerate(STORIES):
        r, c = divmod(pos, 2)
        card(draw, story, (margin + c * (cw + gap),
                           top + r * (ch + 18), cw, ch))

    centred(draw, FOOTLINE, typeface(14), 976, FOOT_INK)

    out = Path(__file__).resolve().parent / "entry.png"
    page.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    render()
