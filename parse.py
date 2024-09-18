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

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Log the chunk size and contents
        print(f"Parsing batch {i} of {len(dom_chunks)}: {chunk[:200]}...")  # Print the first 200 characters for reference

        # Invoke Ollama for parsing
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})

        # Handle empty response more effectively
        if not response or response.strip() == '':
            print(f"No relevant data found in chunk {i}.")
        else:
            print(f"Parsed response for batch {i}: {response}")
            parsed_results.append(response)

    # Combine results and remove any empty entries
    final_result = "\n".join(parsed_results).strip()
    
    # Log the final output
    print(f"Final parsed data:\n{final_result}")
    return final_result if final_result else "No relevant data extracted."

