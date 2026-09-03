"""Offline procedural scene generator for richer image experiments."""

import math
import random
from pathlib import Path


class OfflineSceneGenerator:
    """Create stylized backgrounds locally with Pillow and no network calls."""

    THEMES = ("sunset", "ocean", "forest", "space", "city")
    SIZE = (768, 512)

    def generate(self, prompt: str, output_path: str, seed: int = None) -> str:
        words = prompt.lower().split()
        theme = next((name for name in self.THEMES if name in words), "sunset")
        rng = random.Random(seed if seed is not None else prompt)
        image = Image.new("RGB", self.SIZE)
        draw = ImageDraw.Draw(image)
        self._paint_sky(draw, theme)
        if theme == "sunset":
            self._paint_sunset(draw, rng)
        elif theme == "ocean":
            self._paint_ocean(draw, rng)
        elif theme == "forest":
            self._paint_forest(draw, rng)
        elif theme == "space":
            self._paint_space(draw, rng)
        else:
            self._paint_city(draw, rng)
        image = image.filter(ImageFilter.GaussianBlur(radius=0.35))
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return f"Generated an offline {theme} background with Pillow procedural rendering and saved it to {output_path}."

    def _paint_sky(self, draw, theme):
        palettes = {
            "sunset": ((246, 170, 119), (47, 63, 100)),
            "ocean": ((106, 196, 213), (19, 74, 110)),
            "forest": ((157, 193, 163), (29, 67, 67)),
            "space": ((21, 29, 68), (5, 7, 22)),
            "city": ((176, 188, 204), (33, 43, 67)),
        }
        top, bottom = palettes[theme]
        for y in range(self.SIZE[1]):
            ratio = y / (self.SIZE[1] - 1)
            color = tuple(int(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
            draw.line((0, y, self.SIZE[0], y), fill=color)

    def _paint_sunset(self, draw, rng):
        draw.ellipse((500, 170, 650, 320), fill=(255, 220, 143))
        self._paint_hills(draw, rng, 335, (48, 55, 71))
        self._paint_hills(draw, rng, 390, (24, 38, 47))
        for _ in range(18):
            x = rng.randint(0, self.SIZE[0])
            y = rng.randint(80, 280)
            draw.ellipse((x, y, x + rng.randint(12, 40), y + 5), fill=(246, 185, 153))

    def _paint_ocean(self, draw, rng):
        horizon = 285
        draw.ellipse((500, 95, 610, 205), fill=(255, 229, 155))
        draw.rectangle((0, horizon, self.SIZE[0], self.SIZE[1]), fill=(21, 104, 135))
        for _ in range(45):
            y = rng.randint(horizon + 8, self.SIZE[1] - 14)
            x = rng.randint(0, self.SIZE[0] - 80)
            draw.arc((x, y, x + rng.randint(35, 150), y + 15), 180, 355, fill=(82, 178, 188), width=2)
        self._paint_hills(draw, rng, horizon - 25, (29, 67, 83))

    def _paint_forest(self, draw, rng):
        self._paint_hills(draw, rng, 310, (35, 86, 74))
        self._paint_hills(draw, rng, 385, (18, 55, 53))
        for _ in range(32):
            x = rng.randint(-20, self.SIZE[0])
            base = rng.randint(420, 510)
            height = rng.randint(70, 220)
            color = rng.choice(((20, 67, 61), (29, 90, 68), (43, 111, 77)))
            draw.polygon([(x, base - height), (x - 38, base), (x + 38, base)], fill=color)
            draw.rectangle((x - 4, base - 8, x + 5, base + 20), fill=(38, 55, 47))

    def _paint_space(self, draw, rng):
        for _ in range(130):
            x, y = rng.randrange(self.SIZE[0]), rng.randrange(390)
            radius = rng.choice((1, 1, 1, 2))
            draw.ellipse((x, y, x + radius, y + radius), fill=(220, 231, 255))
        draw.ellipse((485, 90, 620, 225), fill=(196, 160, 239))
        draw.ellipse((510, 120, 595, 205), fill=(107, 84, 158))
        draw.arc((420, 130, 680, 220), 165, 345, fill=(235, 197, 130), width=7)
        draw.polygon([(0, 430), (170, 320), (330, 430)], fill=(12, 16, 38))

    def _paint_city(self, draw, rng):
        horizon = 375
        draw.rectangle((0, horizon, self.SIZE[0], self.SIZE[1]), fill=(27, 35, 51))
        x = -10
        while x < self.SIZE[0]:
            width = rng.randint(35, 90)
            height = rng.randint(80, 240)
            top = horizon - height
            draw.rectangle((x, top, x + width, horizon), fill=rng.choice(((35, 48, 68), (43, 55, 75), (56, 64, 83))))
            for wx in range(x + 10, x + width - 5, 18):
                for wy in range(top + 15, horizon - 10, 24):
                    if rng.random() > 0.38:
                        draw.rectangle((wx, wy, wx + 5, wy + 7), fill=(244, 199, 111))
            x += width + rng.randint(4, 12)
        draw.line((0, horizon, self.SIZE[0], horizon), fill=(235, 177, 112), width=2)

    @staticmethod
    def _paint_hills(draw, rng, base, color):
        points = [(0, base)]
        for x in range(0, 801, 80):
            points.append((x, base - rng.randint(20, 115)))
        points.extend(((768, 512), (0, 512)))
        draw.polygon(points, fill=color)
