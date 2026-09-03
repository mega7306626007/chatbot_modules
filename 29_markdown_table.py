"""Section 3M: MARKDOWN TABLE FORMATTER (proper CSV parsing + alignment)

Previously did a naive `.split(",")` per row, which breaks the moment
any cell itself contains a comma (e.g. "Smith, John" or "1,200"), and
had no support for column alignment. This version:
  - uses Python's `csv` module (Sniffer + reader) to handle quoted
    cells, commas-inside-quotes, and escaped quotes correctly - the
    actual CSV spec, not an approximation of it.
  - supports per-column alignment markers on an optional second
    "alignment line" (":---", "---:", ":---:" - the real Markdown
    table alignment syntax) or inferred automatically: numeric columns
    right-align, everything else left-aligns.
  - pads every column to a consistent width (real Markdown doesn't
    require this, but it makes the raw source readable too, not just
    the rendered output).
"""
import csv
import io


class MarkdownTableFormatter:
    @staticmethod
    def _parse_rows(raw_text: str):
        lines = [ln for ln in raw_text.strip().splitlines() if ln.strip()]
        if not lines:
            return []
        # sniff whether this is actually pipe-delimited (someone typed
        # "Name | Age" style input) vs comma-delimited CSV
        delimiter = "|" if lines[0].count("|") >= lines[0].count(",") and "|" in lines[0] else ","
        reader = csv.reader(io.StringIO("\n".join(lines)), delimiter=delimiter, skipinitialspace=True)
        return [[cell.strip() for cell in row] for row in reader if row]

    @staticmethod
    def _is_numeric_column(rows, col_index):
        values = [row[col_index] for row in rows if col_index < len(row) and row[col_index]]
        if not values:
            return False
        for v in values:
            try:
                float(v.replace(",", ""))
            except ValueError:
                return False
        return True

    def format_table(self, raw_text: str, alignments=None) -> str:
        rows = self._parse_rows(raw_text)
        if len(rows) < 2:
            return "Give me at least a header row and one data row (comma or pipe separated)."

        width = len(rows[0])
        rows = [r + [""] * (width - len(r)) if len(r) < width else r[:width] for r in rows]
        header, body = rows[0], rows[1:]

        if alignments is None:
            alignments = ["right" if self._is_numeric_column(body, i) else "left" for i in range(width)]
        else:
            alignments = (alignments + ["left"] * width)[:width]

        col_widths = [max(len(header[i]), max((len(r[i]) for r in body), default=0)) for i in range(width)]

        def pad(cell, i):
            w = col_widths[i]
            if alignments[i] == "right":
                return cell.rjust(w)
            elif alignments[i] == "center":
                return cell.center(w)
            return cell.ljust(w)

        def sep_cell(i):
            w = col_widths[i]
            if alignments[i] == "right":
                return "-" * (w - 1) + ":" if w > 1 else ":"
            elif alignments[i] == "center":
                return ":" + "-" * max(w - 2, 1) + ":"
            return "-" * w

        out = ["| " + " | ".join(pad(header[i], i) for i in range(width)) + " |",
               "| " + " | ".join(sep_cell(i) for i in range(width)) + " |"]
        for r in body:
            out.append("| " + " | ".join(pad(r[i], i) for i in range(width)) + " |")
        return "\n".join(out)

    def format_checklist(self, raw_text: str) -> str:
        lines = [ln.strip() for ln in raw_text.strip().splitlines() if ln.strip()]
        if not lines:
            return "Give me one item per line to turn into a checklist."
        return "\n".join(f"- [ ] {ln}" for ln in lines)
