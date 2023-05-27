import json
from typing import *
import dawdreamer as daw


class Effect:
    name = str
    effect_path = str
    save_state_path = str

    def __init__(self) -> None:
        pass


class Note:
    name = str
    frequency = float
    key = int
    velocity = int
    duration = float

    def __init__(self, frequency, key) -> None:

        self.frequency = frequency
        self.key = key


class Instrument:
    name = str
    instrument_path = str
    save_state_path = str
    
    effects = {str: Effect}
    notes = {str: Note}

    def __init__(self) -> None:
        pass

    def add_note():
        pass

    def add_effect():
        pass


class Project:
    name = str
    instruments = {str: Instrument}
    time_length = float

    def __init__(self) -> None:
        pass

    def load_from_json_file(filepath) -> None:
        pass

    def save_to_json_file(filepath) -> None:
        pass
