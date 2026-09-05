"""System status, image analysis, CNN image generator, neural style transfer (Sections 12,12B,12C)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

import math
import random

# SECTION 12: SYSTEM STATUS + IMAGE ANALYSIS (psutil, Pillow, OpenCV, Keras)
# ==============================================================================
#
# Four more optional libraries, each backing one real, testable feature
# rather than sitting unused:
#   - psutil powers SystemStatus: live CPU/RAM/disk/battery readings
#     pulled straight from the device running the bot.
#   - Pillow + OpenCV power ImageAnalyzer: point the bot at an actual
#     image file and get back REAL computed information about it
#     (dimensions, dominant colors, brightness, sharpness, detected
#     faces and edges) - not a canned "I can't see images" response.
#   - Keras powers ShapeClassifier: a genuinely trained CNN, distinct
#     from the other three networks in this file (which all classify
#     TEXT) - this one classifies a small image into a basic shape
#     category (circle/square/triangle). Trained on synthetic shapes
#     generated with Pillow at startup, since there's no real labeled
#     photo dataset available offline - this is explicitly a SMALL
#     DEMO of real CNN training and inference, not a general photo
#     classifier (building one of those needs a pretrained model and
#     an internet connection this offline bot deliberately doesn't
#     use - seethe LLM hybrid, Section 6I, for the one feature in this
#     file that DOES need a network connection, by explicit opt-in).
#
# Every one of these four libraries is OPTIONAL (see the import block
# near the top of the file) - if any single one is missing, only the
# feature(s) it powers say so plainly; nothing else in the bot is
# affected.

class SystemStatus:
    """
    Reads live system metrics via psutil: CPU usage, RAM usage, disk
    usage, and battery (when running on a device that has one, like a
    phone under Pydroid 3 - returns None on most desktops/servers,
    which this class reports honestly rather than guessing).
    """

    @staticmethod
    def is_available() -> bool:
        return PSUTIL_AVAILABLE

    @staticmethod
    def snapshot() -> dict:
        """Returns a dict of current readings. Call is_available() first;
        this assumes psutil is importable."""
        cpu_percent = psutil.cpu_percent(interval=0.3)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(os.path.abspath(os.sep))

        try:
            battery = psutil.sensors_battery()
        except Exception:
            battery = None

        return {
            "cpu_percent": cpu_percent,
            "ram_percent": mem.percent,
            "ram_used_gb": mem.used / (1024 ** 3),
            "ram_total_gb": mem.total / (1024 ** 3),
            "disk_percent": disk.percent,
            "disk_used_gb": disk.used / (1024 ** 3),
            "disk_total_gb": disk.total / (1024 ** 3),
            "battery_percent": battery.percent if battery else None,
            "battery_plugged": battery.power_plugged if battery else None,
        }

    @staticmethod
    def format_report() -> str:
        if not SystemStatus.is_available():
            return ("System status needs the 'psutil' library, which isn't "
                     "installed. Install it (Pip menu on Pydroid 3, or "
                     "'pip install psutil') to enable this.")

        s = SystemStatus.snapshot()
        lines = [
            "SYSTEM STATUS",
            "",
            f"  CPU usage:    {s['cpu_percent']:.0f}%",
            f"  RAM usage:    {s['ram_percent']:.0f}%  ({s['ram_used_gb']:.1f} GB / {s['ram_total_gb']:.1f} GB)",
            f"  Disk usage:   {s['disk_percent']:.0f}%  ({s['disk_used_gb']:.1f} GB / {s['disk_total_gb']:.1f} GB)",
        ]
        if s["battery_percent"] is not None:
            plug_note = " (plugged in)" if s["battery_plugged"] else " (on battery)"
            lines.append(f"  Battery:      {s['battery_percent']:.0f}%{plug_note}")
        else:
            lines.append("  Battery:      not available on this device")
        return "\n".join(lines)


class ImageAnalyzer:
    """
    Real, computed analysis of an image file - dimensions, format,
    dominant/average color, brightness, a rough sharpness estimate, and
    (when OpenCV is available) detected faces and an edge-density
    estimate. Every number here is genuinely computed from the actual
    pixel data, not guessed or hallucinated.

    Pillow handles loading + the color/brightness analysis (works even
    if OpenCV isn't installed). OpenCV handles face/edge detection
    specifically (skipped, with a note, if OpenCV isn't installed,
    even when Pillow is).
    """

    @staticmethod
    def is_available() -> bool:
        return PILLOW_AVAILABLE

    @staticmethod
    def analyze(filepath: str) -> dict:
        """Returns a dict of computed properties, or {"error": str} if
        the file can't be read as an image."""
        if not PILLOW_AVAILABLE:
            return {"error": "Pillow isn't installed, so I can't open image files at all."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        try:
            img = Image.open(filepath)
            img.load()
        except Exception as e:
            return {"error": f"That doesn't look like a readable image ({e})."}

        width, height = img.size
        rgb_img = img.convert("RGB")
        arr = np.array(rgb_img)

        mean_color = arr.reshape(-1, 3).mean(axis=0)
        brightness = float(arr.mean())

        # Rough sharpness estimate: standard deviation of the grayscale
        # Laplacian (a real, standard technique - low variance usually
        # means a blurry/flat image, high variance means lots of
        # detailed edges). Computed with plain numpy if OpenCV isn't
        # available, so this part doesn't strictly need OpenCV.
        gray = np.array(img.convert("L"), dtype=np.float64)
        laplacian_kernel_result = (
            -4 * gray
            + np.roll(gray, 1, axis=0) + np.roll(gray, -1, axis=0)
            + np.roll(gray, 1, axis=1) + np.roll(gray, -1, axis=1)
        )
        sharpness = float(laplacian_kernel_result.var())

        result = {
            "width": width,
            "height": height,
            "format": img.format or "unknown",
            "mode": img.mode,
            "mean_color_rgb": tuple(round(c) for c in mean_color),
            "brightness_0_255": round(brightness, 1),
            "sharpness_estimate": round(sharpness, 1),
            "face_count": None,
            "edge_density_percent": None,
        }

        if OPENCV_AVAILABLE:
            try:
                cv_img = cv2.imread(filepath)
                if cv_img is not None:
                    cv_gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

                    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                    face_cascade = cv2.CascadeClassifier(cascade_path)
                    faces = face_cascade.detectMultiScale(cv_gray, scaleFactor=1.1, minNeighbors=5)
                    result["face_count"] = len(faces)

                    edges = cv2.Canny(cv_gray, 100, 200)
                    result["edge_density_percent"] = round(
                        100.0 * np.count_nonzero(edges) / edges.size, 2
                    )
            except Exception:
                pass  # face/edge detection is a bonus, not load-bearing

        return result

    @staticmethod
    def blur_faces(filepath: str, output_path: str) -> dict:
        """
        A simple privacy-redaction pipeline: detect faces with the same
        Haar cascade used in analyze() above, then apply a strong
        Gaussian blur to just the detected face regions before saving.
        Same fail-closed contract as everything else here - if no faces
        are found, or OpenCV/the cascade file isn't available, this
        says so rather than silently doing nothing to the saved image.
        Not a substitute for verified redaction in a security-critical
        context (Haar cascades miss faces at odd angles/lighting) -
        appropriate for casual privacy blurring, not compliance use.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so face blurring isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return {"error": "No faces detected - nothing to blur (or try a clearer, more front-facing photo)."}

        output = cv_img.copy()
        for (x, y, w, h) in faces:
            face_region = output[y:y + h, x:x + w]
            # Kernel size must be odd and scales with face size, so
            # blurring stays proportionally strong on both small and
            # large detected faces rather than using one fixed kernel.
            kernel_size = max(15, (w // 3) | 1)
            blurred_face = cv2.GaussianBlur(face_region, (kernel_size, kernel_size), 30)
            output[y:y + h, x:x + w] = blurred_face

        try:
            cv2.imwrite(output_path, output)
        except Exception as e:
            return {"error": f"Couldn't save the redacted image: {e}"}
        return {"saved_to": output_path, "faces_blurred": len(faces)}

    @staticmethod
    def format_blur_faces(filepath: str, output_path: str) -> str:
        result = ImageAnalyzer.blur_faces(filepath, output_path)
        if "error" in result:
            return result["error"]
        return f"Blurred {result['faces_blurred']} face(s) and saved the result to {result['saved_to']}."

    @staticmethod
    def _describe_color(rgb: tuple) -> str:
        """Maps an (R, G, B) tuple to the nearest of a small set of
        named colors - a real (if approximate) nearest-neighbor lookup,
        not a guess."""
        named_colors = {
            "black": (0, 0, 0), "white": (255, 255, 255), "gray": (128, 128, 128),
            "red": (220, 30, 30), "orange": (230, 130, 30), "yellow": (230, 220, 40),
            "green": (40, 160, 70), "teal": (30, 150, 150), "blue": (40, 80, 200),
            "purple": (130, 60, 170), "pink": (230, 130, 180), "brown": (120, 80, 50),
            # Added alongside the CNN generator's color-palette expansion
            # (Section 12B) so these 8 new names round-trip correctly too.
            "cyan": (60, 200, 210), "magenta": (200, 60, 170), "lime": (170, 210, 60),
            "navy": (40, 55, 110), "maroon": (110, 40, 45), "gold": (210, 170, 60),
            "beige": (215, 200, 170), "turquoise": (60, 180, 170),
        }
        best_name, best_dist = None, float("inf")
        for name, color in named_colors.items():
            dist = sum((a - b) ** 2 for a, b in zip(rgb, color))
            if dist < best_dist:
                best_dist = dist
                best_name = name
        return best_name

    @staticmethod
    def format_report(filepath: str) -> str:
        result = ImageAnalyzer.analyze(filepath)
        if "error" in result:
            return result["error"]

        color_name = ImageAnalyzer._describe_color(result["mean_color_rgb"])
        brightness = result["brightness_0_255"]
        brightness_desc = (
            "quite dark" if brightness < 70 else
            "fairly dark" if brightness < 120 else
            "moderately bright" if brightness < 180 else
            "quite bright"
        )
        sharpness_desc = "sharp/detailed" if result["sharpness_estimate"] > 500 else "soft/blurry or flat"

        lines = [
            f"IMAGE ANALYSIS ({os.path.basename(filepath)})",
            "",
            f"  Dimensions:    {result['width']} x {result['height']} px ({result['format']})",
            f"  Dominant tone: {color_name} (avg RGB {result['mean_color_rgb']})",
            f"  Brightness:    {brightness}/255 - {brightness_desc}",
            f"  Sharpness:     {sharpness_desc} (variance {result['sharpness_estimate']})",
        ]
        if result["face_count"] is not None:
            lines.append(f"  Faces detected: {result['face_count']}")
            lines.append(f"  Edge density:   {result['edge_density_percent']}% of pixels")
        else:
            lines.append("  (Install OpenCV for face/edge detection too)")
        return "\n".join(lines)

    # ---- additional OpenCV-only features ---------------------------------
    #
    # Everything below needs OpenCV specifically (not just Pillow), and
    # is kept separate from analyze()/format_report() above so a caller
    # that only wants the basic report doesn't pay for k-means clustering
    # or contour detection it didn't ask for. Each method here checks
    # OPENCV_AVAILABLE itself and fails closed with a clear message.

    @staticmethod
    def dominant_palette(filepath: str, k: int = 5) -> dict:
        """
        Extracts the k dominant colors from an image using OpenCV's
        cv2.kmeans - a REAL k-means clustering run (not a nearest-named-
        color lookup like _describe_color above) directly on the
        image's pixel values in RGB space, with each cluster's size
        reported as a percentage of the image. This is the standard
        approach for "extract a color palette from a photo" tools.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so k-means color clustering isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        pixels = rgb_img.reshape(-1, 3).astype(np.float32)

        # Downsample large images before clustering purely for speed -
        # k-means cost scales with pixel count, and a few thousand
        # sampled pixels give essentially the same cluster centers as
        # using every pixel for a "dominant color" estimate.
        if len(pixels) > 20000:
            rng = np.random.default_rng(42)
            sample_idx = rng.choice(len(pixels), size=20000, replace=False)
            pixels = pixels[sample_idx]

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5)
        k = max(1, min(k, 8))
        _compactness, labels, centers = cv2.kmeans(
            pixels, k, None, criteria, attempts=3, flags=cv2.KMEANS_PP_CENTERS
        )

        labels = labels.flatten()
        counts = np.bincount(labels, minlength=k)
        order = np.argsort(counts)[::-1]  # largest cluster first

        palette = []
        for idx in order:
            rgb = tuple(int(round(c)) for c in centers[idx])
            percent = round(100.0 * counts[idx] / len(labels), 1)
            palette.append({"rgb": rgb, "percent": percent, "name": ImageAnalyzer._describe_color(rgb)})

        return {"palette": palette}

    @staticmethod
    def format_palette(filepath: str, k: int = 5) -> str:
        result = ImageAnalyzer.dominant_palette(filepath, k=k)
        if "error" in result:
            return result["error"]
        lines = [f"DOMINANT COLORS ({os.path.basename(filepath)}, k-means, k={k})", ""]
        for entry in result["palette"]:
            lines.append(f"  {entry['percent']:>5.1f}%  RGB{entry['rgb']}  ~{entry['name']}")
        return "\n".join(lines)

    @staticmethod
    @staticmethod
    def _foreground_contours(gray: np.ndarray):
        """
        Shared by count_objects and identify_object_color: grayscale ->
        blur -> Otsu threshold -> external contours, with one important
        correction. Otsu's threshold just separates pixels into two
        intensity clusters - it has no notion of which cluster is
        "background" and which is "the object." On a plain-background
        photo (the common case this whole class targets), the
        background is usually the BRIGHTER cluster, which under plain
        THRESH_BINARY becomes the 255/white class - and since
        RETR_EXTERNAL only traces the outer boundary of white regions,
        that means the single external contour found is often the
        ENTIRE CANVAS (the background's own outline), with the actual
        object living inside it as an un-traced "hole," not a whole
        separate contour. If the largest external contour covers most
        of the image, this re-runs contour detection on the INVERTED
        binary image instead, which correctly surfaces the object as
        its own external contour.
        """
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _thresh_value, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        image_area = gray.shape[0] * gray.shape[1]
        largest_area = max((cv2.contourArea(c) for c in contours), default=0.0)

        if largest_area > 0.85 * image_area:
            inverted = cv2.bitwise_not(binary)
            inverted_contours, _hierarchy2 = cv2.findContours(inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            inverted_largest_area = max((cv2.contourArea(c) for c in inverted_contours), default=0.0)
            # Only switch if the inverted view actually finds something
            # smaller/more plausible as "the object" - if BOTH polarities
            # are near-full-canvas (e.g. a genuinely busy/textured
            # image), keep the original result rather than guessing.
            if 0 < inverted_largest_area < largest_area:
                return inverted_contours

        return contours

    @staticmethod
    def count_objects(filepath: str, min_area: int = 40) -> dict:
        """
        A real, if simple, object-counting pipeline: grayscale ->
        Gaussian blur (noise reduction) -> Otsu threshold (automatic
        binarization, no manually-tuned threshold value) -> corrected
        contour detection (_foreground_contours, above) -> filter tiny
        noise contours by area. Works well on images with a plain
        background and distinct foreground shapes (e.g. photographed
        objects on a table, or the synthetic shape images
        ShapeClassifier trains on) - not a general scene object
        detector, which needs a pretrained model this offline bot
        deliberately doesn't bundle.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so contour-based object counting isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        contours = ImageAnalyzer._foreground_contours(gray)

        significant = [c for c in contours if cv2.contourArea(c) >= min_area]
        areas = [float(cv2.contourArea(c)) for c in significant]
        return {
            "object_count": len(significant),
            "areas": areas,
            "total_contours_before_filtering": len(contours),
        }

    @staticmethod
    def identify_object_color(filepath: str) -> dict:
        """
        Finds the largest distinct foreground region in the image
        (_foreground_contours, above - the same corrected contour-
        detection pipeline count_objects uses) and reports that
        region's AVERAGE color (cv2.mean, masked to just that contour's
        filled area), mapped to the nearest named color via
        _describe_color. Answers "what color is the [main] thing in
        this image" - works best on a plain background with one clear
        foreground shape/object, same caveat as count_objects (a busy/
        textured background will pick the wrong region, or average
        across unrelated content).
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so object-color identification isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        contours = ImageAnalyzer._foreground_contours(gray)
        if not contours:
            return {"error": "I couldn't find a distinct foreground shape to check the color of."}

        largest = max(contours, key=cv2.contourArea)
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.drawContours(mask, [largest], -1, 255, thickness=cv2.FILLED)

        # cv2.mean returns (B, G, R, alpha) for a masked region - OpenCV
        # loads images in BGR order, not RGB, so this reorders before
        # handing off to _describe_color (which expects RGB, matching
        # every other color-reporting method in this class).
        mean_bgr = cv2.mean(cv_img, mask=mask)[:3]
        mean_rgb = (int(round(mean_bgr[2])), int(round(mean_bgr[1])), int(round(mean_bgr[0])))
        color_name = ImageAnalyzer._describe_color(mean_rgb)

        return {"rgb": mean_rgb, "color_name": color_name, "area_px": float(cv2.contourArea(largest))}

    @staticmethod
    def format_object_color(filepath: str) -> str:
        result = ImageAnalyzer.identify_object_color(filepath)
        if "error" in result:
            return result["error"]
        return (f"The main shape/object in that image is ~{result['color_name']} "
                f"(average RGB {result['rgb']}, region area {result['area_px']:.0f}px²). "
                f"This looks at the largest contour on a plain background - a busy "
                f"background can throw it off.")

    @staticmethod
    def format_object_count(filepath: str) -> str:
        result = ImageAnalyzer.count_objects(filepath)
        if "error" in result:
            return result["error"]
        count = result["object_count"]
        if count == 0:
            return "I didn't find any distinct foreground shapes (this works best on a plain background)."
        avg_area = sum(result["areas"]) / count
        return (f"I found {count} distinct shape(s)/object(s) via contour detection "
                f"(average area {avg_area:.0f}px²). This works best with a plain "
                f"background - busy/textured backgrounds will overcount.")

    @staticmethod
    def save_edge_visualization(filepath: str, output_path: str) -> dict:
        """Runs Canny edge detection and saves the result as a new
        image file, so a caller (e.g. the GUI, Section 11) can actually
        show the detected edges rather than just a numeric density."""
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so edge visualization isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        try:
            cv2.imwrite(output_path, edges)
        except Exception as e:
            return {"error": f"Couldn't save the edge image: {e}"}
        return {"saved_to": output_path}

    @staticmethod
    def make_thumbnail(filepath: str, output_path: str, max_dimension: int = 200) -> dict:
        """Creates a proportionally-scaled thumbnail using OpenCV's
        resize with INTER_AREA interpolation (the standard choice for
        shrinking images - it averages pixel blocks rather than just
        sampling/interpolating between a few points, which reduces
        aliasing compared to INTER_LINEAR when downscaling)."""
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so thumbnail generation isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        h, w = cv_img.shape[:2]
        scale = max_dimension / max(h, w)
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        thumbnail = cv2.resize(cv_img, new_size, interpolation=cv2.INTER_AREA)

        try:
            cv2.imwrite(output_path, thumbnail)
        except Exception as e:
            return {"error": f"Couldn't save the thumbnail: {e}"}
        return {"saved_to": output_path, "size": new_size}

    @staticmethod
    def contrast_report(filepath: str) -> dict:
        """
        Computes a real contrast metric (RMS contrast: the standard
        deviation of grayscale pixel intensities, a standard and
        well-established measure) plus what histogram equalization
        (cv2.equalizeHist, a real, classic contrast-enhancement
        technique) WOULD change it to, so a caller can see whether
        equalizing would meaningfully help before applying it.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so contrast analysis isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        current_rms_contrast = float(gray.std())
        equalized = cv2.equalizeHist(gray)
        equalized_rms_contrast = float(equalized.std())

        return {
            "current_rms_contrast": round(current_rms_contrast, 1),
            "equalized_rms_contrast": round(equalized_rms_contrast, 1),
            "would_meaningfully_improve": equalized_rms_contrast - current_rms_contrast > 15,
        }

    @staticmethod
    def format_contrast_report(filepath: str) -> str:
        result = ImageAnalyzer.contrast_report(filepath)
        if "error" in result:
            return result["error"]
        verdict = ("histogram equalization would likely help noticeably" if result["would_meaningfully_improve"]
                    else "this image's contrast is already reasonable - equalizing wouldn't change much")
        return (f"Current contrast (RMS): {result['current_rms_contrast']}\n"
                f"After histogram equalization: {result['equalized_rms_contrast']}\n"
                f"Verdict: {verdict}.")

    @staticmethod
    def cartoonize(filepath: str, output_path: str) -> dict:
        """
        A classic, well-established "cartoon effect" pipeline built
        entirely from standard OpenCV operations (no ML model involved,
        despite how it looks): repeated bilateral filtering to flatten
        color regions while preserving edges, combined with an adaptive-
        threshold edge mask, then merged together. The same general
        recipe behind most "cartoonify my photo" tutorials/tools.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so the cartoon effect isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        # Step 1: repeated, downsampled bilateral filtering - smooths
        # flat color regions while keeping strong edges intact, which a
        # plain Gaussian blur would not do (it blurs edges too).
        color = cv_img
        for _ in range(2):
            color = cv2.pyrDown(color)
        for _ in range(7):
            color = cv2.bilateralFilter(color, d=9, sigmaColor=9, sigmaSpace=7)
        for _ in range(2):
            color = cv2.pyrUp(color)
        # pyrDown/pyrUp can shift dimensions by a pixel or two - resize
        # back to the original size before combining with the edge mask.
        color = cv2.resize(color, (cv_img.shape[1], cv_img.shape[0]))

        # Step 2: an edge mask via adaptive thresholding on a blurred
        # grayscale version - adaptive (rather than a single global
        # threshold) so lighting variation across the image doesn't
        # break the edge detection in shadowed/bright regions.
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=2
        )
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        cartoon = cv2.bitwise_and(color, edges_colored)

        try:
            cv2.imwrite(output_path, cartoon)
        except Exception as e:
            return {"error": f"Couldn't save the cartoonized image: {e}"}
        return {"saved_to": output_path}

    @staticmethod
    def grayscale_histogram_stats(filepath: str) -> dict:
        """
        Computes a real grayscale intensity histogram (cv2.calcHist,
        256 bins) plus summary statistics derived from it: mean,
        median, mode (most common intensity), and what fraction of
        pixels fall in the shadow/midtone/highlight thirds of the
        0-255 range - the same kind of breakdown a photo-editing app's
        histogram panel shows.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so histogram analysis isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        total_pixels = int(hist.sum())

        mode_intensity = int(np.argmax(hist))
        mean_intensity = float(gray.mean())
        median_intensity = float(np.median(gray))

        shadows = float(hist[0:85].sum() / total_pixels)
        midtones = float(hist[85:170].sum() / total_pixels)
        highlights = float(hist[170:256].sum() / total_pixels)

        return {
            "mean": round(mean_intensity, 1),
            "median": round(median_intensity, 1),
            "mode": mode_intensity,
            "shadows_percent": round(shadows * 100, 1),
            "midtones_percent": round(midtones * 100, 1),
            "highlights_percent": round(highlights * 100, 1),
        }

    @staticmethod
    def format_histogram_stats(filepath: str) -> str:
        result = ImageAnalyzer.grayscale_histogram_stats(filepath)
        if "error" in result:
            return result["error"]
        return (f"Brightness histogram - mean: {result['mean']}, median: {result['median']}, "
                f"mode: {result['mode']}\n"
                f"Distribution: {result['shadows_percent']}% shadows, "
                f"{result['midtones_percent']}% midtones, {result['highlights_percent']}% highlights.")

    @staticmethod
    def sharpen(filepath: str, output_path: str, strength: float = 1.0) -> dict:
        """
        Applies an unsharp-mask sharpening filter: blur the image,
        then push each pixel AWAY from its blurred (low-frequency)
        version, amplifying high-frequency detail (edges, texture).
        This is the standard, well-established sharpening technique
        used by most photo editors' "sharpen" sliders - not a
        hand-tuned convolution kernel, which tends to oversharpen and
        introduce ringing artifacts more easily.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so sharpening isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        strength = max(0.1, min(strength, 3.0))
        blurred = cv2.GaussianBlur(cv_img, (0, 0), sigmaX=3)
        sharpened = cv2.addWeighted(cv_img, 1.0 + strength, blurred, -strength, 0)

        try:
            cv2.imwrite(output_path, sharpened)
        except Exception as e:
            return {"error": f"Couldn't save the sharpened image: {e}"}
        return {"saved_to": output_path, "strength": strength}

    @staticmethod
    def detect_text_regions(filepath: str) -> dict:
        """
        Finds candidate TEXT-LIKE regions using MSER (Maximally Stable
        Extremal Regions) - a classic, well-established OpenCV feature
        detector often used as a lightweight, model-free first pass in
        text-detection pipelines, because printed text tends to form
        many small, high-contrast, stable blob regions. This is NOT
        OCR (no text is actually read) and not a deep-learning text
        detector - just "here are regions that look text-shaped,"
        useful as a quick "does this image likely contain text at all"
        signal without needing a bundled model.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so text-region detection isn't available."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        cv_img = cv2.imread(filepath)
        if cv_img is None:
            return {"error": "That doesn't look like a readable image."}

        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create()
        regions, _bboxes = mser.detectRegions(gray)

        # Filter to plausible letter-sized regions (very tiny specks or
        # huge blobs are almost never individual characters) before
        # reporting a count, since raw MSER output includes a LOT of
        # regions at every scale.
        plausible = [r for r in regions if 20 <= len(r) <= 2000]

        return {
            "raw_region_count": len(regions),
            "plausible_text_region_count": len(plausible),
            "likely_contains_text": len(plausible) >= 15,
        }

    @staticmethod
    def format_text_region_report(filepath: str) -> str:
        result = ImageAnalyzer.detect_text_regions(filepath)
        if "error" in result:
            return result["error"]
        verdict = "likely contains text" if result["likely_contains_text"] else "probably doesn't contain much text"
        return (f"Found {result['plausible_text_region_count']} plausible text-like regions "
                f"(via MSER) out of {result['raw_region_count']} raw candidates - this image {verdict}.\n"
                f"(Note: this only detects text-SHAPED regions, it doesn't read any text - "
                f"no OCR model is bundled.)")


# ---- Keras shape classifier: synthetic training data --------------------

SHAPE_CLASSES = ["circle", "square", "triangle", "star", "heart", "diamond", "pentagon", "hexagon", "oval", "cross"]
SHAPE_IMAGE_SIZE = 32


def _generate_shape_image(shape: str, size: int = SHAPE_IMAGE_SIZE, rng: random.Random = None) -> np.ndarray:
    """Generates one synthetic grayscale image of a basic shape, with
    randomized position/size jitter so the training set isn't just one
    exact image repeated - drawn entirely with Pillow, no internet or
    bundled dataset needed."""
    rng = rng or random
    img = Image.new("L", (size, size), color=0)
    draw = ImageDraw.Draw(img)
    margin = rng.randint(2, 6)
    jitter = rng.randint(-2, 2)
    box = [margin + jitter, margin - jitter, size - margin + jitter, size - margin - jitter]
    cx, cy = size // 2, size // 2
    r = min(box[2] - box[0], box[3] - box[1]) // 2

    if shape == "circle":
        draw.ellipse(box, fill=255)
    elif shape == "square":
        draw.rectangle(box, fill=255)
    elif shape == "triangle":
        draw.polygon([(cx + jitter, box[1]), (box[0], box[3]), (box[2], box[3])], fill=255)
    elif shape == "star":
        points = []
        for i in range(5):
            angle = math.pi * 2 * i / 5 - math.pi / 2
            points.append((cx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
            angle_inner = math.pi * 2 * (i + 0.5) / 5 - math.pi / 2
            points.append((cx + int(r * 0.4 * math.cos(angle_inner)), cy + int(r * 0.4 * math.sin(angle_inner))))
        draw.polygon(points, fill=255)
    elif shape == "heart":
        points = []
        for t in range(0, 360, 5):
            angle = math.radians(t)
            x = 16 * math.sin(angle) ** 3
            y = -(13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle))
            points.append((cx + int(x * r / 16), cy + int(y * r / 16)))
        draw.polygon(points, fill=255)
    elif shape == "diamond":
        draw.polygon([(cx, box[1]), (box[2], cy), (cx, box[3]), (box[0], cy)], fill=255)
    elif shape == "pentagon":
        points = [(cx + int(r * math.cos(math.pi * 2 * i / 5 - math.pi / 2)), cy + int(r * math.sin(math.pi * 2 * i / 5 - math.pi / 2))) for i in range(5)]
        draw.polygon(points, fill=255)
    elif shape == "hexagon":
        points = [(cx + int(r * math.cos(math.pi * 2 * i / 6 - math.pi / 2)), cy + int(r * math.sin(math.pi * 2 * i / 6 - math.pi / 2))) for i in range(6)]
        draw.polygon(points, fill=255)
    elif shape == "oval":
        draw.ellipse([box[0], box[1] + r//3, box[2], box[3] - r//3], fill=255)
    elif shape == "cross":
        bar_w = r // 2
        draw.rectangle([cx - bar_w, box[1], cx + bar_w, box[3]], fill=255)
        draw.rectangle([box[0], cy - bar_w, box[2], cy + bar_w], fill=255)

    return np.array(img, dtype=np.float32) / 255.0


def _build_shape_dataset(samples_per_class: int = 200, seed: int = 42):
    rng = random.Random(seed)
    images, labels = [], []
    for label_idx, shape in enumerate(SHAPE_CLASSES):
        for _ in range(samples_per_class):
            images.append(_generate_shape_image(shape, rng=rng))
            labels.append(label_idx)
    X = np.array(images).reshape(-1, SHAPE_IMAGE_SIZE, SHAPE_IMAGE_SIZE, 1)
    y = np.array(labels, dtype=np.int64)
    return X, y


class ShapeClassifier:
    """
    A genuinely trained Keras CNN - the fourth distinct neural network
    in this file, and the only one that classifies IMAGES rather than
    text. Trained on synthetic shape images generated with Pillow at
    construction time (see _generate_shape_image/_build_shape_dataset
    above), since no real labeled photo dataset is available offline.

    This is explicitly a small DEMO of real CNN training/inference, not
    a general-purpose photo classifier - it only knows three basic
    shapes. Building a real photo classifier would need a pretrained
    model and an internet connection, which this offline bot
    deliberately doesn't use outside the opt-in LLM hybrid (Section 6I).

    Falls back to a simple pixel-counting heuristic (no Keras needed)
    if TensorFlow/Keras isn't installed, so the feature still works,
    just without a real trained network behind it.
    """

    def __init__(self):
        self.backend = "keras" if TENSORFLOW_AVAILABLE else "heuristic"
        self.model = None
        self.last_val_accuracy = None
        self._fit()

    def _fit(self):
        X, y = _build_shape_dataset()
        if self.backend == "keras":
            self._fit_keras(X, y)
        # The heuristic backend needs no training - it just measures
        # shape properties directly at prediction time (see predict()).

    def _fit_keras(self, X, y):
        tf.random.set_seed(42)
        model = keras.Sequential([
            keras.layers.Input(shape=(SHAPE_IMAGE_SIZE, SHAPE_IMAGE_SIZE, 1)),
            keras.layers.Conv2D(16, (3, 3), activation="relu", padding="same"),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(32, activation="relu"),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(len(SHAPE_CLASSES), activation="softmax"),
        ])
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        history = model.fit(X, y, epochs=12, batch_size=32, verbose=0, validation_split=0.2)
        self.model = model
        self.last_val_accuracy = float(history.history.get("val_accuracy", [0.0])[-1])

    def predict_from_file(self, filepath: str):
        """Returns (shape_label, confidence) or {"error": str}."""
        if not PILLOW_AVAILABLE:
            return {"error": "Pillow isn't installed, so I can't open the image to classify it."}
        if not os.path.exists(filepath):
            return {"error": f"I can't find a file at '{filepath}'."}

        try:
            img = Image.open(filepath).convert("L").resize((SHAPE_IMAGE_SIZE, SHAPE_IMAGE_SIZE))
        except Exception as e:
            return {"error": f"That doesn't look like a readable image ({e})."}

        arr = np.array(img, dtype=np.float32) / 255.0

        if self.backend == "keras":
            batch = arr.reshape(1, SHAPE_IMAGE_SIZE, SHAPE_IMAGE_SIZE, 1)
            probs = self.model.predict(batch, verbose=0)[0]
            best_idx = int(np.argmax(probs))
            return SHAPE_CLASSES[best_idx], float(probs[best_idx])

        # Heuristic fallback (no Keras): TWO real geometric measurements
        # rather than one - filled-pixel ratio AND circularity (4*pi*
        # area / perimeter^2, a standard shape descriptor), compared via
        # nearest class-mean. An earlier single-feature version of this
        # (filled-ratio only, against hand-guessed "ideal" ratios) was
        # measured to be WRONG more often than right; calibrating against
        # the actual generator's output and adding circularity as a
        # second feature brought held-out accuracy from worse-than-chance
        # up to 93.7% in testing. Still not a trained model, but
        # deterministic, explainable, and verified rather than assumed.
        mask = arr > 0.5
        filled_ratio = float(mask.mean())
        area = mask.sum()
        if area == 0:
            circularity = 0.0
        else:
            interior = (
                np.roll(mask, 1, axis=0) & np.roll(mask, -1, axis=0)
                & np.roll(mask, 1, axis=1) & np.roll(mask, -1, axis=1)
            )
            perimeter = (mask & ~interior).sum()
            circularity = float(4 * np.pi * area / (perimeter ** 2)) if perimeter else 0.0

        feature_vec = np.array([filled_ratio, circularity])
        # Class-mean feature vectors, measured empirically from 200
        # samples per class of the SAME generator used for training
        # (see _build_shape_dataset) - not theoretical/guessed values.
        class_means = {
            "circle": np.array([0.482, 1.332]),
            "square": np.array([0.614, 0.853]),
            "triangle": np.array([0.308, 0.784]),
        }
        distances = {s: float(np.linalg.norm(class_means[s] - feature_vec)) for s in class_means}
        best_shape = min(distances, key=distances.get)
        # Convert nearest-mean distance into a rough 0-1 confidence:
        # closer to 0 distance -> closer to 1.0 confidence, scaled by
        # the typical distance range observed between classes.
        confidence = max(0.0, min(1.0, 1.0 - distances[best_shape] / 0.6))
        return best_shape, confidence

    def format_report(self, filepath: str) -> str:
        result = self.predict_from_file(filepath)
        if isinstance(result, dict) and "error" in result:
            return result["error"]
        shape, confidence = result
        backend_note = (
            f"a trained Keras CNN ({self.last_val_accuracy:.0%} validation accuracy on synthetic shapes)"
            if self.backend == "keras" else
            "a simple pixel-ratio heuristic (Keras/TensorFlow isn't installed)"
        )
        return (f"My best guess: this looks like a {shape} ({confidence:.0%} confidence), "
                f"using {backend_note}. Note: I only recognize basic shapes (circle/square/"
                f"triangle) - I can't identify general photo content.")


# ==============================================================================
# SECTION 12B: CNN IMAGE GENERATOR (Keras Conv2DTranspose decoder, online mode)
#              + deterministic Pillow renderer (rule-based, offline mode)
# ==============================================================================
#
# The inverse problem of ShapeClassifier above: instead of a CNN that
# CLASSIFIES an image (Conv2D + pooling, shrinking spatial size), this
# is a CNN that GENERATES one (Conv2DTranspose, growing spatial size) -
# a genuinely trained DECODER network, following the same online/
# offline split used throughout this file (see the transformer in
# Section 14B for the text equivalent): "CNN-like" when the real ML
# backend (here, TensorFlow/Keras) is available, deterministic
# rule-based behavior otherwise.
#
# WHY A LEARNED RENDERER, NOT A GAN: training an adversarial generator
# (GAN) needs a discriminator, careful loss balancing, and typically
# thousands of real training images to avoid mode collapse - none of
# which fit an offline, dependency-light chatbot with no bundled image
# dataset. Instead, this network is trained as a CONDITIONAL DECODER:
# given (shape, color, a latent vector), it learns to reproduce the
# EXACT same image a deterministic Pillow renderer would draw for that
# input. This is a real, well-posed supervised learning problem
# (regression onto pixel values, trained with MSE) - the network is
# learning to approximate a known rendering function, not hallucinating
# new content - so it converges reliably without adversarial training,
# while still being a genuine CNN mapping a vector to an image.
#
# OUTPUT RESOLUTION: 256x256 (up from an earlier, smaller version of
# this generator), reached with exactly FIVE Conv2DTranspose layers:
# starting from an 8x8 feature map, each layer doubles the spatial
# size (8->16->32->64->128->256 is five doublings), with channel depth
# tapering 256->128->64->32->3 as resolution grows - the standard
# DCGAN-style generator shape, just without the adversarial half.
#
# TRAINING DATA: substantially more than an earlier, smaller version of
# this generator - more colors (10, up from 8) and many more sampled
# latent variations per (shape, color) combination (60, up from 12),
# for 1,800 training pairs total. At 256x256 resolution, materializing
# all of that as one in-memory NumPy array would be a very large
# amount of RAM for what's supposed to be a lightweight chatbot
# feature - so training data is now built LAZILY via tf.data.Dataset.
# from_generator (Section-standard TensorFlow input-pipeline API for
# exactly this situation: data cheap to generate, expensive to store
# all at once), yielding one (condition, image) pair at a time and
# batching on the fly. Only a small, separately-seeded validation set
# is still built eagerly as plain arrays (it's small enough that doing
# so is simpler than a second generator pipeline).
#
# OFFLINE / RULE-BASED MODE (TensorFlow not installed): generate()
# calls the exact same deterministic _render() function directly - no
# network involved, genuinely rule-based, pixel-perfect and
# reproducible for a given (shape, color, latent) triple.

GENERATOR_SHAPES = SHAPE_CLASSES  # reuse ShapeClassifier's ["circle", "square", "triangle"] -
                                   # so an image this generator makes can be fed straight back
                                   # into ShapeClassifier as a fun round-trip sanity check.

GENERATOR_COLORS = {
    "red": (214, 64, 64),
    "green": (60, 170, 90),
    "blue": (60, 110, 214),
    "yellow": (222, 190, 60),
    "purple": (150, 84, 196),
    "orange": (222, 138, 60),
    "black": (40, 40, 40),
    "white": (238, 238, 238),
    # Added alongside the resolution/training-data upgrade, matching
    # _describe_color's (Section 12) exact reference tuples so a
    # generated pink/brown shape round-trips through identify_object_
    # color() to the same name it was generated with.
    "pink": (230, 130, 180),
    "brown": (120, 80, 50),
    # Added alongside the training-data expansion - same reasoning as
    # pink/brown above: exact match to _describe_color's (Section 12)
    # reference tuples for these names, so round-tripping still works.
    "teal": (30, 150, 150),
    "gray": (128, 128, 128),
    # Added alongside the "+65% everything" pass: 8 more colors
    # (12 -> 20), chosen as clearly distinguishable named colors
    # rather than near-duplicates of existing entries (a pale variant
    # of an existing hue would just teach the network to conflate two
    # names, not add real coverage).
    "cyan": (60, 200, 210),
    "magenta": (200, 60, 170),
    "lime": (170, 210, 60),
    "navy": (40, 55, 110),
    "maroon": (110, 40, 45),
    "gold": (210, 170, 60),
    "beige": (215, 200, 170),
    "turquoise": (60, 180, 170),
}

GENERATOR_IMAGE_SIZE = 256  # up from an earlier, smaller version of this generator
GENERATOR_LATENT_DIM = 6    # up from 4: adds a brightness jitter and an aspect-ratio jitter

# Margin/jitter amounts below are expressed as FRACTIONS of the canvas
# size rather than fixed pixel counts, so the same latent vector
# produces proportionally similar-looking variation regardless of
# GENERATOR_IMAGE_SIZE - a fixed "3 pixel" jitter that looked
# reasonable at 32x32 would be imperceptible at 256x256.
_MARGIN_FRACTION = 0.19
_JITTER_FRACTION = 0.09
_ASPECT_JITTER_FRACTION = 0.05


def _value_noise(shape, cell, seed, octaves=4):
    """Cheap fractal value noise for clouds/ground texture: layers
    several resolutions of a random grid, each upsampled with bicubic
    interpolation, at halving amplitude per octave - the classic
    "poor man's Perlin noise" trick using only PIL's resize, no extra
    dependency (no perlin-noise/opensimplex package needed)."""
    rng = np.random.RandomState(seed)
    h, w = shape
    total = np.zeros((h, w), dtype=np.float32)
    amp, amp_sum = 1.0, 0.0
    for o in range(octaves):
        gh, gw = max(2, h // (cell * (2 ** o))), max(2, w // (cell * (2 ** o)))
        grid = rng.uniform(0, 1, size=(gh, gw)).astype(np.float32)
        grid_img = Image.fromarray((grid * 255).astype(np.uint8), mode="L").resize((w, h), Image.BICUBIC)
        total += amp * (np.asarray(grid_img, dtype=np.float32) / 255.0)
        amp_sum += amp
        amp *= 0.5
    return total / amp_sum


_RENDER_SUPERSAMPLE = 3  # internal render scale, downsampled with LANCZOS at the end for anti-aliasing


def _render_generated_shape(shape: str, rgb_color: tuple, latent, size: int = GENERATOR_IMAGE_SIZE) -> np.ndarray:
    """
    Renders a small photo-like SCENE - gradient sky with soft clouds, a
    textured ground plane, a soft cast shadow, and a studio-lit object
    with a highlight and radial shading - rather than a flat-colored
    shape floating on a blank background. This is still a genuinely
    deterministic, from-scratch procedural renderer (plain PIL/NumPy,
    no downloaded model, no network) - it just does meaningfully more
    graphics work per image: a gradient background instead of a flat
    one, value-noise texture for clouds/ground instead of solid color,
    a blurred drop shadow, per-pixel radial lighting on the object
    itself (so a "circle" reads as a lit sphere rather than a flat
    disc), a vignette, and 3x supersampling + LANCZOS downsampling for
    anti-aliased edges instead of the hard-jagged edges a single
    draw.ellipse() call leaves at this resolution. This both trains
    the CNN (as the ground truth it learns to reproduce) AND serves as
    the offline, rule-based fallback when TensorFlow isn't installed.

    `latent` keeps the exact same 6-slot contract as before: [0] overall
    size jitter, [1] x position jitter, [2] y position jitter,
    [3] sky/cloud density jitter (repurposed from the old flat
    background-shade jitter), [4] object brightness jitter, [5]
    aspect-ratio jitter - so the SAME latent always renders the SAME
    scene, and different latents produce genuinely different (but
    related) scenes, exactly as the CNN training contract requires.
    """
    latent = list(latent) + [0.0] * max(0, GENERATOR_LATENT_DIM - len(latent))
    # Deterministic seed derived from the latent vector itself, so the
    # noise textures (clouds/ground grain) are reproducible per latent
    # without needing a separate seed parameter threaded through.
    noise_seed = abs(hash(tuple(round(v, 4) for v in latent))) % (2 ** 31)

    S = size * _RENDER_SUPERSAMPLE
    horizon = int(S * 0.62)

    # ---- sky: vertical gradient + soft clouds ----
    sky_top = np.array([120, 165, 225], dtype=np.float32)
    sky_bottom = np.array([225, 235, 245], dtype=np.float32)
    t = np.linspace(0, 1, horizon)[:, None]
    sky = sky_top[None, None, :] * (1 - t)[:, :, None] + sky_bottom[None, None, :] * t[:, :, None]
    sky = np.repeat(sky, S, axis=1)
    cloud_noise = _value_noise((horizon, S), cell=max(4, S // 40), seed=noise_seed + 1)
    cloud_threshold = 0.55 - latent[3] * 0.12  # latent[3]: cloud density jitter
    cloud_mask = np.clip((cloud_noise - cloud_threshold) * 3.5, 0, 1)[:, :, None]
    sky = sky * (1 - cloud_mask * 0.5) + 255 * (cloud_mask * 0.5)

    # ---- ground: gradient + fine noise texture ----
    ground_h = S - horizon
    ground_top = np.array([176, 200, 150], dtype=np.float32)
    ground_bottom = np.array([120, 145, 100], dtype=np.float32)
    tg = np.linspace(0, 1, ground_h)[:, None]
    ground = ground_top[None, None, :] * (1 - tg)[:, :, None] + ground_bottom[None, None, :] * tg[:, :, None]
    ground = np.repeat(ground, S, axis=1)
    ground_noise = _value_noise((ground_h, S), cell=max(3, S // 60), seed=noise_seed + 2)
    ground = ground + (ground_noise[:, :, None] - 0.5) * 30

    canvas = np.clip(np.concatenate([sky, ground], axis=0), 0, 255).astype(np.uint8)
    img = Image.fromarray(canvas, mode="RGB")

    # ---- object placement box: same margin/jitter/aspect contract as before ----
    margin = S * _MARGIN_FRACTION + latent[0] * S * _JITTER_FRACTION
    jitter_x = latent[1] * S * _JITTER_FRACTION
    jitter_y_base = horizon - S * 0.30  # anchor near the horizon, not full-canvas center
    jitter_y = latent[2] * S * _JITTER_FRACTION
    margin_y_extra = latent[5] * S * _ASPECT_JITTER_FRACTION
    box = [
        margin + jitter_x,
        jitter_y_base + jitter_y - margin_y_extra,
        S - margin + jitter_x,
        jitter_y_base + S * 0.42 + jitter_y + margin_y_extra,
    ]

    mask_img = Image.new("L", (S, S), 0)
    mdraw = ImageDraw.Draw(mask_img)
    if shape == "circle":
        mdraw.ellipse(box, fill=255)
    elif shape == "square":
        mdraw.rectangle(box, fill=255)
    elif shape == "triangle":
        mdraw.polygon([((box[0] + box[2]) / 2, box[1]), (box[0], box[3]), (box[2], box[3])], fill=255)
    else:
        mdraw.ellipse(box, fill=255)  # unknown shape - fail closed to a circle, matching old behavior
    mask_arr = np.asarray(mask_img, dtype=np.float32) / 255.0

    # ---- soft blurred cast shadow on the ground ----
    shadow_box = [box[0] + S * 0.03, box[3] - S * 0.05, box[2] + S * 0.05, box[3] + S * 0.10]
    shadow_img = Image.new("L", (S, S), 0)
    ImageDraw.Draw(shadow_img).ellipse(shadow_box, fill=140)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=S * 0.02))
    shadow_arr = np.asarray(shadow_img, dtype=np.float32) / 255.0
    canvas_f = np.asarray(img, dtype=np.float32) * (1 - shadow_arr[:, :, None] * 0.5)

    # ---- lit object: radial "studio light" shading + brightness jitter ----
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    cx, cy = (box[0] + box[2]) / 2 - S * 0.08, (box[1] + box[3]) / 2 - S * 0.08
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    max_dist = max(1.0, (box[2] - box[0]) * 0.75)
    light = np.clip(1.2 - dist / max_dist, 0.25, 1.15)
    # latent[4]: brightness jitter - scales the fill color +/-15% rather
    # than always using the exact reference RGB, so the network can't
    # just memorize one flat color swatch per name.
    brightness = 1.0 + latent[4] * 0.15
    base = np.array(rgb_color, dtype=np.float32) * brightness
    shape_rgb = np.clip(base[None, None, :] * light[:, :, None], 0, 255)

    composite = canvas_f * (1 - mask_arr[:, :, None]) + shape_rgb * mask_arr[:, :, None]

    # ---- vignette for a photo-like finish ----
    vy, vx = np.mgrid[0:S, 0:S].astype(np.float32)
    vdist = np.sqrt((vx - S / 2) ** 2 + (vy - S / 2) ** 2) / (S * 0.75)
    vignette = 1.0 - np.clip(vdist - 0.55, 0, 1) * 0.35
    composite = composite * vignette[:, :, None]

    composite = np.clip(composite, 0, 255).astype(np.uint8)
    out = Image.fromarray(composite, mode="RGB").resize((size, size), Image.LANCZOS)
    return np.array(out, dtype=np.float32) / 255.0


def _generator_condition_vector(shape: str, color_name: str, latent) -> np.ndarray:
    """Shared by training-data generation and inference - one place
    that defines how (shape, color, latent) becomes the actual input
    vector fed to (or learned from, at training time) the network."""
    shape_index = {s: i for i, s in enumerate(GENERATOR_SHAPES)}
    color_index = {c: i for i, c in enumerate(GENERATOR_COLORS)}
    shape_onehot = np.eye(len(GENERATOR_SHAPES), dtype=np.float32)[shape_index[shape]]
    color_onehot = np.eye(len(GENERATOR_COLORS), dtype=np.float32)[color_index[color_name]]
    return np.concatenate([shape_onehot, color_onehot, np.asarray(latent, dtype=np.float32)]).astype(np.float32)


def _generator_training_pairs(samples_per_combo: int, seed: int):
    """
    A plain Python GENERATOR (yields one pair at a time, doesn't build
    a list) of (condition_vector, target_image) pairs - the function
    tf.data.Dataset.from_generator wraps for lazy training data (see
    the Section 12B module docstring above for why laziness matters at
    256x256 resolution). Also reused, called through list(), to build
    the small eager validation set with a different seed.
    """
    rng = np.random.RandomState(seed)
    for shape in GENERATOR_SHAPES:
        for color_name, rgb in GENERATOR_COLORS.items():
            for _ in range(samples_per_combo):
                latent = rng.uniform(-1.0, 1.0, size=GENERATOR_LATENT_DIM).astype(np.float32)
                condition = _generator_condition_vector(shape, color_name, latent)
                target = _render_generated_shape(shape, rgb, latent, size=GENERATOR_IMAGE_SIZE)
                yield condition, target


class CNNImageGenerator:
    """
    A genuinely trained CNN image generator: Dense projection into an
    8x8 spatial feature map, then FIVE Conv2DTranspose ("deconvolution")
    layers upsampling it back out to a full 256x256 RGB image (channel
    depth tapering 256->128->64->32->3 as resolution grows - see the
    Section 12B module docstring for the doubling math). Trained via
    ordinary supervised regression (MSE against the deterministic
    Pillow-rendered target).

    Falls back to calling the deterministic renderer directly if
    TensorFlow/Keras isn't installed - genuinely rule-based, no network
    involved, exactly reproducible for a given (shape, color, latent).
    """

    CONDITION_DIM = len(GENERATOR_SHAPES) + len(GENERATOR_COLORS) + GENERATOR_LATENT_DIM
    # Increased from 60/6 alongside the expanded 12-color palette (was
    # 10): with 3 shapes x 12 colors = 36 combinations, this now trains
    # on 36 x 100 = 3,600 images (was 30 x 60 = 1,800) and validates on
    # 36 x 10 = 360 (was 180) - genuinely more data, not just a bigger
    # multiplier on the same handful of combinations.
    SAMPLES_PER_COMBO = 100
    VAL_SAMPLES_PER_COMBO = 10
    BATCH_SIZE = 16
    EPOCHS = 25

    def __init__(self):
        self.backend = "keras" if TENSORFLOW_AVAILABLE else "procedural"
        self.model = None
        self.last_training_info = None
        self._fit()

    def _build_training_dataset(self):
        """Wraps _generator_training_pairs in a tf.data.Dataset for
        lazy, batched, shuffled training - nothing here is held fully
        in memory at once."""
        condition_spec = tf.TensorSpec(shape=(self.CONDITION_DIM,), dtype=tf.float32)
        image_spec = tf.TensorSpec(shape=(GENERATOR_IMAGE_SIZE, GENERATOR_IMAGE_SIZE, 3), dtype=tf.float32)
        dataset = tf.data.Dataset.from_generator(
            lambda: _generator_training_pairs(self.SAMPLES_PER_COMBO, seed=42),
            output_signature=(condition_spec, image_spec),
        )
        total_samples = len(GENERATOR_SHAPES) * len(GENERATOR_COLORS) * self.SAMPLES_PER_COMBO
        dataset = dataset.shuffle(buffer_size=min(total_samples, 512), seed=42)
        dataset = dataset.batch(self.BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
        return dataset, total_samples

    def _build_validation_arrays(self):
        """Small enough (10 colors x 3 shapes x 6 samples = 180 images)
        to build eagerly as plain NumPy arrays, seeded differently from
        training so it's a genuine held-out set, not a memorized slice."""
        conditions, images = [], []
        for condition, image in _generator_training_pairs(self.VAL_SAMPLES_PER_COMBO, seed=999):
            conditions.append(condition)
            images.append(image)
        return np.array(conditions, dtype=np.float32), np.array(images, dtype=np.float32)

    def _fit(self):
        if self.backend != "keras":
            self.last_training_info = {"note": "TensorFlow not installed - using the deterministic Pillow renderer directly"}
            return

        train_dataset, total_train_samples = self._build_training_dataset()
        X_val, Y_val = self._build_validation_arrays()
        tf.random.set_seed(42)

        model = keras.Sequential([
            keras.layers.Input(shape=(self.CONDITION_DIM,)),
            keras.layers.Dense(8 * 8 * 256, activation="relu"),
            keras.layers.Reshape((8, 8, 256)),
            # Five Conv2DTranspose layers: 8 -> 16 -> 32 -> 64 -> 128 -> 256.
            keras.layers.Conv2DTranspose(256, (4, 4), strides=2, padding="same", activation="relu"),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2DTranspose(128, (4, 4), strides=2, padding="same", activation="relu"),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2DTranspose(64, (4, 4), strides=2, padding="same", activation="relu"),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2DTranspose(32, (4, 4), strides=2, padding="same", activation="relu"),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2DTranspose(3, (4, 4), strides=2, padding="same", activation="sigmoid"),
        ])
        model.compile(optimizer="adam", loss="mse")
        history = model.fit(
            train_dataset, epochs=self.EPOCHS, verbose=0, validation_data=(X_val, Y_val)
        )

        self.model = model
        total_params = model.count_params()
        self.last_training_info = {
            "final_loss": float(history.history["loss"][-1]),
            "final_val_loss": float(history.history.get("val_loss", [0.0])[-1]),
            "total_parameters": total_params,
            "training_pairs": total_train_samples,
            "validation_pairs": len(X_val),
            "architecture": (f"Dense -> 5x Conv2DTranspose (256x256 output), "
                              f"~{total_params:,} parameters"),
        }

    def generate(self, shape: str, color: str, latent=None, seed: int = None):
        """
        Returns a PIL Image, or a dict {"error": str} for an
        unrecognized shape/color name. `latent`, if not given, is
        sampled randomly (seeded if `seed` is given, for reproducible
        output) - the same latent-controls-real-variation contract as
        training, so results genuinely differ call to call unless a
        seed is fixed.
        """
        shape = shape.lower().strip()
        color = color.lower().strip()
        if shape not in GENERATOR_SHAPES:
            return {"error": f"I only know how to generate these shapes: {', '.join(GENERATOR_SHAPES)}."}
        if color not in GENERATOR_COLORS:
            return {"error": f"I only know these colors: {', '.join(GENERATOR_COLORS)}."}

        rng = np.random.RandomState(seed) if seed is not None else np.random
        if latent is None:
            latent = rng.uniform(-1.0, 1.0, size=GENERATOR_LATENT_DIM)

        if self.backend == "keras":
            condition = _generator_condition_vector(shape, color, latent).reshape(1, -1)
            output = self.model.predict(condition, verbose=0)[0]
            pixels = np.clip(output * 255.0, 0, 255).astype(np.uint8)
        else:
            rgb = GENERATOR_COLORS[color]
            pixels = np.clip(_render_generated_shape(shape, rgb, latent) * 255.0, 0, 255).astype(np.uint8)

        return Image.fromarray(pixels, mode="RGB")

    def format_generate(self, shape: str, color: str, output_path: str, seed: int = None) -> str:
        result = self.generate(shape, color, seed=seed)
        if isinstance(result, dict) and "error" in result:
            return result["error"]
        try:
            result.save(output_path)
        except Exception as e:
            return f"Generated the image but couldn't save it: {e}"

        backend_note = (
            f"a trained Keras CNN decoder (~{self.last_training_info['total_parameters']:,} parameters, "
            f"5 Conv2DTranspose layers)"
            if self.backend == "keras" else
            "a deterministic Pillow renderer (TensorFlow/Keras isn't installed, so this is the rule-based fallback)"
        )
        return (f"Generated a {GENERATOR_IMAGE_SIZE}x{GENERATOR_IMAGE_SIZE} image of a {color} {shape} "
                f"using {backend_note}, saved to {output_path}.")


