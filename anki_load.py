import os
import os.path
import re
from typing import Dict, TYPE_CHECKING

import anki.collection
import anki.importing
import anki.storage

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from anki.collection import _Collection as Collection


def _rmdir_quiet(path: str) -> None:
    if os.path.exists(path):
        os.rmdir(path)


def _delete_quiet(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


def _cleanup() -> None:
    _rmdir_quiet("tmp.media")
    _delete_quiet("tmp.anki2")
    _delete_quiet("tmp.anki2-shm")
    _delete_quiet("tmp.anki2-wal")
    _delete_quiet("tmp.media.db2")


def __load(cwd: str, col: "Collection", path: str) -> None:
    anki.importing.AnkiPackageImporter(col, os.path.join(cwd, "res", path)).run()


def _load(cwd: str, col: "Collection") -> None:
    for path in os.listdir(os.path.join(cwd, "res")):
        __load(cwd, col, path)


_NAME_PAT = re.compile(r"N(\d)", re.IGNORECASE)


def _deck_map(col: "Collection") -> Dict[int, int]:
    decks: Dict[int, int] = {}
    for deck in col.decks.all():
        name = deck["name"]
        if name == "Default":
            continue
        level = _NAME_PAT.search(name).group(1)
        assert level
        decks[deck["id"]] = int(level)
    return decks


def _levels(cwd: str, col: "Collection") -> Dict[str, int]:
    _load(cwd, col)
    results: Dict[str, int] = {}
    decks = _deck_map(col)
    for card_id in col.findCards(""):
        card = col.getCard(card_id)
        level = decks[card.did]
        note = col.getNote(card.nid)
        word = note.fields[0]
        # Measure at lowest JLPT level when word has multiple readings
        results[word] = max(results.get(word, 0), level)
    return results


def levels() -> Dict[str, int]:
    _cleanup()
    cwd = os.getcwd()
    col = anki.storage.Collection("tmp.anki2")
    try:
        return _levels(cwd, col)
    finally:
        os.chdir(cwd)
        _cleanup()
