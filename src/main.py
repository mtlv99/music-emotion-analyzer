from utils.api_helpers import generate_completion  # Changed to absolute import

def main():
    prompt = "Hello, how are you?"
    response = generate_completion(prompt)
    print(f"Response: {response}")

if __name__ == "__main__":
    main()