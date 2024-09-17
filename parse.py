from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time
import httpx

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Prioritize Accuracy:** Ensure that the data provided is as accurate and specific to the request as possible."
)

model = OllamaLLM(model="llama3.1")

def parse_with_ollama(dom_chunks, parse_description, retries=3):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        attempt = 0
        while attempt < retries:
            try:
                response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
                print(f"Parsed batch {i} of {len(dom_chunks)}")
                parsed_results.append(response)
                break  # Break the loop on successful parse
            except (httpx.ConnectError, httpx.RequestError) as e:
                attempt += 1
                print(f"Retrying batch {i} of {len(dom_chunks)}, attempt {attempt} due to error: {e}")
                time.sleep(2)  # Delay before retrying
                if attempt == retries:
                    parsed_results.append("")  # Append an empty string for failed parses
            except Exception as e:
                print(f"Unexpected error parsing batch {i} of {len(dom_chunks)}: {e}")
                parsed_results.append("")  # Handle unexpected exceptions
                break  # Exit retry loop for unexpected errors

    return "\n".join(parsed_results)
