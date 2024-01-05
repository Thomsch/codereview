from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.
    llm = ChatOpenAI()
    llm.invoke("how can langsmith help with testing?")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
