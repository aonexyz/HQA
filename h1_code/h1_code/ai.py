from openai import OpenAI,APIConnectionError
from typing import Callable

document_prompts = {
    0: "No docstrings or formal documentation at all. Add comments only when absolutely necessary to clarify complex or confusing code",
    1: "very very very minimal Clean, concise documentation, preferably one line",
    2: 'limited documentation - write a brief overview, limited to a few sentences. Key points should be clear without over-explaining.',
    3: 'Balanced documentation with an overview and key details. Keep explanations concise and minimal.',
    4: 'Provide comprehensive documentation with explanations, use cases, and examples. Ensure clarity and ensure you got the right details.'
}

# the double 3 is on purpose :)
h1_chat_system_prompt = """
You are a highly intelligent code converter specialized in converting code to H1-quality {lang} code. H1-quality code adheres to the following guidelines:
0. No hallucinations: dont invent things that arent there yet (for example, dont create a new class out of no where). if you cant convert this file, only write a single line "Error: <short explanation>". no codeblock, and DONT write a placeholder
1. Clear Code
2. No redundant or duplicate code.
3. Concise and Relevant Comments: Include only useful, *professional comments* that describe the code flow or clarify important logic. Avoid trivial comments (e.g., "//set a to 5") and keep comments short.
3. Write comments only when you fully understand the code and its context. *Do not add comments if you're unsure of their correctness or necessity*.
4. Retain only essential, concise comments when absolutely necessary to explain complex logic or the overall flow.
5. {document_prompt}
6. No commented-out or unused code. 
7. High-quality {lang} code with best practices.
8. Thoughtful and meaningful naming conventions.
9. No typos in the code or comments.
10. Smart conversion that improves code without introducing issues.  For example, do not replace variables with functions or make unnecessary changes that alter the code's intent or efficiency.
11. Preserve high-quality code from the original and ensure no functionality is lost. (for example, Make sure you dont change constants values that make the code works.)

Your task is to convert the code strictly according to these principles. The output should be code only. note that the files given to you are just a part of a larger codebase."""

# TODO: define the rules as list, because they take from each other
h1_doc_system_prompt= """
You are a highly intelligent code formatter and documentation helper specialized in improving the documentation of code to H1-quality {lang} comments and documentation H1-quality code adheres to the following guidelines:
0. No hallucinations: dont invent things that arent there yet (for example, dont create a new class out of no where). if you cant convert this file, only write a single line "Error: <short explanation>". no codeblock, and DONT write a placeholder
1. you should keep the original code in any case. your mission is just to add documentation and comments (and sometimes fix typos.)
2. No redundant or duplicate comments
3. Focus on adding or enhancing documentation: Include useful, *professional comments* and docstrings that describe the code flow or clarify important logic, without adding unnecessary details. Avoid trivial comments (e.g., "//set a to 5").
4. Write documentation only when you fully understand the code and its context. *Do not add comments or docstrings if you're unsure of their correctness or necessity*.
5. Ensure proper formatting and use whitespace or indentation to make the code more readable, without altering the functionality.
6. {document_prompt}
8. No commented-out or unused code. 
9. No typos in the code or comments.
10. Retain the functionality of the original code
11. ensure no functionality is lost"""

def get_prompt(human_lang:str,doc_level:int,only_doc: bool):
    if (doc_level >4 or doc_level < 0):
        print(f"doc level ({doc_level}) is not in the range of 0-4")
    
    if only_doc:
        sprompt =  h1_doc_system_prompt
    else:
        sprompt = h1_chat_system_prompt

    return sprompt.format(lang=human_lang,document_prompt=document_prompts[doc_level])

# Default callback that prints streamed messages
print_callback = lambda message: print(message, end="", flush=True)


# Class for configuration settings
class AiConfig:
    def __init__(
        self,
        model: str = "llama3.1",
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "ollama",
    ):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key


def ai(
    source_code: str,
    markdown_lang: str,
    filename:str,
    system_prompt:str,
    config: AiConfig,
    stream_callback: Callable[[str], None] = print_callback,
):
    # Initialize OpenAI client with config parameters
    client = OpenAI(
        base_url=config.base_url,
        api_key=config.api_key,  # required, but unused
    )

    # Set up streaming from the client
    try:
        stream = client.chat.completions.create(
            model=config.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"rewrite this code in H1 quality:\nfilename:{filename}:```{markdown_lang.lower()}\n{source_code}\n```",
                },
            ],
            stream=True,
            stop=["```\n"],
        )
    except APIConnectionError as e:
            print(f"Cannot connect to {config.base_url}\nError:{e}")
            exit(1)

    full_markdown = ""
    for chunk in stream:
        message = chunk.choices[0].delta.content
        if message:
            full_markdown += message
            stream_callback(message)

    # If a valid code block is not found, raise an error
    if f"```{markdown_lang.lower()}" in full_markdown:
        code = full_markdown.split(f"```{markdown_lang.lower()}")[1]
        return code.rstrip('`')
    else:
        raise ValueError(
            full_markdown,'have no codeblock in the correct language'
        )

    # return full_markdown
