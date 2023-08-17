"""
sources:
https://www.youtube.com/watch?v=UkvFsyPk6LY
"""
import os
import json
import openai
import requests


class Image:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def create(self,
               prompt: str,
               n: int,
               size: str,
               path_save_image: str):
        response = openai.Image.create(prompt=prompt,
                                       n=n,
                                       size=size)
        # save data
        path, _ = os.path.splitext(path_save_image)
        path_save_data = f"{path}.json"
        self.save_data(data=response,
                       path_save_data=path_save_data)
        # save images
        url_list = [data["url"] for data in response["data"]]
        self.save_image(url_list=url_list,
                        path_save_image=path_save_image)
        return response

    def save_data(self, data, path_save_data: str):
        with open(path_save_data, 'w') as f:
            json.dump(data, f, indent=4)

    def save_image(self, url_list: list, path_save_image: str):
        for n, url in enumerate(url_list):
            response = requests.get(url)
            if response.status_code == 200:
                path, extension = os.path.splitext(path_save_image)
                path_image = f"{path}_{n}{extension}"
                with open(path_image, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Image({url}) download failed")


if __name__ == "__main__":
    # arguments
    path_api_key = "api.key"											# <-- api.key file, paste your api key there
    path_save_image = "image_rubic_niki.png"							# <-- txt file to save chat
    prompt = "Rubic Cube jewellery in style of Niki de Saint Phalle"	# <-- prompt
    n = 1																# <-- number of images to generate
    size = "256x256"													# <-- size images to generate
    with open("api.key", "r") as api_key:
        api_key = api_key.read()

    # generate and save image
    image = Image(api_key=api_key)
    response = image.create(prompt=prompt,
                            n=n,
                            size=size,
                            path_save_image=path_save_image)
    print(response)
