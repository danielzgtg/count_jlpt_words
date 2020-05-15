#!/usr/bin/python3.8

assert __name__ == '__main__'

if True:
    import sys
    sys.path.append("/usr/share/anki")
    import anki_load
    import re
    import unicodedata
    from typing import Dict, Generator, Iterable, List, Optional


def _get_words(line: str) -> Iterable[str]:
    """Gets desired words such as Japanese ones, excluding undesired ones such as English ones."""
    if not line:
        return
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


def _handle_line(levels: Dict[str, int], histogram: List[int], words: Iterable[str]) -> None:
    for word in words:
        assert word
        if len(word) == 1 and _KANA_PATTERN.match(word):
            # Hardcode Kana detection
            level = 5
        else:
            # 0 is for unknown
            level = levels.get(word, 0)
        histogram[level] += 1


def _worker(levels: Dict[str, int]) -> Generator[None, str, None]:
    histogram: Optional[List[int]] = None
    while True:
        line = yield
        words = list(_get_words(line))
        if words:
            if not histogram:
                histogram = [0, 0, 0, 0, 0, 0]
            _handle_line(levels, histogram, words)
        else:
            if histogram:
                _print_histogram(histogram)
                histogram = None
            print(line)


def main() -> None:
    levels = anki_load.levels()
    worker = _worker(levels)
    next(worker)
    try:
        while True:
            line = input()
            worker.send(line)
    except EOFError:
        pass
    # Flush last histogram
    worker.send("")


if __name__ == '__main__':
    main()
