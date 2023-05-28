import json
from typing import *
import dawdreamer as daw


class Effect:
    def __init__(self, name: str) -> None:
        self.name = name
        self.effect_path = ""
        
    def getEffectPath(self) -> str:
        return self.effect_path
    
    def setEffectPath(self, effect_path: str) -> None:
        self.effect_path = effect_path

class Note:
    def __init__(self, name: str, key: int = 60, frequency: float = 1.0, velocity: int = 100, duration: float = 0.5) -> None:
        self.name: str = name
        self.frequency: float = frequency
        self.key: int = key
        self.velocity: int = velocity
        self.duration: float = duration

    def getName(self) -> str:
        return self.name

    def getFrequency(self) -> float:
        return self.frequency

    def getKey(self) -> int:
        return self.key

    def getVelocity(self) -> int:
        return self.velocity

    def getDuration(self) -> float:
        return self.duration

    def setName(self, name: str) -> None:
        self.name = name

    def setFrequency(self, frequency: float) -> None:
        self.frequency = frequency

    def setKey(self, key: int) -> None:
        self.key = key
    
    def setVelocity(self, velocity: int) -> None:
        self.velocity = velocity
    
    def setDuration(self,duration: float) -> None:
        self.duration = duration

    


class Instrument:
    def __init__(self, name: str) -> None:
        self.name:str = name
        self.instrument_path: str = ""
        self.save_state_path: str = ""

        self.effects:  Dict[str, Effect] = {}
        self.notes: Dict[str, Note] = {}

    def add_note(self, note: Note):
        self.notes.update({note.name: note})

    def add_effect(self, effect: Effect):
        self.effects.update({effect.name: effect})
        
    def getNote(self, name: str) -> Note:
        return self.notes[name]        

    def getEffect(self, name: str) -> Effect:
        return self.effects[name]

    def getEffectCount(self) -> int:
        return len(self.effects)

    def getNoteCount(self) -> int:
        return len(self.notes)
    
    def getName(self) -> str:
        return self.name
    
    def getInstrumentPath(self) -> str:
        return self.instrument_path
    
    def getSave_state_path(self) -> str:
        return self.save_state_path
    
    def getNotes(self) -> Dict[str, Note]:
        return self.notes
    
    def getEffects(self) -> Dict[str, Effect]:
        return self.effects
    
    def setName(self, name: str) -> None:
        self.name = name
    
    def setInstrumentPath(self, instrumentpath: str) -> None:
        self.instrument_path = instrumentpath
    
    def setSave_state_path(self, save_state_path: str) -> None:
        self.save_state_path = save_state_path


class Project:
    def __init__(self, name: str, runtime: float = 10.0, sample_rate: int = 44100) -> None:
        self.name: str = name
        self.instruments: Dict[str, Instrument] = {}
        self.runtime: float = runtime
        self.sample_rate: int = sample_rate

    def load_from_json_file(self, filepath) -> None:
        pass

    def save_to_json_file(self, filepath) -> None:
        pass

    def getNumberOfInstruments(self) -> int:
        return len(self.instruments)

    def addInstrument(self, instrument: Instrument) -> None:
        self.instruments.update({instrument.name: instrument})
    
    def getInstrument(self, name: str) -> Instrument:
        return self.instruments[name]

    def getSampleRate(self)-> int:
        return self.sample_rate
    
    def getRuntime(self) -> float:
        return self.runtime
    
    def getInstruments(self) -> Dict[str, Instrument]:
        return self.instruments
    
    def setSampleRate(self, sample_rate: int) -> None:
        self.sample_rate = sample_rate
    
    def setRuntime(self, runtime:float) -> None:
        self.runtime = runtime
        
    