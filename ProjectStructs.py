import json

class Project:
    def __init__(self) -> None:
        self.name:str = ""
        self.instruments = {}
    
    def load_from_json_file(filepath) -> None:
        pass

    def save_to_json_file(filepath) -> None:
        pass


class Instrument:
    def __init__(self) -> None:
        self.name:str = ""
        self.effects = {}
        self.notes = {}
        self.instrument_path = ""
        
    def add_note():
        pass
    
    def add_effect():
        pass
    

class Effect:
    def __init__(self) -> None:
        self.name:str = ""
        self.effect_path = ""

class Note:
    def __init__(self, frequency, key) -> None:
        self.name:str = ""
        self.frequency: float = frequency
        self.key:int = key