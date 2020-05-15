#!/usr/bin/python3.8

assert __name__ == '__main__'

if True:
    import sys
    sys.path.append("/usr/share/anki")
    import anki_load
    import re
    import unicodedata
    from typing import Dict, Iterable, List


def _get_words(line: str) -> Iterable[str]:
    """Gets desired words such as Japanese ones, excluding undesired ones such as English ones."""
    last_idx = -1
    idx = 0
    for idx in range(len(line)):
        char = line[idx]
        if unicodedata.category(char) != "Lo":
            # The enclosing conditional ends the word upon seeing non-Lo characters such as:
            # - Spaces and commas
            # - Latin letters
            # "Lo" (Letter other) isn't really CJK, but it's good enough
            if last_idx + 1 < idx:
                yield line[last_idx + 1:idx]
            last_idx = idx
    if last_idx < idx:
        yield line[last_idx + 1:]


_BAR_LABELS = {
    0: "N?:",
    1: "N1:",
    2: "N2:",
    3: "N3:",
    4: "N4:",
    5: "N5:",
}


def _print_histogram(histogram: List[int]) -> None:
    for level, frequency in enumerate(histogram):
        # Print frequency of unknown classification as number to set it apart from the bars
        print("`",
              _BAR_LABELS[level], " ", "#" * frequency if level else frequency,
              "`",
              sep="",
              )
        print()


_KANA_PATTERN = re.compile("[\u3040-\u30ff]")


def _handle_line(levels: Dict[str, int], line: str) -> None:
    if not line:
        return
    words = list(_get_words(line))
    if words:
        histogram = [0, 0, 0, 0, 0, 0]
        for word in words:
            assert word
            if len(word) == 1 and _KANA_PATTERN.match(word):
                # Hardcode Kana detection
                level = 5
            else:
                # 0 is for unknown
                level = levels.get(word, 0)
            histogram[level] += 1
        _print_histogram(histogram)
    else:
        print(line)


def main() -> None:
    levels = anki_load.levels()
    try:
        while True:
            _handle_line(levels, input())
    except EOFError:
        pass


if __name__ == '__main__':
    main()
