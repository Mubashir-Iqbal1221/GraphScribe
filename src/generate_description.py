from llama_cpp import Llama
from prompt_optimizer.poptim import EntropyOptim
from loguru import logger

class Descriptor:
    """
    A class to describe and analyze flowgraphs based on text extracted through OCR.

    This class utilizes a language model to interpret and clean up text extracted from a flowchart,
    which may contain inaccuracies or incomplete information due to OCR errors.
    """
    
    def __init__(self,config) -> None:
        """
        Initializes the Descriptor with a language model instance.
        """
        self.config = config
        self.__llm = Llama(
            model_path=self.config["model_path"],
        )
    
    def __invoke_llm(self,prompt:str, text:str, fast = False)->str:
        
        formatted_prompt = prompt.format(retrieved_text=text)
        if fast:
            p_optimizer = EntropyOptim(p=0.1)
            result = p_optimizer(formatted_prompt)
            logger.info(f"Original results: {formatted_prompt}")
            formatted_prompt = result.content #replace formated prompt with the optimized prompt
            logger.info(f"Optimized Prompt: {formatted_prompt}")
        
        output = self.__llm(
            formatted_prompt,          # Prompt
            max_tokens = self.config["max_tokens"],          # Generate up to 10,000 tokens
            temperature = self.config["temperature"],          # Adjust creativity of the output
            stop=["<|im_end|>"],
            echo = self.config["echo"]                 # Do not echo the prompt back in the output
        )
        
        return output['choices'][0]["text"]
    
    def __clean(self,retrieved_text : str) -> str:
        prompt = """
                <|im_start|>system
                You are tasked with receiving noisy text extracted via OCR that may contain spelling mistakes or garbled characters. Your task is to:

                Guidelines:
                1. Spelling Correction: Correct any spelling mistakes present in the extracted text.
                2. Text Cleaning: Clean any text that is clearly distorted or doesn't make sense due to OCR errors.
                3. Preserve Original Structure: Maintain the original structure of the text as much as possible, only correcting obvious mistakes.
                <|im_start|>user
                Here is the noisy extracted text: {retrieved_text}
                <|im_end|>

                <|im_start|>assistant
                Here is the cleaned version of the extracted text:
             """
        result = self.__invoke_llm(prompt=prompt,text=retrieved_text)
        
        return result
    
    def __understand(self,retrieved_text : str) -> str:
        prompt = """
                <|im_start|>system
                You are expert in interpreting flowgraphs from missing details.You are tasked with understanding the workflow or flowchart described by the cleaned text. Your job is to:

                Guidelines:
                1. Workflow Understanding: Understand the flow or process described in the text.
                2. Relationship Identification: Identify and make sense of the relationships between the components or steps.
                3. Logical Inference: Where the text is unclear or incomplete, use logical assumptions to fill in the gaps and reconstruct the workflow.

                <|im_start|>user
                Here is the cleaned text: {retrieved_text}
                <|im_end|>

                <|im_start|>assistant
                Here is the workflow and the relationships between the steps, with any logical assumptions explained:
            """
        result = self.__invoke_llm(prompt=prompt,text=retrieved_text)
        
        return result

        
    def __describe(self, retrieved_text: str) -> str:
        prompt = """
                <|im_start|>system
                You are tasked with providing a clear and structured explanation of the workflow based on the relationships understood in the previous step. Your job is to:

                Guidelines:
                1. Organized Explanation: Describe the workflow in a clear and organized manner.
                2. Logical Flow: Ensure that each step or component is logically connected and explained.
                3. Neat Presentation: Provide a concise and well-organized final description of the workflow.

                <|im_start|>user
                Here is the relationship and flow understanding from the previous step: {retrieved_text}
                <|im_end|>

                <|im_start|>assistant
                Here is the final organized explanation of the workflow:
            """

        result = self.__invoke_llm(prompt=prompt,text=retrieved_text)
        return result
    
    def __fast_generate(self,retrieved_text:str)-> str:
        prompt ="""
        <|im_start|>system
                You are tasked with analyzing text extracted via OCR that may contain errors and describing the workflow it represents. Your task is to:

                1. Clean the text by correcting any spelling mistakes or garbled characters while preserving its original structure.
                2. Understand the workflow described, identify relationships between steps, and use logical assumptions to fill in any gaps.
                3. Provide a clear and organized explanation of the workflow, ensuring each step is logically connected and presented concisely.

                <|im_start|>user
                Here is the noisy extracted text: {retrieved_text}
                <|im_end|>

                <|im_start|>assistant
                Here is the cleaned version of the extracted text:
        """
        result = self.__invoke_llm(prompt=prompt,text=retrieved_text,fast=True)
        return result
        
    
    def generate(self, retrieved_text : str, fast_generate : bool = False )-> str:
        """
        Generates a description based on the retrieved text by cleaning it, analyzing its flow, 
        and then describing the processed flow.

        Args:
            retrieved_text (str): The raw input text that needs to be processed.

        Returns:
            str: A description generated after processing the cleaned and analyzed text.
        """
        if fast_generate:
            return self.__fast_generate(retrieved_text=retrieved_text)
        
        clean_text = self.__clean(retrieved_text=retrieved_text)
        flow_text =  self.__understand(retrieved_text=clean_text)
        description = self.__describe(retrieved_text=flow_text)
        
        return description
        
