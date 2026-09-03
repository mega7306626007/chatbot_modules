"""QR code generator (Section 13C) - Reed-Solomon generator-polynomial order bug FIXED here
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 13C: QR CODE GENERATOR (from-scratch ISO/IEC 18004 encoder)
# ==============================================================================
#
# A from-scratch QR code encoder - no external qrcode library (this
# sandbox has no network access to install one, and this file avoids
# adding new hard dependencies anyway). Implements the real published
# spec: byte-mode encoding, Reed-Solomon error correction over
# GF(256), the standard finder/timing/alignment pattern layout, the
# zigzag data-placement order, XOR masking, and BCH-coded format
# information - not a simplified look-alike.
#
# SCOPE: supports versions 1-5 with error-correction level L only
# (deliberately - these are the single-codeword-block versions, which
# avoids implementing the spec's block-splitting/interleaving rules
# for larger payloads). That caps payloads at roughly 100 bytes of
# text - plenty for a URL, a short message, a Wi-Fi credential line,
# or similar, but not a large document.
#
# HONESTY NOTE ON VERIFICATION: this was checked against OpenCV's
# built-in QR decoder (cv2.QRCodeDetector) during development, which
# confirmed the finder-pattern/quiet-zone geometry is detected
# correctly. Full decode-round-trip verification across every code
# path was not exhaustively completed. If a generated code doesn't
# scan for you, that's a real possibility worth testing for, not a
# hypothetical - try a phone camera or another scanner, and treat
# unusual payloads (very short/very long text, non-ASCII) as more
# likely to expose an edge case than a plain short URL.

class QRCodeGenerator:
    """From-scratch ISO/IEC 18004 QR code encoder - see the Section 13C
    module docstring above for scope and the honesty note on
    verification status."""

    # ---- GF(256) arithmetic for Reed-Solomon error correction --------------
    _GF_EXP = [0] * 512
    _GF_LOG = [0] * 256

    @classmethod
    def _init_gf(cls):
        x = 1
        for i in range(255):
            cls._GF_EXP[i] = x
            cls._GF_LOG[x] = i
            x <<= 1
            if x & 0x100:
                x ^= 0x11D  # the QR code spec's primitive polynomial
        for i in range(255, 512):
            cls._GF_EXP[i] = cls._GF_EXP[i - 255]

    @classmethod
    def _gf_mul(cls, a, b):
        if a == 0 or b == 0:
            return 0
        return cls._GF_EXP[cls._GF_LOG[a] + cls._GF_LOG[b]]

    @classmethod
    def _rs_generator_poly(cls, num_ec):
        poly = [1]
        for i in range(num_ec):
            new_poly = [0] * (len(poly) + 1)
            for j, coef in enumerate(poly):
                new_poly[j] ^= cls._gf_mul(coef, cls._GF_EXP[i])
                new_poly[j + 1] ^= coef
            poly = new_poly
        return poly

    @classmethod
    def _rs_encode(cls, data, num_ec):
        # BUGFIX: _rs_generator_poly() builds the polynomial ascending
        # (poly[k] = coefficient of x^k), but the long-division loop
        # below walks it MSB-first (highest-degree term first), which
        # requires descending order. Without the reverse, every QR code
        # this generated had correct data codewords but wrong
        # error-correction codewords, so the finder/timing/format
        # pattern all looked right but real scanners couldn't decode
        # the payload. Reversing here fixes it - verified against
        # OpenCV's QRCodeEncoder as a reference.
        gen = list(reversed(cls._rs_generator_poly(num_ec)))
        msg = list(data) + [0] * num_ec
        for i in range(len(data)):
            coef = msg[i]
            if coef != 0:
                for j, g in enumerate(gen):
                    msg[i + j] ^= cls._gf_mul(g, coef)
        return msg[len(data):]

    # ---- version tables (EC level L, single-block versions 1-5 only) ------
    VERSION_INFO_L = {
        1: (26, 7, 19), 2: (44, 10, 34), 3: (70, 15, 55),
        4: (100, 20, 80), 5: (134, 26, 108),
    }  # version: (total_codewords, ec_codewords, data_codewords)
    MODULES_PER_SIDE = {1: 21, 2: 25, 3: 29, 4: 33, 5: 37}
    ALIGNMENT_POSITIONS = {1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30]}
    FORMAT_EC_BITS = {"L": 0b01, "M": 0b00, "Q": 0b11, "H": 0b10}

    @classmethod
    def _choose_version(cls, data_len):
        for version, (_total, _ec, data_cap) in cls.VERSION_INFO_L.items():
            header_bits = 4 + 8  # mode indicator + byte-mode character count
            available_bits = data_cap * 8 - header_bits
            if data_len <= available_bits // 8:
                return version
        return None

    @classmethod
    def _build_data_codewords(cls, data_bytes, version):
        _total, _ec, data_cap = cls.VERSION_INFO_L[version]
        bits = [0, 1, 0, 0]  # mode indicator: byte mode
        count = len(data_bytes)
        bits.extend([(count >> i) & 1 for i in range(7, -1, -1)])
        for byte in data_bytes:
            bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])

        capacity_bits = data_cap * 8
        remaining = capacity_bits - len(bits)
        bits.extend([0] * max(0, min(4, remaining)))
        while len(bits) % 8 != 0:
            bits.append(0)
        pad_bytes = [0xEC, 0x11]
        i = 0
        while len(bits) < capacity_bits:
            byte = pad_bytes[i % 2]
            bits.extend([(byte >> b) & 1 for b in range(7, -1, -1)])
            i += 1
        bits = bits[:capacity_bits]

        codewords = []
        for i in range(0, len(bits), 8):
            byte = 0
            for b in bits[i:i + 8]:
                byte = (byte << 1) | b
            codewords.append(byte)
        return codewords

    @classmethod
    def _encode_bitstream(cls, text, version=None):
        data_bytes = list(text.encode("utf-8"))
        if version is None:
            version = cls._choose_version(len(data_bytes))
        if version is None:
            return None, None

        _total, num_ec, _data_cap = cls.VERSION_INFO_L[version]
        data_codewords = cls._build_data_codewords(data_bytes, version)
        ec_codewords = cls._rs_encode(data_codewords, num_ec)
        all_codewords = data_codewords + ec_codewords

        bitstream = []
        for cw in all_codewords:
            bitstream.extend([(cw >> i) & 1 for i in range(7, -1, -1)])
        remainder_bits = {1: 0, 2: 7, 3: 7, 4: 7, 5: 7}[version]
        bitstream.extend([0] * remainder_bits)
        return bitstream, version

    @staticmethod
    def _place_finder_pattern(matrix, top, left):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr, cc = top + r, left + c
                if not (0 <= rr < matrix.shape[0] and 0 <= cc < matrix.shape[1]):
                    continue
                if r in (-1, 7) or c in (-1, 7):
                    matrix[rr, cc] = 0
                elif r in (0, 6) or c in (0, 6):
                    matrix[rr, cc] = 1
                elif 2 <= r <= 4 and 2 <= c <= 4:
                    matrix[rr, cc] = 1
                else:
                    matrix[rr, cc] = 0

    @staticmethod
    def _place_alignment_pattern(matrix, center_r, center_c):
        for r in range(-2, 3):
            for c in range(-2, 3):
                rr, cc = center_r + r, center_c + c
                if r in (-2, 2) or c in (-2, 2) or (r == 0 and c == 0):
                    matrix[rr, cc] = 1
                else:
                    matrix[rr, cc] = 0

    @staticmethod
    def _apply_mask(pattern, row, col, bit):
        conditions = {
            0: (row + col) % 2 == 0,
            1: row % 2 == 0,
            2: col % 3 == 0,
            3: (row + col) % 3 == 0,
            4: ((row // 2) + (col // 3)) % 2 == 0,
            5: (row * col) % 2 + (row * col) % 3 == 0,
            6: ((row * col) % 2 + (row * col) % 3) % 2 == 0,
            7: ((row + col) % 2 + (row * col) % 3) % 2 == 0,
        }
        return bit ^ 1 if conditions.get(pattern, False) else bit

    @classmethod
    def _build_matrix(cls, bitstream, version, mask_pattern):
        size = cls.MODULES_PER_SIDE[version]
        matrix = np.full((size, size), -1, dtype=np.int8)  # -1 = not yet placed

        cls._place_finder_pattern(matrix, 0, 0)
        cls._place_finder_pattern(matrix, 0, size - 7)
        cls._place_finder_pattern(matrix, size - 7, 0)

        for i in range(8, size - 8):
            matrix[6, i] = 1 if i % 2 == 0 else 0
            matrix[i, 6] = 1 if i % 2 == 0 else 0

        aligns = cls.ALIGNMENT_POSITIONS[version]
        for ar in aligns:
            for ac in aligns:
                if (ar <= 8 and ac <= 8) or (ar <= 8 and ac >= size - 9) or (ar >= size - 9 and ac <= 8):
                    continue  # skip positions that would overlap a finder pattern
                cls._place_alignment_pattern(matrix, ar, ac)

        dark_row = 4 * version + 9
        matrix[dark_row, 8] = 1

        for i in range(9):
            if matrix[8, i] == -1:
                matrix[8, i] = 0
            if matrix[i, 8] == -1:
                matrix[i, 8] = 0
        for i in range(8):
            if matrix[8, size - 1 - i] == -1:
                matrix[8, size - 1 - i] = 0
            if matrix[size - 1 - i, 8] == -1:
                matrix[size - 1 - i, 8] = 0

        bit_idx = 0
        col = size - 1
        upward = True
        while col > 0:
            if col == 6:
                col -= 1  # column 6 is the vertical timing pattern - never used for data
            for i in range(size):
                row = (size - 1 - i) if upward else i
                for c in (col, col - 1):
                    if matrix[row, c] == -1:
                        bit = bitstream[bit_idx] if bit_idx < len(bitstream) else 0
                        bit_idx += 1
                        matrix[row, c] = cls._apply_mask(mask_pattern, row, c, bit)
            upward = not upward
            col -= 2

        return matrix

    @classmethod
    def _format_info_bits(cls, ec_level, mask_pattern):
        data = (cls.FORMAT_EC_BITS[ec_level] << 3) | mask_pattern
        generator = 0x537
        val = data << 10
        for i in range(4, -1, -1):
            if val & (1 << (i + 10)):
                val ^= generator << i
        fmt = (data << 10) | val
        fmt ^= 0b101010000010010  # the spec's fixed XOR mask for format info
        return [(fmt >> i) & 1 for i in range(14, -1, -1)]

    @classmethod
    def _place_format_info(cls, matrix, ec_level, mask_pattern):
        bits = cls._format_info_bits(ec_level, mask_pattern)
        size = matrix.shape[0]
        positions_a = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8),
                       (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]
        for bit, (r, c) in zip(bits, positions_a):
            matrix[r, c] = bit
        positions_b = [(size - 1, 8), (size - 2, 8), (size - 3, 8), (size - 4, 8),
                       (size - 5, 8), (size - 6, 8), (size - 7, 8),
                       (8, size - 8), (8, size - 7), (8, size - 6), (8, size - 5),
                       (8, size - 4), (8, size - 3), (8, size - 2), (8, size - 1)]
        for bit, (r, c) in zip(bits, positions_b):
            matrix[r, c] = bit

    @classmethod
    def generate_matrix(cls, text: str, ec_level: str = "L", mask_pattern: int = 0):
        """Returns a 2D numpy array of 0/1 QR modules, or None if the
        text is too long for the supported versions (1-5, roughly 100
        bytes)."""
        bitstream, version = cls._encode_bitstream(text)
        if bitstream is None:
            return None
        matrix = cls._build_matrix(bitstream, version, mask_pattern)
        cls._place_format_info(matrix, ec_level, mask_pattern)
        return matrix

    @classmethod
    def generate_image(cls, text: str, scale: int = 10, quiet_zone: int = 4):
        """Renders the QR matrix to a PIL Image (black/white modules,
        scaled up, with the required quiet-zone border), or a dict
        {"error": str} if the text won't fit."""
        if not PILLOW_AVAILABLE:
            return {"error": "Pillow isn't installed, so QR image rendering isn't available."}
        matrix = cls.generate_matrix(text)
        if matrix is None:
            return {"error": "That text is too long for this QR generator (roughly a 100-byte / short-URL limit)."}

        size = matrix.shape[0]
        full_size = size + quiet_zone * 2
        img_array = np.full((full_size, full_size), 255, dtype=np.uint8)
        img_array[quiet_zone:quiet_zone + size, quiet_zone:quiet_zone + size] = np.where(matrix == 1, 0, 255)
        scaled = np.kron(img_array, np.ones((scale, scale), dtype=np.uint8))
        return Image.fromarray(scaled, mode="L")

    @classmethod
    def format_generate(cls, text: str, output_path: str) -> str:
        result = cls.generate_image(text)
        if isinstance(result, dict) and "error" in result:
            return result["error"]
        try:
            result.save(output_path)
        except Exception as e:
            return f"Generated the QR code but couldn't save it: {e}"
        return (f"Generated a QR code for '{text}' and saved it to {output_path}. "
                f"(Rule-based, no ML involved - if it doesn't scan, try a shorter payload "
                f"or a different scanner app.)")


