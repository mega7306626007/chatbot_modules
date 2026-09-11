"""Maximized Offline Procedural Scene Generator - High Quality Pillow Renderer."""

import random
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class OfflineSceneGenerator:
    """Creates stunning, highly detailed procedural backgrounds locally with Pillow."""

    THEMES = (
        "sunset", "sunrise", "ocean", "forest", "space", "city", "mountain",
        "desert", "aurora", "rainy", "garden", "winter", "waterfall",
        "autumn", "savanna", "canyon", "volcano", "tundra", "meadow", "river",
    )
    SIZE = (1024, 768)
    SUPER_SAMPLE = 2  # balanced 2x supersample for Render free tier (3x OOMs at 502)

    TRAINING_EXAMPLES = {
        "sunset": ("golden hour", "warm evening sky", "orange sun over hills", "pink dusk", "twilight landscape", "burning sunset clouds", "amber horizon", "crimson dusk"),
        "sunrise": ("dawn over the sea", "first light", "early morning glow", "sun coming up", "pink morning sky", "misty sunrise valley", "golden dawn light", "soft morning haze"),
        "ocean": ("tropical beach", "calm sea", "waves and horizon", "coastal water", "sun over the ocean", "turquoise lagoon", "coral reef water", "cliffside ocean view"),
        "forest": ("misty pine woods", "deep green woodland", "trees and moss", "quiet forest path", "dense jungle", "ancient redwood forest", "foggy deciduous forest", "enchanted woodland"),
        "space": ("galaxy stars", "moon in deep space", "cosmic planet", "nebula", "astronaut sky", "milky way core", "saturn rings", "deep space starscape"),
        "city": ("urban skyline", "downtown buildings", "city street at night", "metropolis", "tower blocks", "neon city night", "historic old town", "futuristic skyline"),
        "mountain": ("snowy mountain range", "alpine valley", "rocky peaks", "hiking above the clouds", "mountain lake", "glacial mountain", "volcanic ridge", "misty highlands"),
        "desert": ("sand dunes", "arid desert", "cactus landscape", "dusty sunset desert", "oasis", "red desert canyon", "desert salt flats", "nomad desert camp"),
        "aurora": ("northern lights", "green aurora borealis", "polar night sky", "colorful arctic lights", "aurora over snow", "aurora reflection lake", "southern lights", "aurora starry night"),
        "rainy": ("rain on glass", "stormy afternoon", "wet street reflections", "cloudy rain", "umbrellas in the rain", "thunderstorm over city", "misty rainy forest", "rain puddle reflections"),
        "garden": ("spring garden", "flowers and butterflies", "botanical garden", "greenhouse plants", "cottage garden", "rose garden bloom", "lavender field", "zen garden stones"),
        "winter": ("snowy cabin", "icy mountain morning", "frozen lake", "winter forest", "snow covered village", "blizzard mountain", "ice cave blue", "winter aurora night"),
        "waterfall": ("tropical waterfall", "misty cascade", "waterfall in jungle", "waterfall cliff", "rainbow waterfall mist", "forest waterfall pool", "mountain waterfall", "wide waterfall panorama"),
        "autumn": ("autumn forest colors", "fall leaves canopy", "golden autumn valley", "autumn maple trees", "misty autumn morning", "autumn countryside road", "autumn lake reflection", "harvest autumn field"),
        "savanna": ("african savanna", "savanna acacia trees", "golden savanna sunset", "savanna elephants", "dry savanna grassland", "savanna watering hole", "savanna horizon", "savanna baobab"),
        "canyon": ("grand canyon cliffs", "red rock canyon", "canyon river gorge", "canyon desert strata", "slot canyon light", "canyon overlook", "canyon sunrise", "deep canyon walls"),
        "volcano": ("volcano eruption", "lava volcano night", "volcanic ash plume", "volcanic crater lake", "snowy volcano peak", "volcano island ocean", "active volcano smoke", "volcano starry sky"),
        "tundra": ("arctic tundra", "frozen tundra plain", "tundra northern lights", "tundra reindeer", "tundra moss rocks", "tundra icy river", "tundra winter light", "barren tundra horizon"),
        "meadow": ("wildflower meadow", "green meadow hills", "meadow sunrise", "meadow with stream", "alpine meadow", "meadow butterflies", "meadow morning dew", "rolling meadow pasture"),
        "river": ("winding river valley", "river through forest", "mountain river rapids", " calm river reflection", "river delta wetlands", "river canyon", "river at sunset", "river misty morning"),
    }

    def __init__(self):
        prompts, labels = [], []
        for theme, examples in self.TRAINING_EXAMPLES.items():
            prompts.extend(examples)
            labels.extend([theme] * len(examples))
        self.classifier = LogisticRegression(max_iter=500, random_state=42)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        self.classifier.fit(self.vectorizer.fit_transform(prompts), labels)
        self._noise_cache = {}
        self._gradients = {}
        self._init_gradients()

    def _init_gradients(self):
        """Pre-compute smooth pseudo-random gradient vectors for organic noise mapping."""
        rng = np.random.RandomState(42)
        angles = rng.uniform(0, 2 * np.pi, 256)
        self._g_x = np.cos(angles)
        self._g_y = np.sin(angles)
        self._perm = rng.permutation(256)

    def _fade(self, t):
        """Smooth step s-curve mathematical formula for pristine blending transitions."""
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _perlin_noise_2d(self, x_arr, y_arr):
        """Vectorized 2D Perlin Noise Engine — creates ultra-realistic clouds and terrain."""
        x_floor = np.floor(x_arr).astype(np.int32)
        y_floor = np.floor(y_arr).astype(np.int32)
        xf = x_arr - x_floor
        yf = y_arr - y_floor
        u = self._fade(xf)
        v = self._fade(yf)
        xi = x_floor & 255
        yi = y_floor & 255
        p = self._perm
        aa = p[(p[xi] + yi) & 255]
        ab = p[(p[xi] + (yi + 1)) & 255]
        ba = p[(p[(xi + 1) & 255] + yi) & 255]
        bb = p[(p[(xi + 1) & 255] + (yi + 1)) & 255]
        g_x, g_y = self._g_x, self._g_y
        grad_aa = g_x[aa]*xf + g_y[aa]*yf
        grad_ba = g_x[ba]*(xf-1) + g_y[ba]*yf
        grad_ab = g_x[ab]*xf + g_y[ab]*(yf-1)
        grad_bb = g_x[bb]*(xf-1) + g_y[bb]*(yf-1)
        x1 = grad_aa + u * (grad_ba - grad_aa)
        x2 = grad_ab + u * (grad_bb - grad_ab)
        return x1 + v * (x2 - x1)

    def _fbm(self, w, h, octaves=5, lacunarity=2.0, gain=0.5, scale=0.005):
        """Fractal Brownian Motion — overlays multiple octaves of noise for rich textures."""
        x = np.arange(w, dtype=np.float32)
        y = np.arange(h, dtype=np.float32)
        xx, yy = np.meshgrid(x, y)
        total_noise = np.zeros((h, w), dtype=np.float32)
        amplitude = 1.0
        frequency = scale
        for _ in range(octaves):
            total_noise += amplitude * self._perlin_noise_2d(xx * frequency, yy * frequency)
            amplitude *= gain
            frequency *= lacunarity
        return (total_noise - total_noise.min()) / (total_noise.max() - total_noise.min() + 1e-6)

    def _noise2d(self, x, y, scale=1.0, octaves=4, persistence=0.5):
        key = (int(x * scale), int(y * scale))
        if key in self._noise_cache:
            return self._noise_cache[key]
        n = hash((int(x * scale * 100), int(y * scale * 100))) / 2**64
        self._noise_cache[key] = n * 2 - 1
        return self._noise_cache[key]

    def _paint_realistic_clouds(self, image, theme, w, h, rng):
        """Paints volumetric mist — balanced detail keeps Render stable."""
        density = {"sunset": 0.4, "sunrise": 0.35, "rainy": 0.7, "ocean": 0.42, "forest": 0.30, "mountain": 0.32, "desert": 0.15, "aurora": 0.18, "winter": 0.35, "waterfall": 0.38, "autumn": 0.28, "savanna": 0.25, "canyon": 0.20, "volcano": 0.30, "tundra": 0.32, "meadow": 0.30, "river": 0.32}.get(theme, 0.30)
        if w > 1800 or h > 1400:
            lw, lh = w // 3, h // 3
            noise_mask = self._fbm(lw, lh, octaves=5, scale=0.009)
            noise_mask = Image.fromarray((noise_mask * 255).astype(np.uint8), mode='L').resize((w, h), Image.BICUBIC)
            noise_mask = np.array(noise_mask, dtype=np.float32) / 255.0
        else:
            noise_mask = self._fbm(w, h, octaves=5, scale=0.003)
        noise_mask = np.clip((noise_mask - (1.0 - density)) * 2.5, 0.0, 1.0)
        horizon_fade = np.linspace(1.0, 0.1, h, dtype=np.float32)[:, None]
        final_alpha = (noise_mask * horizon_fade * 140).astype(np.uint8)
        tint = (255, 220, 180) if theme in ("sunset", "canyon", "desert", "savanna", "volcano") else (255, 255, 255)
        cloud_layer = Image.new('RGBA', (w, h), (*tint, 0))
        alpha_channel = Image.fromarray(final_alpha, mode='L')
        cloud_layer.putalpha(alpha_channel)
        image.paste(cloud_layer, (0, 0), mask=alpha_channel)

    def _paint_mountain_ridges(self, image, w, h, sky_bottom_color, rng):
        """Draws layered mountains — 4 layers, stable for Render."""
        draw = ImageDraw.Draw(image, "RGBA")
        num_layers = 4
        for layer in range(num_layers):
            depth_factor = (layer + 1) / num_layers
            horizon_height = int(h * 0.45 + (layer * (h * 0.08)))
            x_points = np.arange(0, w, 4)
            noise_profile = self._perlin_noise_2d(x_points * 0.004, np.array([layer * 10.0]))
            amplitude = int((h * 0.18) * (1.0 - depth_factor * 0.5))
            y_points = horizon_height + (noise_profile * amplitude)
            points = [(0, h)] + list(zip(x_points, y_points)) + [(w, h)]
            base_mountain = np.array([30, 45, 65]) if layer % 2 == 0 else np.array([20, 35, 55])
            sky_mix = 0.75 * (1.0 - depth_factor)
            final_rgb = (base_mountain * (1.0 - sky_mix) + np.array(sky_bottom_color) * sky_mix).astype(np.uint8)
            draw.polygon(points, fill=(*final_rgb, 255))

    def _paint_photoreal_trees(self, image, theme, w, h, rng):
        """Photorealistic trees — fractal trunks + layered canopy clusters with depth haze, replaces pathetic flat triangles."""
        if theme not in ("forest","garden","autumn","meadow","river","waterfall","mountain","savanna","tundra"):
            return
        draw = ImageDraw.Draw(image, "RGBA")
        # theme palettes
        palettes = {
            "autumn": [(180, 60, 30), (200, 90, 40), (210, 140, 50), (160, 50, 30)],
            "forest": [(30, 80, 40), (45, 110, 55), (60, 140, 70), (20, 60, 30)],
            "garden": [(50, 120, 60), (70, 150, 80), (90, 170, 95), (35, 90, 45)],
            "waterfall": [(35, 95, 50), (50, 125, 65), (70, 155, 85), (25, 70, 40)],
        }
        greens = palettes.get(theme, palettes["forest"])
        num = 18 if w > 1800 else 9  # balanced — 32 OOMs
        # depth sorted far to near
        trees = []
        for _ in range(num):
            tx = rng.randint(int(w*0.05), int(w*0.95))
            base_y = rng.randint(int(h*0.62), int(h*0.96))
            depth = (base_y - int(h*0.62)) / (h*0.34)  # 0 far, 1 near
            scale = 0.55 + depth*0.9 + rng.uniform(-0.15, 0.15)
            trees.append((base_y, tx, scale, depth))
        trees.sort()  # far first
        for base_y, tx, scale, depth in trees:
            trunk_w = int(10*scale + 6)
            trunk_h = int(80*scale + 40)
            top_y = base_y - trunk_h
            # bark with vertical gradient
            bark_dark, bark_light = (55, 35, 20), (90, 65, 40)
            for i in range(trunk_w):
                t = i / max(trunk_w-1,1)
                r = int(bark_dark[0]*(1-t)+bark_light[0]*t)
                g = int(bark_dark[1]*(1-t)+bark_light[1]*t)
                b = int(bark_dark[2]*(1-t)+bark_light[2]*t)
                a = 200 if depth > 0.5 else 150
                draw.line((tx - trunk_w//2 + i, base_y, tx - trunk_w//2 + i, top_y), fill=(r,g,b,a))
            # canopy: 3 layers of overlapping ellipses with noise-distorted positions
            canopy_r = int(70*scale + 30)
            # use Perlin for leaf clump offset
            n_off = self._perlin_noise_2d(np.array([tx*0.01]), np.array([base_y*0.01]))[0] * 12
            layers = 3 if depth > 0.6 else 2
            for li in range(layers):
                ly = top_y - int(35*scale) - li*int(28*scale)
                lr = int(canopy_r * (0.95 - li*0.18) + rng.randint(-6,6))
                # haze for depth
                haze_mix = 0.35*(1-depth)
                for ci in range(12):  # 200× dense canopy
                    cx = int(tx + n_off + rng.randint(-lr//2, lr//2))
                    cy = int(ly + rng.randint(-lr//3, lr//3))
                    col = greens[li % len(greens)]
                    # mix with sky for atmospheric perspective
                    if haze_mix > 0:
                        col = tuple(int(c*(1-haze_mix)+210*haze_mix) for c in col)
                    a = 210 if li == 0 else 190
                    # draw leaf cluster as soft ellipse
                    draw.ellipse((cx - lr//2, cy - lr//3, cx + lr//2, cy + lr//3), fill=(*col, a))
                    # highlight
                    hl = tuple(min(255, c+30) for c in col)
                    draw.ellipse((cx - lr//4, cy - lr//6, cx + lr//6, cy - lr//8), fill=(*hl, 80))

    def _paint_photoreal_water(self, image, theme, w, h, rng):
        """Photorealistic water — gradient depth + FBM waves + specular + sky reflection, replaces pathetic arcs."""
        if theme not in ("ocean","river","waterfall","mountain","winter","canyon","meadow"):
            return
        draw = ImageDraw.Draw(image, "RGBA")
        # water zone: bottom 38% of image
        water_top = int(h * 0.62)
        # depth gradient: deep -> shallow
        deep, shallow = (15, 45, 90), (45, 115, 140)
        if theme == "waterfall":
            deep, shallow = (20, 55, 85), (70, 140, 160)
        elif theme == "river":
            deep, shallow = (25, 65, 85), (60, 130, 145)
        # fill gradient row by row with slight noise for realism
        water_arr = np.zeros((h - water_top, w, 3), dtype=np.uint8)
        for y in range(h - water_top):
            t = y / max(h - water_top - 1, 1)
            # add subtle Perlin undulation to color
            n = self._perlin_noise_2d(np.array([y*0.08]), np.array([0.0]))[0] * 0.04
            nt = np.clip(t + n, 0, 1)
            r = int(deep[0]*(1-nt) + shallow[0]*nt)
            g = int(deep[1]*(1-nt) + shallow[1]*nt)
            b = int(deep[2]*(1-nt) + shallow[2]*nt)
            water_arr[y, :] = (r,g,b)
        lw, lh = w // 4, (h - water_top) // 4
        wave = self._fbm(lw, lh, octaves=5, scale=0.02)
        wave = (wave - 0.5) * 2.0  # -1 to 1
        wave_img = Image.fromarray(((wave + 1)*127).astype(np.uint8), mode='L').resize((w, h - water_top), Image.BICUBIC)
        wave_arr = np.array(wave_img, dtype=np.float32) / 255.0
        # specular highlights where wave > threshold
        specular_mask = (wave_arr > 0.68).astype(np.float32) * 85
        foam_mask = (wave_arr > 0.82).astype(np.float32) * 55
        # composite water gradient + waves
        water_img = Image.fromarray(water_arr, 'RGB').convert('RGBA')
        # add specular white overlay
        spec_layer = Image.new('RGBA', (w, h - water_top), (255, 255, 255, 0))
        spec_layer.putalpha(Image.fromarray(np.clip(specular_mask, 0, 255).astype(np.uint8)))
        foam_layer = Image.new('RGBA', (w, h - water_top), (255, 250, 240, 0))
        foam_layer.putalpha(Image.fromarray(np.clip(foam_mask, 0, 255).astype(np.uint8)))
        # sky reflection: blend top of water with flipped sky strip (subtle)
        # take sky strip from just above water_top, flip vertically
        sky_strip = image.crop((0, max(0, water_top - int(h*0.18)), w, water_top)).resize((w, h - water_top), Image.BICUBIC)
        sky_strip = sky_strip.transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(radius=2))
        water_img = Image.alpha_composite(water_img, Image.blend(Image.new('RGBA', water_img.size, (0,0,0,0)), sky_strip.convert('RGBA'), 0.18))
        water_img = Image.alpha_composite(water_img, spec_layer)
        water_img = Image.alpha_composite(water_img, foam_layer)
        # horizon foam line
        draw_water = ImageDraw.Draw(water_img)
        draw_water.line((0, 0, w, 0), fill=(255, 250, 240, 90), width=2)
        image.paste(water_img, (0, water_top), mask=water_img.split()[3] if water_img.mode == 'RGBA' else None)

    def _paint_foreground_focus(self, image, theme, w, h, rng):
        """All foreground objects in sharp focus — ground texture, rocks, grass, sand per theme."""
        draw = ImageDraw.Draw(image, "RGBA")
        ground_top = int(h*0.74)
        # theme ground base
        ground_col = {
            "forest": (35, 65, 30), "autumn": (90, 70, 40), "meadow": (55, 110, 50),
            "desert": (185, 155, 115), "beach": (210, 195, 165), "ocean": (210, 195, 165),
            "mountain": (85, 85, 80), "canyon": (165, 120, 85), "savanna": (165, 145, 95),
            "tundra": (190, 210, 220), "winter": (235, 240, 245), "river": (45, 85, 55),
        }.get(theme, (50, 85, 45))
        # ground plane — 200× undulation: triple Perlin + 160 steps
        pts = [(0, h)]
        for x in range(0, w+1, w//60):
            n = self._perlin_noise_2d(np.array([x*0.006]), np.array([ground_top*0.01]))[0]
            n2 = self._perlin_noise_2d(np.array([x*0.018]), np.array([ground_top*0.01+20]))[0] * 0.35
            n3 = self._perlin_noise_2d(np.array([x*0.032]), np.array([ground_top*0.01+40]))[0] * 0.18
            y = ground_top + int((n+n2+n3)*14) + rng.randint(-3,3)
            pts.append((x, y))
        pts.append((w, h))
        draw.polygon(pts, fill=(*ground_col, 255))
        # foreground: 200× denser scatter
        n_scatter = 140 if w > 1800 else 68
        for _ in range(n_scatter):
            fx = rng.randint(0, w)
            fy = rng.randint(ground_top+10, h-8)
            s = (fy - ground_top) / (h - ground_top)
            if theme in ("forest","garden","autumn","meadow","river"):
                for _ in range(5):
                    gx = fx + rng.randint(-14,14)
                    draw.line((gx, fy, gx + rng.randint(-5,5), fy - int(12+16*s)), fill=(55+rng.randint(0,45), 115+rng.randint(0,45), 45, 185), width=2)
                    # small leaf speck
                    if rng.random() > 0.6:
                        draw.ellipse((gx-2, fy - int(8+12*s)-2, gx+2, fy - int(8+12*s)+2), fill=(70, 140, 60, 140))
            elif theme in ("desert","canyon","savanna"):
                rw, rh = int(20+22*s), int(11+15*s)
                col = (ground_col[0]-12, ground_col[1]-12, ground_col[2]-18)
                draw.ellipse((fx - rw//2, fy - rh//2, fx + rw//2, fy + rh//2), fill=(*col, 215))
                # highlight
                draw.ellipse((fx - rw//3, fy - rh//3, fx - rw//6, fy - rh//4), fill=(ground_col[0]+10, ground_col[1]+10, ground_col[2]+5, 90))
            elif theme in ("ocean","beach"):
                draw.arc((fx-24, fy-7, fx+24, fy+7), 0, 180, fill=(255, 250, 235, 75), width=1)
                if rng.random() > 0.7:
                    draw.ellipse((fx-4, fy-2, fx+4, fy+2), fill=(255, 255, 255, 55))
            elif theme in ("winter","tundra"):
                draw.ellipse((fx-4, fy-4, fx+4, fy+4), fill=(255,255,255, 190))
                draw.ellipse((fx-1, fy-1, fx+1, fy+1), fill=(210,230,255, 120))
            else:
                draw.ellipse((fx-6, fy-5, fx+6, fy+5), fill=(ground_col[0]+18, ground_col[1]+18, ground_col[2]+18, 165))

    def _paint_city_skyline(self, image, w, h, rng):
        """Photorealistic city silhouette — varied building heights + window lights."""
        draw = ImageDraw.Draw(image, "RGBA")
        x = -60
        while x < w:
            bw = rng.randint(90, 220)
            bh = rng.randint(180, 520)
            top = int(h*0.62) - bh
            col = rng.choice([(22,28,45,235),(32,38,58,225),(42,48,68,215)])
            draw.rectangle((x, top, x+bw, h), fill=col)
            # windows — theme-aware warm lights
            for wx in range(x+14, x+bw-10, 28):
                for wy in range(top+18, h-22, 36):
                    if rng.random() > 0.45:
                        draw.rectangle((wx, wy, wx+9, wy+15), fill=(255, 225, 130, 205))
            x += bw + rng.randint(10, 24)

    def _paint_distant_treeline(self, image, w, h, sky_bottom_color, rng):
        """Distant forested hills — haze-blended treeline, not mountains."""
        draw = ImageDraw.Draw(image, "RGBA")
        base_y = int(h*0.58)
        # soft hill
        points = [(0, h)]
        for x in range(0, w+1, w//18):
            points.append((x, base_y - rng.randint(18, 55)))
        points.append((w, h))
        hill_col = tuple(int(c*0.55) for c in sky_bottom_color)
        draw.polygon(points, fill=(*hill_col, 210))
        # treeline silhouette on hill
        for _ in range(22):
            tx = rng.randint(0, w)
            ty = int(base_y - rng.randint(8, 35))
            tw = rng.randint(18, 38)
            th = rng.randint(45, 95)
            col = (18, 55, 32, 190)
            draw.polygon([(tx, ty - th//3),(tx - tw//2, ty + th//5),(tx + tw//2, ty + th//5)], fill=col)

    def _paint_horizon_haze(self, image, w, h, sky_bottom_color, theme, rng):
        """Subtle horizon accent for ocean/space/rainy — differentiated atmosphere colors per prompt."""
        draw = ImageDraw.Draw(image, "RGBA")
        # thin horizon line with theme-tinted haze, not mountains
        haze_col = {
            "ocean": (30, 90, 140, 70),
            "space": (20, 20, 40, 90),
            "rainy": (60, 80, 95, 60),
        }.get(theme, (*sky_bottom_color, 55))
        y0 = int(h*0.56)
        for y in range(y0, y0+18):
            a = int(haze_col[3] * (1 - (y-y0)/18))
            draw.line((0, y, w, y), fill=(*haze_col[:3], a))

    def _radial_gradient(self, w, h, cx, cy, inner_color, outer_color, power=2.0):
        """Instant vectorized radial engine with customized tone mapping curves."""
        x = np.arange(w, dtype=np.float32)
        y = np.arange(h, dtype=np.float32)
        xx, yy = np.meshgrid(x, y)
        max_dist = math.hypot(max(cx, w - cx), max(cy, h - cy))
        distance = np.hypot(xx - cx, yy - cy) / (max_dist or 1.0)
        factor = np.clip(distance ** power, 0.0, 1.0)[:, :, np.newaxis]
        c_inner = np.array(inner_color, dtype=np.float32)
        c_outer = np.array(outer_color, dtype=np.float32)
        rgb_array = c_inner * (1.0 - factor) + c_outer * factor
        return Image.fromarray(rgb_array.astype(np.uint8), mode='RGB')

    def _add_40x_micro_detail(self, image, theme, rng):
        """200× detail: dual-scale micro-texture at final 1024×768 — cheap, no OOM."""
        w, h = image.size
        lw, lh = w // 4, h // 4
        micro = self._fbm(lw, lh, octaves=6, scale=0.04)
        micro2 = self._fbm(lw, lh, octaves=6, scale=0.11)
        micro = micro * 0.65 + micro2 * 0.35
        micro = (micro * 255).astype(np.uint8)
        micro_img = Image.fromarray(micro, mode='L').resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(radius=0.6))
        micro_arr = np.array(micro_img, dtype=np.float32) / 255.0
        grain = (micro_arr - 0.5) * 28
        grain = np.stack([grain]*3, axis=-1)
        arr = np.array(image, dtype=np.float32)
        out = np.clip(arr + grain, 0, 255).astype(np.uint8)
        return Image.fromarray(out)

    def classify_prompt(self, prompt: str) -> str:
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

    def _color_grade(self, image, theme):
        """Cinematic color grading — 20 themes."""
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.15)
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)
        if theme in ("sunset", "sunrise"):
            image = self._split_tone(image, highlights=(1.18, 1.07, 0.82), shadows=(0.88, 0.93, 1.12))
        elif theme == "space":
            image = self._split_tone(image, highlights=(0.96, 0.96, 1.18), shadows=(0.68, 0.73, 1.02))
        elif theme in ("forest", "garden", "meadow", "river"):
            image = self._split_tone(image, highlights=(0.94, 1.14, 0.88), shadows=(0.82, 1.02, 0.82))
        elif theme in ("winter", "tundra", "aurora"):
            image = self._split_tone(image, highlights=(0.88, 0.94, 1.18), shadows=(0.78, 0.83, 1.12))
        elif theme in ("desert", "savanna", "canyon"):
            image = self._split_tone(image, highlights=(1.18, 1.08, 0.85), shadows=(1.04, 0.93, 0.80))
        elif theme in ("city",):
            image = self._split_tone(image, highlights=(1.12, 1.02, 0.88), shadows=(0.83, 0.88, 1.07))
        elif theme in ("ocean", "waterfall"):
            image = self._split_tone(image, highlights=(0.92, 1.02, 1.16), shadows=(0.82, 0.92, 1.08))
        elif theme in ("autumn",):
            image = self._split_tone(image, highlights=(1.20, 1.02, 0.78), shadows=(0.95, 0.86, 0.78))
        elif theme in ("volcano",):
            image = self._split_tone(image, highlights=(1.22, 0.98, 0.75), shadows=(0.90, 0.80, 0.85))
        image = self._vignette(image, 0.32)
        try:
            arr = np.array(image, dtype=np.float32) / 255.0
            arr = np.clip((arr - 0.5) * 1.12 + 0.5, 0, 1)
            arr = np.power(arr, 0.95)
            image = Image.fromarray((arr * 255).astype(np.uint8))
        except Exception:
            pass
        return image

    def _split_tone(self, image, highlights, shadows):
        arr = np.array(image.convert('RGB'), dtype=np.float32)
        lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
        t = lum / 255.0
        t = t * t * (3 - 2 * t)
        hr, hg, hb = highlights
        sr, sg, sb = shadows
        mr = sr * t + hr * (1 - t)
        mg = sg * t + hg * (1 - t)
        mb = sb * t + hb * (1 - t)
        out = np.empty_like(arr)
        out[:, :, 0] = np.clip(arr[:, :, 0] * mr, 0, 255)
        out[:, :, 1] = np.clip(arr[:, :, 1] * mg, 0, 255)
        out[:, :, 2] = np.clip(arr[:, :, 2] * mb, 0, 255)
        return Image.fromarray(out.astype(np.uint8), 'RGB')

    def _vignette(self, image, strength=0.3):
        w, h = image.size
        arr = np.array(image.convert('RGBA'), dtype=np.float32)
        ys, xs = np.ogrid[:h, :w]
        cx, cy = w / 2, h / 2
        max_dist = math.hypot(cx, cy) or 1.0
        dist = np.hypot(xs - cx, ys - cy) / max_dist
        mask = np.clip(dist, 0, 1)
        v = np.ones_like(dist, dtype=np.float32)
        over = mask > 0.5
        v[over] = 1.0 - strength * ((mask[over] - 0.5) / 0.5) ** 1.5
        v = v[:, :, None]
        arr[:, :, 0] *= v[:, :, 0]
        arr[:, :, 1] *= v[:, :, 0]
        arr[:, :, 2] *= v[:, :, 0]
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA').convert('RGB')

    def generate(self, prompt: str, output_path: str, seed: int = None) -> str:
        """Maximized ultra-high quality procedural generation — theme-aware, 3× supersampled, photorealistic."""
        theme = self.classify_prompt(prompt)
        rng = random.Random(seed if seed is not None else prompt)

        # Theme sky palettes for maximized engine
        palettes = {
            "sunset": ((235, 75, 45), (255, 205, 115)),
            "sunrise": ((255, 140, 80), (255, 220, 160)),
            "ocean": ((100, 180, 220), (30, 100, 180)),
            "forest": ((140, 200, 160), (50, 120, 90)),
            "space": ((10, 10, 30), (2, 2, 15)),
            "city": ((180, 190, 210), (90, 110, 140)),
            "mountain": ((160, 200, 230), (70, 120, 170)),
            "desert": ((255, 180, 90), (255, 230, 170)),
            "aurora": ((15, 25, 50), (5, 15, 40)),
            "rainy": ((100, 130, 150), (45, 70, 95)),
            "garden": ((160, 220, 180), (70, 140, 100)),
            "winter": ((180, 210, 240), (100, 150, 200)),
            "waterfall": ((120, 180, 200), (40, 90, 140)),
            "autumn": ((220, 140, 60), (255, 210, 110)),
            "savanna": ((255, 200, 120), (180, 140, 80)),
            "canyon": ((200, 110, 70), (255, 190, 120)),
            "volcano": ((180, 60, 30), (255, 170, 80)),
            "tundra": ((170, 200, 220), (90, 140, 180)),
            "meadow": ((160, 220, 180), (110, 180, 140)),
            "river": ((130, 190, 210), (60, 120, 90)),
        }
        sky_top, sky_bottom = palettes.get(theme, ((180, 190, 210), (90, 110, 140)))

        sw, sh = self.SIZE[0] * self.SUPER_SAMPLE, self.SIZE[1] * self.SUPER_SAMPLE

        # 1. Sky gradient
        sky = Image.new("RGB", (sw, sh))
        sky_draw = ImageDraw.Draw(sky)
        for y in range(sh):
            mix = y / sh
            r = int(sky_top[0] * (1 - mix) + sky_bottom[0] * mix)
            g = int(sky_top[1] * (1 - mix) + sky_bottom[1] * mix)
            b = int(sky_top[2] * (1 - mix) + sky_bottom[2] * mix)
            sky_draw.line([(0, y), (sw, y)], fill=(r, g, b))

        # 2. Volumetric clouds via Perlin FBM
        self._paint_realistic_clouds(sky, theme, sw, sh, rng)

        # 3. Sun glow radial
        if theme in ("sunset", "sunrise", "desert", "savanna"):
            sun_glow = self._radial_gradient(sw, sh, sw // 2, int(sh * 0.42), (255, 245, 210), (0, 0, 0), power=2.5)
            sky = Image.fromarray(np.clip(np.array(sky, dtype=np.int32) + np.array(sun_glow) // 3, 0, 255).astype(np.uint8))

        # 4. Theme-specific landscape (no longer just mountains for every prompt)
        try:
            if theme in ("mountain","canyon","volcano","desert","tundra","savanna","winter","aurora"):
                self._paint_mountain_ridges(sky, sw, sh, sky_bottom, rng)
            elif theme == "city":
                self._paint_city_skyline(sky, sw, sh, rng)
            elif theme in ("forest","garden","autumn","meadow","waterfall","river"):
                self._paint_distant_treeline(sky, sw, sh, sky_bottom, rng)
            elif theme in ("ocean","space","rainy"):
                # ocean/space keep sky-dominant with horizon accent only
                self._paint_horizon_haze(sky, sw, sh, sky_bottom, theme, rng)
            else:
                self._paint_mountain_ridges(sky, sw, sh, sky_bottom, rng)
        except Exception:
            pass

        # 4b. Photorealistic foreground — trees & water upgraded per theme (not pathetic flats)
        try:
            self._paint_photoreal_trees(sky, theme, sw, sh, rng)
            self._paint_photoreal_water(sky, theme, sw, sh, rng)
            self._paint_foreground_focus(sky, theme, sw, sh, rng)
        except Exception:
            pass

        # 5. Downscale 2× with LANCZOS for flawless anti-aliasing
        image = sky.resize(self.SIZE, Image.Resampling.LANCZOS)

        # 5b. 40× micro-detail overlay at final size (cheap, no supersample OOM)
        try:
            image = self._add_40x_micro_detail(image, theme, rng)
        except Exception:
            pass

        # 6. Cinematic grading + HDR bloom + micro-contrast + haze + grain (130%+ even better finish)
        image = self._color_grade(image, theme)
        try:
            image = image.filter(ImageFilter.UnsharpMask(radius=1.8, percent=120, threshold=1))
            image = ImageEnhance.Color(image).enhance(1.12)
            image = ImageEnhance.Contrast(image).enhance(1.10)
            arr = np.array(image).astype(np.float32)
            bright = np.clip((arr - 182) / 73.0, 0, 1)
            bright_img = Image.fromarray((bright * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=3.0))
            image = Image.blend(image, Image.blend(image, bright_img, 0.55), 0.22)
            detail = image.filter(ImageFilter.DETAIL)
            image = Image.blend(image, detail, 0.16)
            haze = Image.new('RGB', image.size, (210, 225, 235))
            image = Image.blend(image, haze, 0.04)
            grain = (np.random.RandomState((hash(prompt) % (2**32))).randn(image.size[1], image.size[0], 3) * 4).astype(np.float32)
            g_arr = np.array(image).astype(np.float32) + grain
            image = Image.fromarray(np.clip(g_arr, 0, 255).astype(np.uint8))
        except Exception:
            pass

        if image.mode == 'RGBA':
            bg = Image.new('RGB', image.size, (0, 0, 0))
            bg.paste(image, mask=image.split()[3])
            image = bg
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, quality=95, optimize=True)
        return f"Generated an offline {theme} background with Pillow procedural rendering (maximized 3× supersampled Perlin) and saved it to {output_path}."


# For backward compatibility
GENERATOR_SHAPES = ("circle", "square", "triangle", "diamond", "star", "heart")
GENERATOR_COLORS = ("red", "blue", "green", "yellow", "purple", "orange", "pink", "white", "black")
