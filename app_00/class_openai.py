import openai


class ChatGPT:
    def __init__(self, api_key: str, role: str):
        openai.api_key = api_key
        self.dialog = [{"role": "system",
                        "content": role}]

    def question(self, question: str):
        self.dialog.append({"role": "user",
                            "content": question})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.dialog
        )
        answer = response.choices[0].message.content
        self.dialog.append({"role": "assistant",
                            "content": answer})
        return answer


class DALLE:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def create(self,
               prompt: str,
               n: int,
               size: str):
        response = openai.Image.create(prompt=prompt,
                                       n=n,
                                       size=size)
        return response["data"][0]["url"]