QRCodeGenerator._init_gf()


class DictionaryAPIConnector:
    """
    Real word definitions via the Free Dictionary API
    (dictionaryapi.dev) - another no-key-required public API, following
    the exact same _RestApiClient pattern as the other connectors in
    this section. Returns definitions, part of speech, and (when
    present) a phonetic spelling, pulling from the first matching entry
    the API returns.
    """

    API_URL_TEMPLATE = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    def __init__(self, client: _RestApiClient = None):
        self.client = client or _shared_rest_client

    def define(self, word: str):
        word = word.strip().lower()
        if not word:
            return {"error": "Give me a word to define."}

        result = self.client.get_json(self.API_URL_TEMPLATE.format(word=urllib.parse.quote(word)))
        if isinstance(result, dict) and "error" in result:
            return {"error": f"Couldn't reach the dictionary service ({result['error']})."}
        if not isinstance(result, list) or not result:
            return {"error": f"I couldn't find a definition for '{word}'."}

        entry = result[0]
        phonetic = entry.get("phonetic", "")
        if not phonetic:
            # "phonetic" is sometimes empty even when a per-entry
            # phonetics list has one - check there before giving up.
            for p in entry.get("phonetics", []):
                if p.get("text"):
                    phonetic = p["text"]
                    break

        meanings = []
        for meaning in entry.get("meanings", []):
            part_of_speech = meaning.get("partOfSpeech", "")
            definitions = meaning.get("definitions", [])
            # Up to 2 definitions per part of speech now (was 1) - a
            # word like "run" has meaningfully different senses within
            # the same part of speech, and only ever showing the very
            # first one undersold that.
            defs_out = []
            synonyms = set(meaning.get("synonyms", []))
            for d in definitions[:2]:
                defs_out.append({"definition": d.get("definition", ""), "example": d.get("example")})
                synonyms.update(d.get("synonyms", []))
            if defs_out:
                meanings.append({
                    "part_of_speech": part_of_speech,
                    "definitions": defs_out,
                    "synonyms": sorted(synonyms)[:5],  # a handful is plenty for a chat reply
                })

        if not meanings:
            return {"error": f"I couldn't find a usable definition for '{word}'."}

        return {"word": word, "phonetic": phonetic, "meanings": meanings}

    def format_definition(self, word: str) -> str:
        result = self.define(word)
        if "error" in result:
            return result["error"]
        lines = [f"{result['word']}" + (f"  {result['phonetic']}" if result["phonetic"] else "")]
        for meaning in result["meanings"][:3]:
            lines.append(f"  ({meaning['part_of_speech']})")
            for d in meaning["definitions"]:
                lines.append(f"    - {d['definition']}")
                if d.get("example"):
                    lines.append(f"      e.g. \"{d['example']}\"")
            if meaning["synonyms"]:
                lines.append(f"    synonyms: {', '.join(meaning['synonyms'])}")
        return "\n".join(lines)


# ==============================================================================
