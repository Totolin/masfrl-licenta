import pickle
from masfrl.engine.world import stringify

name = 'environment.pkl'

def save_obj(obj):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_env():
    with open(name, 'rb') as f:
        return pickle.load(f)


def save_env(env):
    env_data = stringify(env)
    save_obj(env_data)
