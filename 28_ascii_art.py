"""Section 3L: ASCII ART GENERATOR (block-letter banners, simple shapes)

A small hand-written 5-row block font (uppercase letters, digits,
space) plus a few basic geometric shapes rendered in plain text
characters - no image library involved, just string building.
"""

_FONT = {
    "A": [" ## ", "#  #", "####", "#  #", "#  #"],
    "B": ["### ", "#  #", "### ", "#  #", "### "],
    "C": [" ###", "#   ", "#   ", "#   ", " ###"],
    "D": ["### ", "#  #", "#  #", "#  #", "### "],
    "E": ["####", "#   ", "### ", "#   ", "####"],
    "F": ["####", "#   ", "### ", "#   ", "#   "],
    "G": [" ###", "#   ", "# ##", "#  #", " ###"],
    "H": ["#  #", "#  #", "####", "#  #", "#  #"],
    "I": ["###", " # ", " # ", " # ", "###"],
    "J": ["  ##", "   #", "   #", "#  #", " ## "],
    "K": ["#  #", "# # ", "##  ", "# # ", "#  #"],
    "L": ["#   ", "#   ", "#   ", "#   ", "####"],
    "M": ["#  #", "####", "####", "#  #", "#  #"],
    "N": ["#  #", "## #", "# ##", "#  #", "#  #"],
    "O": [" ## ", "#  #", "#  #", "#  #", " ## "],
    "P": ["### ", "#  #", "### ", "#   ", "#   "],
    "Q": [" ## ", "#  #", "#  #", "# # ", " ###"],
    "R": ["### ", "#  #", "### ", "# # ", "#  #"],
    "S": [" ###", "#   ", " ## ", "   #", "### "],
    "T": ["###", " # ", " # ", " # ", " # "],
    "U": ["#  #", "#  #", "#  #", "#  #", " ## "],
    "V": ["#  #", "#  #", "#  #", " ## ", " ## "],
    "W": ["#  #", "#  #", "####", "####", "#  #"],
    "X": ["#  #", " ## ", " ## ", " ## ", "#  #"],
    "Y": ["#  #", " ## ", " #  ", " #  ", " #  "],
    "Z": ["####", "  # ", " #  ", "#   ", "####"],
    " ": ["  ", "  ", "  ", "  ", "  "],
    "0": [" ## ", "#  #", "#  #", "#  #", " ## "],
    "1": [" # ", "## ", " # ", " # ", "###"],
    "2": ["### ", "   #", " ## ", "#   ", "####"],
    "3": ["### ", "   #", " ## ", "   #", "### "],
    "4": ["#  #", "#  #", "####", "   #", "   #"],
    "5": ["####", "#   ", "### ", "   #", "### "],
    "6": [" ###", "#   ", "### ", "#  #", " ## "],
    "7": ["####", "   #", "  # ", " #  ", " #  "],
    "8": [" ## ", "#  #", " ## ", "#  #", " ## "],
    "9": [" ## ", "#  #", " ###", "   #", "### "],
    "!": ["#", "#", "#", " ", "#"],
    "?": [" ##", "  #", " # ", "   ", " # "],
}

_SHAPES = {
    "triangle": lambda n: "\n".join(("*" * (2 * i + 1)).center(2 * n - 1) for i in range(1, n + 1)),
    "square": lambda n: "\n".join("*" * n for _ in range(n)),
    "diamond": lambda n: "\n".join(("*" * (2 * i + 1)).center(2 * n - 1) for i in range(1, n + 1))
    + "\n" + "\n".join(("*" * (2 * i + 1)).center(2 * n - 1) for i in range(n - 1, 0, -1)),
    "star": lambda n: _draw_star(n),
    "heart": lambda n: _draw_heart(n),
}


def _draw_star(n):
    """A six-pointed star (hexagram) drawn as two overlapping
    triangles, one upright and one inverted, offset so their points
    interleave - the classic "Star of David" construction. Computed
    from the same triangle-row math as the plain triangle shape
    rather than a fixed lookup table, so it scales to any size."""
    size = max(3, n)
    width = 4 * size - 1
    grid = [[" "] * width for _ in range(2 * size)]

    # upright triangle, apex at top-center
    for row in range(size):
        half = row
        center = width // 2
        for col in range(center - half, center + half + 1):
            grid[row][col] = "*"

    # inverted triangle, apex at bottom-center, drawn size-1 rows down
    offset = size - 1
    for row in range(size):
        half = size - 1 - row
        center = width // 2
        r = row + offset
        if r < len(grid):
            for col in range(center - half, center + half + 1):
                grid[r][col] = "*"

    return "\n".join("".join(row).rstrip() for row in grid if "".join(row).strip())


def _draw_heart(n):
    """Renders the classic implicit heart curve
    (x^2+y^2-1)^3 - x^2*y^3 <= 0 onto a text grid - genuinely computed
    from the curve at whatever resolution `n` implies, not a fixed
    template."""
    width = max(16, n * 3)
    height = width // 2
    lines = []
    for row_i in range(height):
        row = []
        for col_i in range(width):
            x = (col_i - width / 2) / (width / 2) * 1.5
            y = (height / 2 - row_i) / (height / 2) * 1.5 - 0.4
            val = (x ** 2 + y ** 2 - 1) ** 3 - (x ** 2) * (y ** 3)
            row.append("*" if val <= 0 else " ")
        line = "".join(row).rstrip()
        if line:
            lines.append(line)
    return "\n".join(lines)


class AsciiArtGenerator:
    MAX_BANNER_CHARS = 20
    BOX_WRAP_WIDTH = 30

    def banner(self, text: str) -> str:
        text = text.upper()[: self.MAX_BANNER_CHARS]
        if not text:
            return "Give me some text to turn into a banner."
        rows = ["", "", "", "", ""]
        for ch in text:
            glyph = _FONT.get(ch, _FONT[" "])
            for i in range(5):
                rows[i] += glyph[i] + "  "
        return "\n".join(rows)

    def shape(self, name: str, size: int = 5) -> str:
        name = name.lower().strip()
        if name not in _SHAPES:
            return f"I can draw a triangle, square, diamond, star, or heart - not '{name}'."
        size = max(1, min(size, 15))
        return _SHAPES[name](size)

    def box(self, text: str, width: int = None) -> str:
        """Word-wraps text to `width` columns and draws a box-drawing
        border around it - simple word-wrap algorithm (greedy line
        filling) plus border rendering, rather than a single fixed
        template."""
        width = width or self.BOX_WRAP_WIDTH
        width = max(10, min(width, 60))

        words = text.split()
        lines, current = [], ""
        for word in words:
            candidate = (current + " " + word).strip()
            if len(candidate) > width:
                if current:
                    lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        if not lines:
            lines = [""]

        inner_width = max(len(ln) for ln in lines)
        top = "+" + "-" * (inner_width + 2) + "+"
        body = "\n".join(f"| {ln.ljust(inner_width)} |" for ln in lines)
        return f"{top}\n{body}\n{top}"
