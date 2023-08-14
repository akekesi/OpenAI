"""
sources:
https://www.youtube.com/watch?v=m2tXEX5g0BM
https://www.youtube.com/watch?v=R3mo_OJO5pM
"""
import openai


class ChatTextDavinci003:
	def __init__(self, api_key: str):
		openai.api_key = api_key

	def question(self, question: str):
		response = openai.Completion.create(
			model="text-davinci-003",
			prompt=question
		)
		answer = response.choices[0].text
		return answer


if __name__ == "__main__":
	# arguments
	path_api_key = "api.key"			# <-- api.key file, paste your api key there
	path_save_chat = "chat_davinci.txt"	# <-- txt file to save chat
	with open(path_api_key, "r") as api_key_open:
		api_key = api_key_open.read()

	# create chat object
	chatgpt = ChatTextDavinci003(
		api_key=api_key
	)

	# run and save chat, terminate it with "EXIT"
	while True:
		question = input("\n> ")
		if question == "EXIT":
			break
		answer = chatgpt.question(question=question)
		print(answer)

		with open(path_save_chat, "a") as f:
			f.write(f"> {question}\n")
			f.write(f"> {answer}\n")