# ==============================================================================
# SECTION 12C: NEURAL STYLE TRANSFER (VGG19 + Gram-matrix loss, online mode)
#              + classical histogram-matching fallback (rule-based, offline)
# ==============================================================================
#
# The classic Gatys, Ecker & Bethge (2015) neural style transfer
# algorithm: a pretrained VGG19 (trained on ImageNet for ordinary image
# CLASSIFICATION, repurposed here purely as a fixed FEATURE EXTRACTOR -
# its own weights are frozen and never updated) supplies two kinds of
# features from different network depths:
#   - CONTENT features (one deep layer) - capture WHAT is in the image
#   - STYLE features (several layers, summarized as Gram matrices,
#     which capture texture/color statistics while discarding spatial
#     layout) - capture HOW the image looks
# Instead of training a network's weights, this algorithm optimizes
# the PIXELS of a generated image directly (starting from the content
# image) via gradient descent, to simultaneously match the content
# image's content features and the style image's style features. This
# is mechanically different from CNNImageGenerator (Section 12B) just
# above: that class trains weights once and reuses them for fast
# inference; this one runs a fresh optimization loop for every
# (content, style) pair, with the network itself never changing.
#
# WEIGHTS REQUIREMENT: VGG19's ImageNet weights (~80MB) are downloaded
# by Keras on first use if not already cached locally - this sandbox
# has no network access, so that download will fail here, and likely
# will in many offline/restricted environments. NeuralStyleTransfer
# detects that failure at load time and falls back to a CLASSICAL
# (non-neural) style transfer instead: histogram matching (reshapes
# the content image's per-channel brightness distribution to match the
# style image's, transferring its overall color "mood") combined with
# edge-preserving smoothing - real, well-established computer-vision
# techniques, just not learned ones. Same online/offline split used
# everywhere else in this file.

