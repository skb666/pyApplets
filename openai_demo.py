#!python
import os
import argparse
import openai


def init_openai():
    # Set the GPT-3 API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # with open("openai_module.txt", 'w+') as f_obj:
    #     f_obj.write(str(openai.Model.list()))


def get_response(content):
    # Generate some text with GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{content}",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return the generated text
    return response["choices"][0]["text"]


def run_openai(content=''):
    if not content:
        while True:
            try:
                content = input('> ')
                if content == 'exit':
                    break
                print(get_response(content))
            except:
                print("ERROR!")
    else:
        try:
            print(get_response(content))
        except:
            print("ERROR!")



if __name__ == '__main__':
    # 创建一个解析器
    parser = argparse.ArgumentParser()
    # 添加参数
    parser.add_argument("-c", '--content', type=str, help='text content')
    # 解析参数
    args = parser.parse_args()
    content = args.content

    init_openai()
    run_openai(content)
