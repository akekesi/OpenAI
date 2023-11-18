import os
import json
import random


def reset_states(doc_config: dict, state: int=-1):
    """
    state:
        -1:	default --> random
         0: deleted
         1: active
    """
    for key in doc_config.keys():
        state_ = state
        if state < 0:
            state_ = random.choice([0, 1])
        doc_config[key]["state"] = state_


def reset_types(doc_config: dict, type: int=-1):
    """
    type:
        -1:	default --> random
         0: private
         1: public
    """
    for key in doc_config.keys():
        type_ = type
        if type < 0:
            type_ = random.choice([0, 1])
        doc_config[key]["type"] = type_


def update(path_doc_config, doc_config):
    with open(path_doc_config, "w") as f:
        json.dump(doc_config, f, indent=4)


if __name__ == "__main__":
    # arguments
    path_doc = os.path.join(os.path.dirname(__file__), "..", "doc")
    path_doc_config = os.path.join(path_doc, "doc_config.json")
    with open(path_doc_config, 'r') as f:
        doc_config = json.load(f)

    # reset states
    reset_states(doc_config=doc_config)
    update(path_doc_config=path_doc_config,
                      doc_config=doc_config)

    # reset types
    reset_types(doc_config=doc_config)
    update(path_doc_config=path_doc_config,
                      doc_config=doc_config)
