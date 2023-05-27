import json
from typing import *
import dawdreamer as daw


class Effect:
    name: str = ""
    effect_path: str = ""
    save_state_path: str = ""

    def __init__(self, name: str, effect_path: str) -> None:
        self.name = name
        self.effect_path = effect_path


class Note:
    name: str = ""
    frequency: float = 0.0
    key: int = 0
    velocity: int = 0
    duration: float = 0.0

    def __init__(self, name: str, key: int, frequency_Hz: float = 1.0, velocity: int = 100, duration: float = 0.5) -> None:
        self.frequency = frequency_Hz
        self.key = key
        self.velocity = velocity
        self.duration = duration


class Instrument:
    name: str = ""
    instrument_path: str = ""
    save_state_path: str = ""

    effects:  Dict[str, Effect] = {}
    notes: Dict[str, Note] = {}

    def __init__(self, name: str, instrument_path: str) -> None:
        self.name = name
        self.instrument_path = instrument_path

    def add_note(self):
        pass

    def add_effect(self):
        pass

    def getEffectCount(self) -> int:
        return len(self.effects)

    def getNoteCount(self) -> int:
        return len(self.notes)


class Project:
    name: str = ""
    instruments: Dict[str, Instrument] = {}
    time_length: float = 0.0
    sample_rate: int = 0

    def __init__(self, name: str, length_s: float = 10.0, sample_rate: int = 44100) -> None:
        self.name = name
        self.time_length = length_s
        self.sample_rate = sample_rate

    def load_from_json_file(filepath) -> None:
        pass

    def save_to_json_file(filepath) -> None:
        pass
