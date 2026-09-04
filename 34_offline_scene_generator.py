"""Offline procedural scene generator for richer image experiments."""

import math
import random
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class OfflineSceneGenerator:
    """Create stylized backgrounds locally with Pillow and no network calls."""

    THEMES = (
        "sunset", "sunrise", "ocean", "forest", "space", "city", "mountain",
        "desert", "aurora", "rainy", "garden", "winter",
    )
    SIZE = (768, 512)

    TRAINING_EXAMPLES = {
        "sunset": ("golden hour", "warm evening sky", "orange sun over hills", "pink dusk", "twilight landscape"),
        "sunrise": ("dawn over the sea", "first light", "early morning glow", "sun coming up", "pink morning sky"),
        "ocean": ("tropical beach", "calm sea", "waves and horizon", "coastal water", "sun over the ocean"),
        "forest": ("misty pine woods", "deep green woodland", "trees and moss", "quiet forest path", "dense jungle"),
        "space": ("galaxy stars", "moon in deep space", "cosmic planet", "nebula", "astronaut sky"),
        "city": ("urban skyline", "downtown buildings", "city street at night", "metropolis", "tower blocks"),
        "mountain": ("snowy mountain range", "alpine valley", "rocky peaks", "hiking above the clouds", "mountain lake"),
        "desert": ("sand dunes", "arid desert", "cactus landscape", "dusty sunset desert", "oasis"),
        "aurora": ("northern lights", "green aurora borealis", "polar night sky", "colorful arctic lights", "aurora over snow"),
        "rainy": ("rain on glass", "stormy afternoon", "wet street reflections", "cloudy rain", "umbrellas in the rain"),
        "garden": ("spring garden", "flowers and butterflies", "botanical garden", "greenhouse plants", "cottage garden"),
        "winter": ("snowy cabin", "icy mountain morning", "frozen lake", "winter forest", "snow covered village"),
    }

    def __init__(self):
        prompts, labels = [], []
        for theme, examples in self.TRAINING_EXAMPLES.items():
            prompts.extend(examples)
            labels.extend([theme] * len(examples))
        self.classifier = LogisticRegression(max_iter=500, random_state=42)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        self.classifier.fit(self.vectorizer.fit_transform(prompts), labels)

    def classify_prompt(self, prompt: str) -> str:
        """Classify varied natural-language scene requests locally."""
        return str(self.classifier.predict(self.vectorizer.transform([prompt]))[0])

    def generate(self, prompt: str, output_path: str, seed: int = None) -> str:
        theme = self.classify_prompt(prompt)
        rng = random.Random(seed if seed is not None else prompt)
        image = Image.new("RGB", self.SIZE)
        draw = ImageDraw.Draw(image)
        self._paint_sky(draw, theme)
        if theme == "sunset":
            self._paint_sunset(draw, rng)
        elif theme == "sunrise":
            self._paint_sunrise(draw, rng)
        elif theme == "ocean":
            self._paint_ocean(draw, rng)
        elif theme == "forest":
            self._paint_forest(draw, rng)
        elif theme == "space":
            self._paint_space(draw, rng)
        elif theme == "mountain":
            self._paint_mountain(draw, rng)
        elif theme == "desert":
            self._paint_desert(draw, rng)
        elif theme == "aurora":
            self._paint_aurora(draw, rng)
        elif theme == "rainy":
            self._paint_rainy(draw, rng)
        elif theme == "garden":
            self._paint_garden(draw, rng)
        elif theme == "winter":
            self._paint_winter(draw, rng)
        else:
            self._paint_city(draw, rng)
        image = image.filter(ImageFilter.GaussianBlur(radius=0.35))
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return f"Generated an offline {theme} background with Pillow procedural rendering and saved it to {output_path}."

    def _paint_sky(self, draw, theme):
        palettes = {
            "sunset": ((246, 170, 119), (47, 63, 100)),
            "sunrise": ((255, 208, 132), (93, 141, 177)),
            "ocean": ((106, 196, 213), (19, 74, 110)),
            "forest": ((157, 193, 163), (29, 67, 67)),
            "space": ((21, 29, 68), (5, 7, 22)),
            "city": ((176, 188, 204), (33, 43, 67)),
            "mountain": ((152, 202, 218), (55, 83, 99)),
            "desert": ((247, 193, 123), (119, 66, 54)),
            "aurora": ((17, 56, 83), (5, 17, 39)),
            "rainy": ((119, 143, 160), (45, 59, 76)),
            "garden": ((191, 220, 174), (71, 123, 91)),
            "winter": ((190, 220, 239), (64, 91, 125)),
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

    def _paint_sunrise(self, draw, rng):
        draw.ellipse((440, 225, 590, 375), fill=(255, 236, 169))
        self._paint_hills(draw, rng, 355, (69, 83, 94))
        self._paint_hills(draw, rng, 415, (31, 59, 68))
        for _ in range(12):
            x = rng.randint(0, self.SIZE[0])
            y = rng.randint(120, 280)
            draw.arc((x, y, x + rng.randint(25, 70), y + 10), 180, 355, fill=(255, 220, 166), width=2)

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

    def _paint_mountain(self, draw, rng):
        self._paint_hills(draw, rng, 365, (38, 64, 77))
        self._paint_hills(draw, rng, 435, (25, 49, 56))
        for x in range(-40, 800, 170):
            peak = rng.randint(130, 230)
            draw.polygon([(x, 420), (x + 90, peak), (x + 210, 420)], fill=(65, 92, 101))
            draw.polygon([(x + 90, peak), (x + 58, peak + 65), (x + 112, peak + 42)], fill=(230, 236, 226))

    def _paint_desert(self, draw, rng):
        draw.ellipse((510, 105, 635, 230), fill=(255, 226, 153))
        self._paint_hills(draw, rng, 350, (188, 117, 72))
        self._paint_hills(draw, rng, 420, (151, 82, 61))
        draw.rectangle((105, 300, 120, 445), fill=(46, 91, 61))
        draw.arc((70, 280, 155, 350), 180, 360, fill=(46, 91, 61), width=12)

    def _paint_aurora(self, draw, rng):
        for _ in range(7):
            x = rng.randint(-80, 600)
            points = [(x, 340), (x + 100, rng.randint(90, 180)), (x + 230, rng.randint(160, 270)), (x + 340, 340)]
            draw.line(points, fill=rng.choice(((67, 220, 157), (91, 169, 239), (176, 105, 219))), width=rng.randint(12, 26), joint="curve")
        self._paint_hills(draw, rng, 390, (9, 27, 38))
        for _ in range(55):
            x, y = rng.randrange(768), rng.randrange(330)
            draw.point((x, y), fill=(220, 239, 231))

    def _paint_rainy(self, draw, rng):
        draw.rectangle((0, 385, 768, 512), fill=(31, 45, 57))
        for _ in range(100):
            x = rng.randrange(768)
            y = rng.randrange(380)
            draw.line((x, y, x - 9, y + 26), fill=(178, 202, 215), width=1)
        for x in range(35, 760, 85):
            draw.line((x, 420, x + 55, 420), fill=(83, 132, 161), width=3)
            draw.line((x + 20, 440, x + 85, 440), fill=(202, 126, 104), width=2)

    def _paint_garden(self, draw, rng):
        self._paint_hills(draw, rng, 345, (73, 130, 83))
        for _ in range(65):
            x = rng.randrange(768)
            y = rng.randint(330, 500)
            stem = rng.randint(15, 70)
            draw.line((x, y, x, y - stem), fill=(38, 102, 59), width=2)
            flower = rng.choice(((235, 111, 126), (245, 214, 99), (169, 130, 226), (244, 240, 220)))
            draw.ellipse((x - 5, y - stem - 5, x + 5, y - stem + 5), fill=flower)

    def _paint_winter(self, draw, rng):
        self._paint_hills(draw, rng, 335, (88, 118, 143))
        self._paint_hills(draw, rng, 405, (44, 68, 91))
        draw.rectangle((0, 405, self.SIZE[0], self.SIZE[1]), fill=(222, 235, 242))
        for _ in range(90):
            x, y = rng.randrange(self.SIZE[0]), rng.randrange(360)
            radius = rng.choice((1, 1, 2, 3))
            draw.ellipse((x, y, x + radius, y + radius), fill=(245, 250, 255))
        draw.rectangle((140, 330, 300, 425), fill=(101, 62, 48))
        draw.polygon([(120, 335), (220, 265), (320, 335)], fill=(70, 55, 61))
        draw.polygon([(145, 322), (220, 270), (295, 322)], fill=(236, 243, 245))

    @staticmethod
    def _paint_hills(draw, rng, base, color):
        points = [(0, base)]
        for x in range(0, 801, 80):
            points.append((x, base - rng.randint(20, 115)))
        points.extend(((768, 512), (0, 512)))
        draw.polygon(points, fill=color)
