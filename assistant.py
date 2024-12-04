from transformers import AutoTokenizer, AutoModelForCausalLM

class CodeGenerator:
    def __init__(self, model_name="Salesforce/codegen-350M-mono"):
        """
        Initializes the CodeGenerator with the model and tokenizer.
        Args:
            model_name (str): The name of the model to load from Hugging Face.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # Define a padding token if not already set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_code(self, input_text, max_length=1500):
        """
        Generates code based on the input text prompt.
        Args:
            input_text (str): The prompt to guide the code generation.
            max_length (int): The maximum length of the generated output.
        Returns:
            str: The generated code.
        """
        # Tokenize the input text
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        # Set attention mask explicitly
        attention_mask = inputs.attention_mask
        # Generate the output with adjusted parameters
        outputs = self.model.generate(
            inputs.input_ids,
            attention_mask=attention_mask,  # Pass attention mask explicitly
            max_length=max_length,  # Allow longer outputs
            num_beams=5,  # Use beam search for better results
            no_repeat_ngram_size=2,  # Avoid repeating phrases
            repetition_penalty=1.2,  # Penalize repetitive tokens
            early_stopping=True,
            pad_token_id=self.tokenizer.pad_token_id  # Set pad token ID explicitly
        )

        # Decode and return the generated code
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded_output

if __name__ == "__main__":
    input_text = """
    write a python program to check whether the user is above 18 age or not by taking prompt of age.
    """
    codegen = CodeGenerator()
    generated_code = codegen.generate_code(input_text)
    print(generated_code)
