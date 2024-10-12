from pathlib import Path
from spacy.util import load_model_from_init_py, get_model_meta

file = Path(__file__).parent
#__version__ = get_model_meta(Path(file).parent)['version']

def load(**overrides):
    return load_model_from_init_py(__file__, **overrides)