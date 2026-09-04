"""Offline procedural scene generator - high quality Pillow renderer."""

import random
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class OfflineSceneGenerator:
    """Create high-quality stylized backgrounds locally with Pillow."""

    THEMES = (
        "sunset", "sunrise", "ocean", "forest", "space", "city", "mountain",
        "desert", "aurora", "rainy", "garden", "winter",
    )
    SIZE = (1536, 1024)  # 2x resolution
    SUPER_SAMPLE = 2  # render at 2x then downsample for anti-aliasing

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

        # Pre-compute noise tables for procedural detail
        self._noise_cache = {}
        self._gradients = {}

    def _noise2d(self, x, y, scale=1.0, octaves=4, persistence=0.5):
        """Simple value noise for procedural detail."""
        key = (int(x * scale), int(y * scale))
        if key in self._noise_cache:
            return self._noise_cache[key]
        # Simple hash-based noise
        n = hash((int(x * scale * 100), int(y * scale * 100))) / 2**64
        self._noise_cache[key] = n * 2 - 1
        return self._noise_cache[key]

    def _fbm(self, x, y, octaves=4, persistence=0.5, lacunarity=2.0):
        """Fractal Brownian Motion for natural noise."""
        value = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_val = 0.0
        for _ in range(octaves):
            value += amplitude * self._noise2d(x * frequency, y * frequency)
            max_val += amplitude
            amplitude *= persistence
            frequency *= lacunarity
        return value / max_val if max_val > 0 else 0

    def _radial_gradient(self, w, h, cx, cy, inner_color, outer_color, power=1.5):
        """Create a radial gradient mask."""
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        max_dist = math.hypot(w, h)
        for y in range(h):
            for x in range(w):
                dist = math.hypot(x - cx, y - cy) / max_dist
                t = 1 - min(dist ** power, 1.0)
                r = int(inner_color[0] * t + outer_color[0] * (1 - t))
                g = int(inner_color[1] * t + outer_color[1] * (1 - t))
                b = int(inner_color[2] * t + outer_color[2] * (1 - t))
                a = int(255 * t)
                draw.point((x, y), fill=(r, g, b, a))
        return img

    def _linear_gradient(self, w, h, top_color, bottom_color):
        """Vertical linear gradient."""
        img = Image.new('RGB', (w, h))
        for y in range(h):
            t = y / max(h - 1, 1)
            r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
            g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
            b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
            for x in range(w):
                img.putpixel((x, y), (r, g, b))
        return img

    def classify_prompt(self, prompt: str) -> str:
        """Classify varied natural-language scene requests locally."""
        normalized = prompt.lower().replace("nighttime", "night").replace("snow-covered", "snow covered")
        aliases = {
            "dawn": "first light sunrise",
            "morning": "early morning sunrise",
            "icy": "winter frozen",
            "snowy": "winter snow covered",
            "woods": "forest woodland",
            "skyline": "city urban skyline",
            "coast": "ocean coastal water",
            "beach": "ocean tropical beach",
            "cyberpunk": "city neon metropolis",
            "deserted": "desert arid",
        }
        for source, replacement in aliases.items():
            normalized = normalized.replace(source, replacement)
        high_signal_themes = (
            ("aurora", ("aurora", "northern lights", "borealis")),
            ("winter", ("winter", "snow", "snowy", "icy", "frozen")),
            ("sunrise", ("sunrise", "dawn", "first light", "morning glow")),
            ("rainy", ("rain", "rainy", "storm", "wet street", "umbrellas")),
            ("desert", ("desert", "dunes", "cactus", "oasis")),
        )
        for theme, cues in high_signal_themes:
            if any(cue in normalized for cue in cues):
                return theme
        return str(self.classifier.predict(self.vectorizer.transform([normalized]))[0])

    def generate(self, prompt: str, output_path: str, seed: int = None) -> str:
        theme = self.classify_prompt(prompt)
        rng = random.Random(seed if seed is not None else prompt)

        # Render at super-sampled resolution for quality
        sw, sh = self.SIZE[0] * self.SUPER_SAMPLE, self.SIZE[1] * self.SUPER_SAMPLE
        image = Image.new("RGBA", (sw, sh), (0, 0, 0, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        # Layer 0: Sky gradient with atmospheric scattering
        self._paint_sky(draw, theme, sw, sh, rng)

        # Layer 1: Far background (mountains, distant hills, stars)
        self._paint_far_background(draw, theme, sw, sh, rng)

        # Layer 2: Mid-ground (hills, treelines, city silhouettes)
        self._paint_midground(draw, theme, sw, sh, rng)

        # Layer 3: Foreground details (trees, rocks, grass, buildings)
        self._paint_foreground(draw, theme, sw, sh, rng)

        # Layer 4: Atmospheric effects (fog, rain, snow, aurora, god rays)
        self._paint_atmosphere(draw, theme, sw, sh, rng)

        # Layer 5: Celestial bodies (sun, moon, planets)
        self._paint_celestial(draw, theme, sw, sh, rng)

        # Downsample with high-quality filter
        image = image.resize(self.SIZE, Image.Resampling.LANCZOS)

        # Color grading / tone mapping
        image = self._color_grade(image, theme)

        # Convert to RGB for saving
        if image.mode == 'RGBA':
            bg = Image.new('RGB', image.size, (0, 0, 0))
            bg.paste(image, mask=image.split()[3])
            image = bg
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, quality=95)
        return f"Generated an offline {theme} background with Pillow procedural rendering and saved it to {output_path}."

    def _paint_sky(self, draw, theme, w, h, rng):
        """Multi-layer sky with atmospheric scattering."""
        palettes = {
            "sunset": ((255, 90, 40), (255, 160, 60), (255, 200, 100), (80, 40, 60), (20, 15, 35)),
            "sunrise": ((255, 140, 80), (255, 190, 120), (255, 220, 160), (100, 70, 90), (30, 25, 50)),
            "ocean": ((100, 180, 220), (60, 140, 200), (30, 100, 180), (15, 60, 120), (5, 20, 60)),
            "forest": ((140, 200, 160), (90, 160, 130), (50, 120, 90), (25, 70, 60), (10, 30, 25)),
            "space": ((10, 10, 30), (5, 5, 20), (2, 2, 15), (0, 0, 10), (0, 0, 5)),
            "city": ((180, 190, 210), (130, 150, 180), (90, 110, 140), (40, 60, 90), (15, 25, 45)),
            "mountain": ((160, 200, 230), (110, 160, 200), (70, 120, 170), (35, 70, 110), (15, 30, 60)),
            "desert": ((255, 180, 90), (255, 210, 130), (255, 230, 170), (180, 100, 50), (80, 40, 30)),
            "aurora": ((15, 25, 50), (10, 20, 45), (5, 15, 40), (2, 10, 35), (0, 5, 20)),
            "rainy": ((100, 130, 150), (70, 100, 120), (45, 70, 95), (25, 45, 65), (10, 20, 35)),
            "garden": ((160, 220, 180), (110, 180, 140), (70, 140, 100), (35, 90, 65), (15, 45, 30)),
            "winter": ((180, 210, 240), (140, 180, 220), (100, 150, 200), (60, 100, 150), (25, 50, 90)),
        }
        colors = palettes.get(theme, palettes["city"])

        # Multi-stop gradient
        for y in range(draw.im.size[1]):
            t = y / max(h - 1, 1)
            # Smooth interpolation through color stops
            if t < 0.2:
                u = t / 0.2
                c1, c2 = colors[0], colors[1]
            elif t < 0.4:
                u = (t - 0.2) / 0.2
                c1, c2 = colors[1], colors[2]
            elif t < 0.6:
                u = (t - 0.4) / 0.2
                c1, c2 = colors[2], colors[3]
            elif t < 0.8:
                u = (t - 0.6) / 0.2
                c1, c2 = colors[3], colors[4]
            else:
                u = (t - 0.8) / 0.2
                c1, c2 = colors[4], colors[4]
            u = u * u * (3 - 2 * u)  # smoothstep
            r = int(c1[0] * (1 - u) + c2[0] * u)
            g = int(c1[1] * (1 - u) + c2[1] * u)
            b = int(c1[2] * (1 - u) + c2[2] * u)
            draw.line((0, y, w, y), fill=(r, g, b, 255))

    def _paint_far_background(self, draw, theme, w, h, rng):
        """Stars, distant mountains, far hills."""
        if theme == "space":
            # Star field with varying magnitudes
            for _ in range(800):
                x = rng.randrange(w)
                y = rng.randrange(h // 2)
                mag = rng.random()
                if mag < 0.6:
                    r = rng.randint(1, 1)
                    brightness = rng.randint(80, 160)
                elif mag < 0.9:
                    r = rng.randint(1, 2)
                    brightness = rng.randint(160, 230)
                else:
                    r = rng.randint(2, 3)
                    brightness = rng.randint(200, 255)
                color = (brightness, brightness, brightness, brightness)
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

            # Nebulae
            for _ in range(6):
                cx = rng.randint(w // 4, 3 * w // 4)
                cy = rng.randint(h // 6, h // 3)
                rx = rng.randint(w // 6, w // 3)
                ry = rng.randint(h // 8, h // 4)
                hue = rng.random()
                for _ in range(1000):
                    angle = rng.random() * 2 * math.pi
                    radius = rng.random() ** 0.5
                    px = int(cx + math.cos(angle) * rx * radius)
                    py = int(cy + math.sin(angle) * ry * radius)
                    if 0 <= px < w and 0 <= py < h:
                        intensity = int(60 * (1 - radius) * rng.random())
                        if hue < 0.33:
                            color = (intensity, intensity // 3, intensity // 2, 180)
                        elif hue < 0.66:
                            color = (intensity // 2, intensity, intensity // 3, 180)
                        else:
                            color = (intensity // 3, intensity // 2, intensity, 180)
                        draw.point((px, py), fill=color)

        elif theme in ("sunset", "sunrise", "desert", "mountain", "ocean"):
            # Distant mountain ridges
            for layer in range(3):
                alpha = 60 + layer * 30
                color_base = {
                    "sunset": (60, 40, 50),
                    "sunrise": (70, 50, 60),
                    "desert": (120, 80, 60),
                    "mountain": (50, 70, 90),
                    "ocean": (30, 50, 80),
                }.get(theme, (50, 50, 70))
                offset = layer * 40
                points = [(0, h // 2 + offset)]
                for x in range(0, w + 1, w // 20):
                    points.append((x, h // 2 + offset - rng.randint(30, 100) * (layer + 1)))
                points.extend([(w, h), (0, h)])
                color = (*color_base, 40 + layer * 20)
                draw.polygon(points, fill=color)

    def _paint_midground(self, draw, theme, w, h, rng):
        """Hills, treelines, city silhouettes."""
        if theme in ("forest", "garden", "mountain", "sunset", "sunrise"):
            # Layered hills with trees
            for layer in range(4):
                base_y = h * (0.55 + layer * 0.1)
                color_dark = {
                    "forest": (15, 45, 25),
                    "garden": (25, 60, 30),
                    "mountain": (25, 40, 35),
                    "sunset": (30, 20, 25),
                    "sunrise": (35, 25, 30),
                }.get(theme, (20, 30, 25))
                alpha = 180 + layer * 15
                color = (*color_dark, alpha)

                # Hill silhouette
                points = [(0, h)]
                for x in range(0, w + 1, w // 15):
                    points.append((x, base_y - rng.randint(20, 80) * (layer + 1)))
                points.append((w, h))
                draw.polygon(points, fill=color)

                # Tree silhouettes on hill
                for _ in range(15 + layer * 5):
                    tx = rng.randint(0, w)
                    ty = int(base_y - rng.randint(10, 50))
                    tw = rng.randint(20, 50)
                    th = rng.randint(60, 150)
                    # Simple pine tree
                    trunk_color = (*color_dark[:3], alpha)
                    draw.rectangle((tx + tw//2 - 3, ty, tx + tw//2 + 3, ty + th//3), fill=trunk_color)
                    for i in range(4):
                        layer_y = ty - i * (th * 2 // 5)
                        layer_w = tw + i * 10
                        draw.polygon([
                            (tx + tw//2, layer_y - th//4),
                            (tx - layer_w//2, layer_y + th//6),
                            (tx + tw//2 + layer_w//2, layer_y + th//6)
                        ], fill=color)

        elif theme == "city":
            # Building silhouettes
            x = -50
            while x < w:
                width = rng.randint(60, 180)
                height = rng.randint(150, 500)
                top = int(h * 0.6) - height
                color = rng.choice([
                    (20, 28, 45, 230),
                    (30, 38, 55, 220),
                    (40, 48, 65, 210),
                ])
                draw.rectangle((x, top, x + width, h), fill=color)
                # Windows
                for wx in range(x + 15, x + width - 10, 24):
                    for wy in range(top + 20, h - 20, 30):
                        if rng.random() > 0.4:
                            win_color = (255, 220, 120, 200)
                            draw.rectangle((wx, wy, wx + 8, wy + 14), fill=win_color)
                x += width + rng.randint(8, 20)

    def _paint_foreground(self, draw, theme, w, h, rng):
        """Detailed foreground elements."""
        if theme in ("forest", "garden"):
            # Detailed trees with branches
            for _ in range(8):
                tx = rng.randint(50, w - 50)
                base_y = rng.randint(int(h * 0.7), h - 50)
                self._draw_detailed_tree(draw, tx, base_y, rng, theme)

        elif theme == "ocean":
            # Waves with foam
            for layer in range(5):
                y = h - 80 - layer * 25
                alpha = 180 - layer * 30
                for _ in range(20):
                    x = rng.randint(-50, w + 50)
                    wx = rng.randint(60, 200)
                    draw.arc((x, y, x + wx, y + 40), 180, 360,
                             fill=(255, 255, 255, alpha), width=3)

            # Shoreline foam
            for _ in range(30):
                x = rng.randint(0, w)
                y = h - rng.randint(60, 100)
                draw.ellipse((x - 15, y - 8, x + 15, y + 8),
                             fill=(255, 255, 255, 180))

        elif theme == "desert":
            # Sand dunes with shadows
            for _ in range(5):
                cx = rng.randint(100, w - 100)
                cy = rng.randint(int(h * 0.65), h - 50)
                rx = rng.randint(80, 200)
                ry = rng.randint(30, 60)
                for angle in range(0, 180, 5):
                    rad = math.radians(angle)
                    px = int(cx + math.cos(rad) * rx)
                    py = int(cy + math.sin(rad) * ry)
                    if px < w and py < h:
                        shadow = (40, 25, 15, 100)
                        draw.ellipse((px - 20, py + 10, px + 20, py + 30), fill=shadow)

        elif theme == "winter":
            # Snow-covered trees
            for _ in range(6):
                tx = rng.randint(50, w - 50)
                base_y = rng.randint(int(h * 0.7), h - 50)
                self._draw_snow_tree(draw, tx, base_y, rng)

        elif theme == "rainy":
            # Puddles with reflections
            for _ in range(12):
                px = rng.randint(50, w - 50)
                py = rng.randint(int(h * 0.75), h - 30)
                rx = rng.randint(40, 120)
                ry = rng.randint(15, 35)
                draw.ellipse((px - rx, py - ry, px + rx, py + ry),
                             fill=(20, 35, 50, 180))
                # Reflection highlight
                draw.ellipse((px - rx//2, py - ry//2, px + rx//3, py + ry//3),
                             fill=(80, 120, 160, 60))

    def _draw_detailed_tree(self, draw, x, base_y, rng, theme):
        """Procedural tree with trunk and branching canopy."""
        trunk_color = (40, 25, 15, 230) if theme == "forest" else (50, 35, 20, 230)
        canopy_color = (20, 70, 35, 220) if theme == "forest" else (40, 100, 50, 220)

        # Trunk
        draw.rectangle((x - 6, base_y, x + 6, base_y + 80), fill=trunk_color)

        # Branching canopy using recursive-like approach
        branches = [(x, base_y, -math.pi/2, 120, 0)]
        for _ in range(60):
            if not branches:
                break
            bx, by, angle, length, depth = branches.pop(rng.randrange(len(branches)))
            if length < 5 or depth > 5:
                continue

            nx = bx + math.cos(angle) * length
            ny = by + math.sin(angle) * length
            width = max(1, int(length * 0.15))

            # Draw branch
            draw.line((bx, by, nx, ny), fill=canopy_color, width=width)

            # Split
            if rng.random() < 0.7 and depth < 4:
                branches.append((nx, ny, angle + rng.uniform(-0.8, -0.3), length * 0.7, depth + 1))
                branches.append((nx, ny, angle + rng.uniform(0.3, 0.8), length * 0.7, depth + 1))
            else:
                branches.append((nx, ny, angle + rng.uniform(-0.4, 0.4), length * 0.8, depth + 1))

    def _draw_snow_tree(self, draw, x, base_y, rng):
        """Snow-covered conifer."""
        # Trunk
        draw.rectangle((x - 4, base_y, x + 4, base_y + 60), fill=(50, 40, 35, 220))

        # Snow layers
        for i in range(5):
            layer_y = base_y - i * 30
            layer_w = 50 + i * 25
            # Snow
            draw.polygon([
                (x, layer_y - 25),
                (x - layer_w, layer_y + 15),
                (x + layer_w, layer_y + 15)
            ], fill=(250, 252, 255, 240))
            # Snow on branches
            draw.line((x - layer_w, layer_y + 15, x + layer_w, layer_y + 15),
                      fill=(255, 255, 255, 220), width=3)

    def _paint_atmosphere(self, draw, theme, w, h, rng):
        """Fog, mist, rain, snow, aurora, god rays."""
        if theme in ("forest", "mountain", "winter"):
            # Ground fog / mist layers
            for layer in range(3):
                y = h - 100 - layer * 60
                for _ in range(200):
                    fx = rng.randrange(w)
                    fy = y + rng.randint(-30, 30)
                    alpha = rng.randint(15, 40)
                    draw.ellipse((fx - 40, fy - 10, fx + 40, fy + 10),
                                 fill=(255, 255, 255, alpha))

        if theme == "aurora":
            # Aurora curtains
            for _ in range(8):
                x = rng.randint(-100, w - 100)
                points = []
                for i in range(15):
                    px = x + i * (w // 15) + rng.randint(-30, 30)
                    py = rng.randint(50, 250)
                    points.append((px, py))
                if len(points) > 2:
                    color = rng.choice([
                        (80, 240, 160, 120),
                        (100, 180, 255, 120),
                        (180, 120, 240, 120),
                    ])
                    # Draw as thick lines
                    for i in range(len(points) - 1):
                        draw.line((points[i], points[i+1]), fill=color, width=rng.randint(8, 20), joint="curve")

        if theme == "rainy":
            # Rain streaks
            for _ in range(300):
                x = rng.randrange(w)
                y = rng.randrange(h - 100)
                length = rng.randint(15, 35)
                alpha = rng.randint(40, 100)
                draw.line((x, y, x - 8, y + length), fill=(180, 200, 220, alpha), width=1)

            # Ground splashes
            for _ in range(40):
                x = rng.randint(50, w - 50)
                y = h - rng.randint(30, 80)
                draw.ellipse((x - 3, y - 2, x + 3, y + 2),
                             fill=(200, 220, 240, 150))

        if theme == "winter":
            # Falling snow
            for _ in range(250):
                x = rng.randrange(w)
                y = rng.randrange(h // 2)
                size = rng.choice([1, 1, 2, 2, 3])
                alpha = rng.randint(120, 220)
                draw.ellipse((x - size, y - size, x + size, y + size),
                             fill=(255, 255, 255, alpha))

        if theme in ("sunset", "sunrise"):
            # God rays / crepuscular rays
            sun_x = w * (0.3 if theme == "sunrise" else 0.7)
            sun_y = h * 0.25
            for _ in range(20):
                angle = rng.uniform(-0.8, 0.8)
                length = h * 0.8
                end_x = sun_x + math.cos(angle) * length
                end_y = sun_y + math.sin(angle) * length
                alpha = rng.randint(15, 35)
                draw.line((sun_x, sun_y, end_x, end_y),
                          fill=(255, 220, 150, alpha), width=rng.randint(2, 8))

    def _paint_celestial(self, draw, theme, w, h, rng):
        """Sun, moon, planets."""
        if theme in ("sunset", "sunrise"):
            # Sun with glow
            sun_x = w * (0.7 if theme == "sunset" else 0.3)
            sun_y = h * 0.22
            for r in range(120, 0, -5):
                alpha = max(5, int(80 * (r / 120)))
                if theme == "sunset":
                    color = (255, 180, 60, alpha)
                else:
                    color = (255, 210, 100, alpha)
                draw.ellipse((sun_x - r, sun_y - r, sun_x + r, sun_y + r), fill=color)
            # Core
            draw.ellipse((sun_x - 30, sun_y - 30, sun_x + 30, sun_y + 30),
                         fill=(255, 255, 200, 255))

        elif theme in ("space", "aurora", "winter"):
            # Moon
            moon_x = w * (0.2 if theme == "aurora" else 0.8)
            moon_y = h * 0.15
            for r in range(60, 0, -3):
                alpha = max(20, int(100 * (r / 60)))
                color = (220, 220, 235, alpha)
                draw.ellipse((moon_x - r, moon_y - r, moon_x + r, moon_y + r), fill=color)
            # Moon surface detail
            for _ in range(15):
                mx = moon_x + rng.randint(-35, 35)
                my = moon_y + rng.randint(-35, 35)
                draw.ellipse((mx - 5, my - 5, mx + 5, my + 5),
                             fill=(180, 180, 200, 180))

    def _paint_hills(self, draw, rng, base, color, w=None):
        """Helper for layered hills."""
        if w is None:
            w = draw.im.size[0]
        points = [(0, base)]
        for x in range(0, w + 1, w // 12):
            points.append((x, base - rng.randint(25, 90)))
        points.extend([(w, w), (0, w)])
        draw.polygon(points, fill=color)

    def _color_grade(self, image, theme):
        """Apply cinematic color grading per theme."""
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.15)

        # Enhance color saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)

        # Theme-specific grading
        if theme in ("sunset", "sunrise"):
            # Warm highlights, cool shadows (split toning)
            image = self._split_tone(image,
                highlights=(1.15, 1.05, 0.85),
                shadows=(0.9, 0.95, 1.1))
        elif theme == "space":
            # Cool, high contrast
            image = self._split_tone(image,
                highlights=(0.95, 0.95, 1.15),
                shadows=(0.7, 0.75, 1.0))
        elif theme in ("forest", "garden"):
            # Green push
            image = self._split_tone(image,
                highlights=(0.95, 1.1, 0.9),
                shadows=(0.85, 1.0, 0.85))
        elif theme == "winter":
            # Blue push
            image = self._split_tone(image,
                highlights=(0.9, 0.95, 1.15),
                shadows=(0.8, 0.85, 1.1))
        elif theme == "desert":
            # Warm
            image = self._split_tone(image,
                highlights=(1.15, 1.05, 0.9),
                shadows=(1.05, 0.95, 0.85))
        elif theme == "city":
            # Teal/orange cinematic
            image = self._split_tone(image,
                highlights=(1.1, 1.0, 0.9),
                shadows=(0.85, 0.9, 1.05))

        # Subtle vignette
        image = self._vignette(image, 0.35)

        return image

    def _split_tone(self, image, highlights, shadows):
        """Apply split toning: different color balance for highlights vs shadows."""
        img = image.convert('RGB')
        pixels = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                r, g, b = pixels[x, y]
                lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
                # Normalize luminance
                t = lum / 255.0
                # Smooth transition
                t = t * t * (3 - 2 * t)  # smoothstep
                # Interpolate between shadow and highlight multipliers
                hr, hg, hb = highlights
                sr, sg, sb = shadows
                mr = sr * t + hr * (1 - t)
                mg = sg * t + hg * (1 - t)
                mb = sb * t + hb * (1 - t)
                nr = min(255, int(r * mr))
                ng = min(255, int(g * mg))
                nb = min(255, int(b * mb))
                pixels[x, y] = (nr, ng, nb)
        return img

    def _vignette(self, image, strength=0.3):
        """Subtle vignette."""
        w, h = image.size
        img = image.convert('RGBA')
        pixels = img.load()
        cx, cy = w // 2, h // 2
        max_dist = math.hypot(cx, cy)
        for y in range(h):
            for x in range(w):
                dist = math.hypot(x - cx, y - cy) / max_dist
                if dist > 0.5:
                    v = 1.0 - strength * ((dist - 0.5) / 0.5) ** 1.5
                    r, g, b, a = pixels[x, y]
                    pixels[x, y] = (int(r * v), int(g * v), int(b * v), a)
        return img.convert('RGB')


# For backward compatibility
GENERATOR_SHAPES = ("circle", "square", "triangle", "diamond", "star", "heart")
GENERATOR_COLORS = ("red", "blue", "green", "yellow", "purple", "orange", "pink", "white", "black")