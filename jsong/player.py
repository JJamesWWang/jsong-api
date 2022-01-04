from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Player:
    uid: str
    username: str
    score: int = 0
    is_correct: bool = False
    is_ready: bool = False
