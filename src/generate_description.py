from llama_cpp import Llama
from src.utils import load_config

config = load_config()

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
            model_path=config["llm"]["model_path"],
        )
    def clean(self,retrieved_text)->str:
        prompt = """
        <|im_start|>system
        You are tasked with receiving noisy text extracted via OCR that may contain spelling mistakes or garbled characters. Your task is to:

        Guidelines:
        1. Spelling Correction: Correct any spelling mistakes present in the extracted text.
        2. Text Cleaning: Clean any text that is clearly distorted or doesn't make sense due to OCR errors.
        3. Preserve Original Structure: Maintain the original structure of the text.
        <|im_start|>user
        Here is the noisy extracted text: {retrieved_text}
        <|im_end|>

        <|im_start|>assistant
        Here is the cleaned version of the extracted text with correct spellings:
        """
        
        formatted_prompt = prompt.format(retrieved_text=retrieved_text)
        
        output = self.__llm(
            formatted_prompt,          # Prompt
            max_tokens = config["llm"]["max_tokens"],          # Generate up to 10,000 tokens
            temperature = config["llm"]["temperature"],          # Adjust creativity of the output
            stop=["<|im_end|>"],
            echo = config["llm"]["echo"]                 # Do not echo the prompt back in the output
        )
        
        return output['choices'][0]["text"]
    
    def understand_flowgraph(self,cleaned_text:str)->str:
        prompt = """
        <|im_start|>system
        You are expert in interpreting flowgraphs from missing details.You are tasked with understanding the workflow or flowchart described by the cleaned text. Your job is to:

        Guidelines:
        1. Workflow Understanding: Understand the flow or process described in the text.
        2. Relationship Identification: Identify and make sense of the relationships between the components or steps.
        3. Logical Inference: Where the text is unclear or incomplete, use logical assumptions to fill in the gaps and reconstruct the workflow.

        <|im_start|>user
        Here is the cleaned text: {cleaned_text}
        <|im_end|>

        <|im_start|>assistant
        Here is the workflow and the relationships between the steps, with any logical assumptions explained:
        """
        
        formatted_prompt = prompt.format(cleaned_text=cleaned_text)
        
        output = self.__llm(
            formatted_prompt,          # Prompt
            max_tokens = config["llm"]["max_tokens"],          # Generate up to 10,000 tokens
            temperature = config["llm"]["temperature"],          # Adjust creativity of the output
            echo = config["llm"]["echo"]                 # Do not echo the prompt back in the output
        )
        
        return output['choices'][0]["text"]

        
    def describe(self, workflow_understanding: str) -> str:
        prompt = """
        <|im_start|>system
        You are tasked with providing a clear and structured explanation of the workflow based on the relationships understood in the previous step. Your job is to:

        Guidelines:
        1. Organized Explanation: Describe the workflow in a clear and organized manner.
        2. Logical Flow: Ensure that each step or component is logically connected and explained.
        3. Neat Presentation: Provide a concise and well-organized final description of the workflow.

        <|im_start|>user
        Here is the relationship and flow understanding from the previous step: {workflow_understanding}
        <|im_end|>

        <|im_start|>assistant
        Here is the final organized explanation of the workflow:
        """

        formatted_prompt = prompt.format(workflow_understanding=workflow_understanding)
        
        output = self.__llm(
            formatted_prompt,          # Prompt
            max_tokens = config["llm"]["max_tokens"],          # Generate up to 10,000 tokens
            temperature = config["llm"]["temperature"],          # Adjust creativity of the output
            echo = config["llm"]["echo"]                 # Do not echo the prompt back in the output
        )
        
        return output['choices'][0]["text"]
    
    def generate(self,retrieved_text:str)-> str:
        clean_text = self.clean(retrieved_text=retrieved_text)
        flow_text =  self.understand_flowgraph(cleaned_text=clean_text)
        description = self.describe(flow_text)
        
        return description
        