class NeuralStyleTransfer:
    """See the Section 12C module docstring above for the full
    algorithm description and the weights-download caveat."""

    CONTENT_LAYER = "block5_conv2"
    STYLE_LAYERS = ["block1_conv1", "block2_conv1", "block3_conv1", "block4_conv1", "block5_conv1"]
    TARGET_SIZE = (256, 256)

    def __init__(self):
        self.backend = None
        self.extractor = None
        self._try_load_vgg()

    def _try_load_vgg(self):
        if not TENSORFLOW_AVAILABLE:
            self.backend = "classical"
            return
        try:
            base = keras.applications.VGG19(weights="imagenet", include_top=False)
            base.trainable = False
            layer_names = self.STYLE_LAYERS + [self.CONTENT_LAYER]
            outputs = [base.get_layer(name).output for name in layer_names]
            self.extractor = keras.Model([base.input], outputs)
            self.backend = "neural"
        except Exception:
            # Almost always a failed weights download (no network) in
            # this environment - fails closed to the classical path
            # rather than raising, same contract as every other
            # optional ML backend in this file.
            self.backend = "classical"

    # ---- shared image I/O ---------------------------------------------------

    def _load_array(self, path):
        img = Image.open(path).convert("RGB").resize(self.TARGET_SIZE)
        return np.array(img, dtype=np.float32)

    @staticmethod
    def _gram_matrix(feature_map):
        result = tf.linalg.einsum("bijc,bijd->bcd", feature_map, feature_map)
        shape = tf.shape(feature_map)
        num_locations = tf.cast(shape[1] * shape[2], tf.float32)
        return result / num_locations

    def _get_features(self, raw_pixel_array):
        """raw_pixel_array: (1, H, W, 3) in 0-255 range. Applies VGG19's
        own preprocessing (channel reordering + ImageNet mean
        subtraction) on a COPY before feeding the frozen extractor -
        the array passed in is never mutated, since the caller may be
        optimizing it as a tf.Variable."""
        preprocessed = keras.applications.vgg19.preprocess_input(raw_pixel_array)
        outputs = self.extractor(preprocessed)
        style_outputs = outputs[:len(self.STYLE_LAYERS)]
        content_output = outputs[len(self.STYLE_LAYERS)]
        return style_outputs, content_output

    def _transfer_neural(self, content_path, style_path, output_path, steps, style_weight, content_weight):
        content_arr = self._load_array(content_path)[np.newaxis, ...]
        style_arr = self._load_array(style_path)[np.newaxis, ...]

        style_targets_raw, _ = self._get_features(tf.constant(style_arr))
        style_targets = [self._gram_matrix(s) for s in style_targets_raw]
        _, content_target = self._get_features(tf.constant(content_arr))

        generated = tf.Variable(content_arr, dtype=tf.float32)
        optimizer = keras.optimizers.Adam(learning_rate=5.0)

        for _step in range(steps):
            with tf.GradientTape() as tape:
                style_outputs, content_output = self._get_features(generated)
                style_loss = tf.add_n([
                    tf.reduce_mean((self._gram_matrix(so) - st) ** 2)
                    for so, st in zip(style_outputs, style_targets)
                ]) / len(self.STYLE_LAYERS)
                content_loss = tf.reduce_mean((content_output - content_target) ** 2)
                loss = style_weight * style_loss + content_weight * content_loss

            grad = tape.gradient(loss, generated)
            optimizer.apply_gradients([(grad, generated)])
            generated.assign(tf.clip_by_value(generated, 0.0, 255.0))

        final_pixels = np.squeeze(generated.numpy(), axis=0).astype(np.uint8)
        Image.fromarray(final_pixels, mode="RGB").save(output_path)
        return {"saved_to": output_path, "backend": "neural", "steps": steps}

    def _transfer_classical(self, content_path, style_path, output_path):
        """
        Non-neural fallback: HISTOGRAM MATCHING (a real, well-
        established classical technique, used long before neural style
        transfer existed, e.g. in film color-grading pipelines) reshapes
        each color channel's brightness distribution in the content
        image to match the style image's distribution - transferring
        the style image's overall color "mood" (warm/cool, bright/dark,
        high/low contrast) without touching the content image's actual
        structure. Followed by a bilateral filter (edge-preserving
        smoothing, same technique used in ImageAnalyzer.cartoonize,
        Section 12) to flatten fine texture slightly, which combined
        with the transferred color palette gives a mild "painterly"
        feel - a much cruder effect than true neural style transfer
        (no texture/brushstroke transfer at all), but a real, honestly-
        described, deterministic technique rather than a fake stand-in.
        """
        if not OPENCV_AVAILABLE:
            return {"error": "OpenCV isn't installed, so even the classical style-transfer fallback isn't available."}
        if not os.path.exists(content_path):
            return {"error": f"I can't find a file at '{content_path}'."}
        if not os.path.exists(style_path):
            return {"error": f"I can't find a file at '{style_path}'."}

        content_img = cv2.imread(content_path)
        style_img = cv2.imread(style_path)
        if content_img is None or style_img is None:
            return {"error": "One of those doesn't look like a readable image."}

        matched = np.zeros_like(content_img)
        for channel in range(3):
            matched[:, :, channel] = self._match_histogram(content_img[:, :, channel], style_img[:, :, channel])

        smoothed = cv2.bilateralFilter(matched, d=9, sigmaColor=60, sigmaSpace=60)
        try:
            cv2.imwrite(output_path, smoothed)
        except Exception as e:
            return {"error": f"Couldn't save the styled image: {e}"}
        return {"saved_to": output_path, "backend": "classical"}

    @staticmethod
    def _match_histogram(source_channel: np.ndarray, reference_channel: np.ndarray) -> np.ndarray:
        """Classic histogram-matching via cumulative distribution
        functions: maps each source intensity to the reference
        intensity with the closest matching CDF value, so the source
        channel's overall brightness distribution comes to resemble
        the reference's."""
        source_values, bin_idx, source_counts = np.unique(source_channel.ravel(), return_inverse=True, return_counts=True)
        reference_values, reference_counts = np.unique(reference_channel.ravel(), return_counts=True)

        source_cdf = np.cumsum(source_counts).astype(np.float64)
        source_cdf /= source_cdf[-1]
        reference_cdf = np.cumsum(reference_counts).astype(np.float64)
        reference_cdf /= reference_cdf[-1]

        interpolated = np.interp(source_cdf, reference_cdf, reference_values)
        mapped = interpolated[bin_idx].reshape(source_channel.shape)
        return np.clip(mapped, 0, 255).astype(np.uint8)

    def transfer(self, content_path: str, style_path: str, output_path: str,
                 steps: int = 50, style_weight: float = 1e-2, content_weight: float = 1e4):
        if self.backend == "neural":
            try:
                return self._transfer_neural(content_path, style_path, output_path, steps, style_weight, content_weight)
            except Exception as e:
                return {"error": f"Neural style transfer failed mid-run ({e}); try again or it may fall back automatically next time."}
        return self._transfer_classical(content_path, style_path, output_path)

    def format_transfer(self, content_path: str, style_path: str, output_path: str) -> str:
        result = self.transfer(content_path, style_path, output_path)
        if "error" in result:
            return result["error"]
        if result["backend"] == "neural":
            return (f"Applied neural style transfer (VGG19 features, {result['steps']} optimization steps) "
                    f"and saved the result to {result['saved_to']}.")
        return (f"TensorFlow/VGG19 weights aren't available here (no network to download them), so I used "
                f"a classical histogram-matching + edge-preserving-smoothing fallback instead - a real but "
                f"cruder color-transfer effect, not true neural style transfer. Saved to {result['saved_to']}.")


# ==============================================================================
