"""
    Module that takes care of writing/reading environment files
    using pickle. Each environment dictionary is written in a file,
    and read from the same file once a module needs it.
"""

import pickle
from masfrl.engine.world import stringify

name = 'environment.pkl'


def save_obj(obj):
    """
    Saves string representation of environment to a pickle file
    :param obj: Environment as string
    :return: 
    """
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_env():
    """
    Loads an environment from a pickle file
    :return: Dictionary representation of the environment
    """
    with open(name, 'rb') as f:
        return pickle.load(f)


def save_env(env):
    """
    Saves environment dictionary to a pickle file
    :param env: Environment dictionary
    :return: 
    """
    env_data = stringify(env)
    save_obj(env_data)
