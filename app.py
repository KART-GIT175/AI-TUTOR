import os
from groq import Groq
from typing import List, Dict
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AITutor:
    def __init__(self, api_key: str = None):
        """
        Initialize the AI Tutor with Groq API key.

        Args:
            api_key: Groq API key. If not provided, will look for GROQ_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass api_key parameter.")

        self.client = Groq(api_key=self.api_key)
        self.conversation_history: List[Dict[str, str]] = []
        self.model = "mixtral-8x7b-32768"  # Good for educational content

    def set_subject(self, subject: str):
        """Set the learning subject for the tutor session."""
        self.subject = subject
        system_message = f"""You are an expert AI tutor specializing in {subject}.
        Your role is to:
        1. Explain concepts clearly and patiently
        2. Break down complex topics into simple steps
        3. Provide practical examples and analogies
        4. Ask questions to check understanding
        5. Adapt your teaching style to the student's responses
        6. Encourage and motivate learning

        Always be encouraging, patient, and thorough in your explanations.
        Use simple language and build upon previous knowledge."""

        self.conversation_history = [{"role": "system", "content": system_message}]

    def ask_question(self, question: str) -> str:
        """
        Ask the tutor a question and get a response.

        Args:
            question: The student's question

        Returns:
            The tutor's response
        """
        # Add user question to conversation
        self.conversation_history.append({"role": "user", "content": question})

        try:
            # Get response from Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=1000,
                temperature=0.7
            )

            tutor_response = response.choices[0].message.content

            # Add tutor response to conversation history
            self.conversation_history.append({"role": "assistant", "content": tutor_response})

            return tutor_response

        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."

    def get_learning_progress(self) -> str:
        """Get a summary of the learning progress so far."""
        if len(self.conversation_history) <= 1:
            return "We haven't started learning yet. What would you like to learn about?"

        # Create a summary prompt
        summary_prompt = "Based on our conversation so far, please provide a brief summary of what we've covered and suggest the next learning steps."

        self.conversation_history.append({"role": "user", "content": summary_prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=500,
                temperature=0.5
            )

            summary = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": summary})

            return summary

        except Exception as e:
            return f"Unable to generate progress summary: {str(e)}"

    def reset_conversation(self):
        """Reset the conversation history while keeping the system message."""
        if self.conversation_history:
            system_msg = self.conversation_history[0]
            self.conversation_history = [system_msg]

def main():
    """Main interactive tutor application."""
    print("🤖 Welcome to your AI Tutor powered by Groq!")
    print("=" * 50)

    # Initialize tutor
    try:
        tutor = AITutor()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nTo use this tutor, you need to:")
        print("1. Sign up for Groq API at https://groq.com")
        print("2. Get your API key")
        print("3. Set it as an environment variable: set GROQ_API_KEY=your_key_here")
        return

    # Get subject
    subject = input("What subject would you like to learn about? ").strip()
    if not subject:
        subject = "general programming"  # default

    tutor.set_subject(subject)
    print(f"\n📚 Great! I'll be your {subject} tutor. Ask me anything!\n")

    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thanks for learning with me! Goodbye!")
                break

            elif user_input.lower() == 'progress':
                progress = tutor.get_learning_progress()
                print(f"\n📊 Learning Progress:\n{progress}\n")

            elif user_input.lower() == 'reset':
                tutor.reset_conversation()
                print("\n🔄 Conversation reset. What would you like to learn?\n")

            elif user_input.lower() == 'help':
                print("\n📖 Commands:")
                print("- 'progress': Get learning summary")
                print("- 'reset': Start fresh conversation")
                print("- 'quit': Exit the tutor")
                print("- Or just ask your question!\n")

            else:
                if user_input:
                    response = tutor.ask_question(user_input)
                    print(f"\n🤖 Tutor: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Thanks for learning! Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
