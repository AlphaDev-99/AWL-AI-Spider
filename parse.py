from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import httpx

# Define the prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Prioritize Accuracy:** Ensure that the data provided is as accurate and specific to the request as possible."
)

# Initialize the model
model = OllamaLLM(model="llama3.1")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
            print(f"Parsed batch {i} of {len(dom_chunks)}")
            parsed_results.append(response)
        except httpx.ConnectError as e:
            print(f"Connection error during batch {i}: {e}")
            # Optionally retry or log the issue
            parsed_results.append("")  # Append empty result in case of failure

    return "\n".join(parsed_results)
