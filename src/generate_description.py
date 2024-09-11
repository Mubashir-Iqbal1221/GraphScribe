from llama_cpp import Llama

class Descriptor:
    """
    A class to describe and analyze flowgraphs based on text extracted through OCR.

    This class utilizes a language model to interpret and clean up text extracted from a flowchart,
    which may contain inaccuracies or incomplete information due to OCR errors.
    """
    
    def __init__(self) -> None:
        """
        Initializes the Descriptor with a language model instance.
        """
        self.__llm = Llama(
            model_path="/home/mubashir/onboarding_project/models/llava-v1.6-mistral-7b.Q4_K_M.gguf",
        )
    
    def generate_desc(self, retrieved_text: str) -> str:
        """
        Generates a description of a flowgraph from the provided OCR-extracted text.

        Constructs a prompt for the language model to interpret and clean up the text,
        making logical assumptions to fill in missing details and identifying potential inaccuracies.

        Args:
            retrieved_text (str): The text extracted from a flowchart by OCR, which may include spelling errors
                                  and incomplete words.

        Returns:
            str: A cleaned and interpreted description of the flowgraph based on the provided text.

        Notes:
            - The method generates up to 10,000 tokens.
        """
        prompt = """
        <|im_start|>system
        You are a highly skilled assistant with expertise in interpreting flowgraphs, flowcharts, and technical diagrams that may be noisy or incomplete due to OCR extraction errors. The OCR process may have missed or misinterpreted some words, making the text inaccurate or incomplete. Your goal is to help the user understand and analyze the content despite these challenges.

        Guidelines:
        1. Critically analyze the extracted text, identifying potential gaps or inaccuracies.
        2. Make logical assumptions to fill in missing details where appropriate.
        3. Inform the user of possible inaccuracies if key details are missing or unclear due to the OCR quality.
        4. If the extracted text is entirely unusable or nonsensical, respond with: "The image you provided is too blurry or unclear to interpret."
        5. Provide a clear, structured interpretation of the extracted text, maintaining as much fidelity to the original structure as possible.
        6. Explain each step of your interpretation in detail to ensure clarity.

        <|im_start|>user
        Describe the workflow for this text extracted from a flowchart by understanding and cleaning: {retrieved_text}
        <|im_end|>

        <|im_start|>assistant
        Here is an explanation of the flowgraph without quoting exact words from the text:
        """

        formatted_prompt = prompt.format(retrieved_text=retrieved_text)
        
        output = self.__llm(
            formatted_prompt,          # Prompt
            max_tokens=10000,          # Generate up to 10,000 tokens
            temperature=0.98,          # Adjust creativity of the output
            echo=False                 # Do not echo the prompt back in the output
        )
        
        return output['choices'][0]["text"]
