import os
import json
import random


def reset_states(docs_data: dict, state: int=1):
	"""
	state:
		1: 	default --> state = 1
		-1:	random
	"""
	for key in docs_data.keys():
		state_ = state
		if state < 0:
			state_ = random.choice([0, 1])
		docs_data[key]["state"] = state_


def reset_types(docs_data: dict, type: int=-1):
	"""
	type:
		-1:	default --> random
	"""
	for key in docs_data.keys():
		type_ = type
		if type < 0:
			type_ = random.choice([0, 1, 2])
		docs_data[key]["type"] = type_


def update_docs(path_docs, docs_data):
	with open(path_docs, "w") as f:
		json.dump(docs_data, f, indent=4)


if __name__ == "__main__":
	# arguments for functions
	path_git_docs = "docs"
	name_docs = "00_docs.json"
	path_docs = os.path.join(os.path.dirname(__file__), path_git_docs, name_docs)
	with open(path_docs, 'r') as f:
		docs_data = json.load(f)

	# functions
	reset_states(docs_data=docs_data)
	update_docs(path_docs=path_docs,
	     		docs_data=docs_data)

	reset_types(docs_data=docs_data)
	update_docs(path_docs=path_docs,
	     		docs_data=docs_data)
