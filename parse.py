from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import httpx
import time

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

def parse_with_ollama(dom_chunks, parse_description, retries=3, delay=2):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        for attempt in range(retries):
            try:
                print(f"Parsing batch {i} of {len(dom_chunks)}, attempt {attempt + 1}...")  # Log current batch
                
                # Send the request to the model
                response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
                
                # Log the raw response for debugging
                print(f"Raw response for batch {i}: {response}")
                
                # Validate the response
                if response and isinstance(response, str):
                    parsed_results.append(response)
                else:
                    print(f"Warning: Invalid response for batch {i}. Skipping.")
                    parsed_results.append("")  # Append an empty string if response is invalid
                break  # If parsing is successful, break out of the retry loop

            except httpx.HTTPStatusError as e:
                print(f"HTTP error during batch {i}, attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)  # Wait before retrying
                else:
                    parsed_results.append("")  # Append empty result if max retries reached

            except httpx.ConnectError as e:
                print(f"Connection error during batch {i}, attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)  # Wait before retrying
                else:
                    parsed_results.append("")  # Append empty result if max retries reached

            except Exception as e:
                print(f"Error occurred during batch {i}, attempt {attempt + 1}: {e}")
                parsed_results.append("")  # Handle any unexpected error gracefully
                break

    # Join all the results
    result = "\n".join(parsed_results)
    
    # Log final result for debugging
    print(f"Final parsed results:\n{result}")
    
    return result
