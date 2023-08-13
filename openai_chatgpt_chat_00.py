"""
sources:
https://www.youtube.com/watch?v=R3mo_OJO5pM
"""
import openai


class ChatGPT35Turbo:
	def __init__(self, api_key: str, role: str):
		openai.api_key = api_key
		self.dialog = [
			{
				"role": "system",
				"content": role
			}
		]

	def question(self, question):
		self.dialog.append(
			{
				"role": "user",
				"content": question
			}
		)
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=self.dialog
		)
		answer = response.choices[0].message.content
		self.dialog.append(
			{
				"role": "assistant",
				"content": answer
			}
		)
		return answer


if __name__ == "__main__":
	# arguments to run chat
	path_api_key = "api.key"						# <-- api.key file, paste your api key there
	path_save_text = "chat_gpt_pirate_BJ.txt"		# <-- txt file to save chat
	role = "Be a pirate who likes Ben & Jerry's."	# <-- role of ChatGPT

	# create ChatGPT
	with open(path_api_key, "r") as api_key_open:
		api_key = api_key_open.read()
	chatgpt = ChatGPT35Turbo(
		api_key=api_key,
		role=role
	)

	# run chat, terminate it with "EXIT"
	with open(path_save_text, "a") as f:
		f.write(f"role: {role}\n")
	while True:
		question = input("\n> ")
		if question == "EXIT":
			break
		answer = chatgpt.question(question=question)
		print(answer)

		with open(path_save_text, "a") as f:
			f.write(f"> {question}\n")
			f.write(f"> {answer}\n")
