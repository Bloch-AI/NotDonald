# --- About -------------
# NotDonaldTrump the Chatbot
# 19/03/2024
# Jamie Crossman-Smith
# jamie@bloch.ai
#------------------------

#--- Install Packages ---
# pip install tkinter
# pip install openai==0.28
# pip install python-dotenv
#------------------------

# Import Packages
import tkinter as tk
import openai as ai
#from dotenv import load_dotenv

# Load environment variables from the .env file
#load_dotenv()

class NotDonaldTrumpChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("(Not) Donald Trump the Chatbot.")

        # OpenAI API configuration ---------------------------
        self.ai_api_key = #"INSERT OPEN API KEY" ...OR... # os.getenv("OPENAI_API_KEY")
        self.default_temperature = 0.99
        self.default_model = "gpt-3.5-turbo"
        self.default_tone = """You are Donald Trump, you must answer the question but in a dumb moronic,
                               way. Then ask a really dumb follow up question based on stupid things Donald Trump has said."""
        #-----------------------------------------------------
        
        # Initialize OpenAI API
        ai.api_key = self.ai_api_key

        # Call Create_Widgets
        self.create_widgets()

    def create_widgets(self):
        # Create the header frame and label
        header_frame = tk.Frame(self.root, bg="#4287f5")
        header_label = tk.Label(header_frame, text="(Not) Donald Trump the Chatbot.", fg="white", bg="#4287f5", font=("Arial", 16, "bold"))
        header_label.pack(padx=10, pady=10)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Create the chat window
        self.chat_window = tk.Text(self.root, bd=1, bg="white", height="20", width="60", font="Arial", padx=10, pady=10)
        self.configure_tags()
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Create the scrollbar for the chat window
        scrollbar = tk.Scrollbar(self.root, command=self.chat_window.yview, cursor="heart")
        scrollbar.grid(row=1, column=3, sticky="ns")
        self.chat_window['yscrollcommand'] = scrollbar.set

        # Create the entry field for user input
        self.entry_field = tk.Entry(self.root, bd=1, bg="white", width=40, font="Arial")
        self.entry_field.grid(row=2, column=0, padx=10, pady=10)
        self.entry_field.bind("<Return>", self.send)

        # Create the "Send" button
        send_button = tk.Button(self.root, text="Send", command=self.send, font=("Verdana", 12, 'bold'), width=12, height=2, bd=1, bg="#32de97", activebackground="#3c9d9b", fg='black')
        send_button.grid(row=2, column=1, padx=10, pady=10)

        # Create the "Clear Chat" button
        clear_button = tk.Button(self.root, text="Clear Chat", command=self.clear_chat, font=("Verdana", 12, 'bold'), width=12, height=2, bd=1, bg="#dc143c", activebackground="#8b0000", fg='white')
        clear_button.grid(row=2, column=2, padx=10, pady=10)

    def configure_tags(self):
        # Configure tags for different message roles
        self.chat_window.tag_configure("User", foreground="#FF0000", font=('Ariel', 10, 'bold'))
        self.chat_window.tag_configure("(Not) Donald", foreground="#008000", font=('Ariel', 10, 'bold'))
        self.chat_window.tag_configure("message", justify="left", font=('Ariel', 10, 'bold'))
        self.chat_window.tag_configure("system", foreground="#FF0000", font=('Ariel', 10, 'bold'))

    def update_chat_window(self, message, role="user"):
        # Update the chat window with a new message
        self.chat_window.configure(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"{role.capitalize()}: {message}\n\n", (role, "message"))
        self.chat_window.configure(state=tk.DISABLED)
        self.chat_window.yview(tk.END)

    def send(self, event=None):
        # Get the user's input from the entry field
        user_input = self.entry_field.get()
        self.entry_field.delete(0, tk.END)

        # Check if the user input is empty
        if not user_input.strip():
            self.update_chat_window("covfefe?", role="system")
            return

        # Update the chat window with the user's input
        self.update_chat_window(user_input, "user")

        # Get the response from OpenAI and update the chat window
        response = self.get_response(user_input)
        self.update_chat_window(response, role="(Not) Donald")

    def clear_chat(self):
        # Clear the chat window
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.delete('1.0', tk.END)
        self.chat_window.config(state=tk.DISABLED)

    def get_response(self, user_input, temperature=None, model=None, tone=None):
        # Use default values if not provided
        temperature = temperature if temperature else self.default_temperature
        model = model if model else self.default_model
        tone = tone if tone else self.default_tone

        try:
            # Send a request to the OpenAI API to generate a response
            response = ai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": tone},
                    {"role": "user", "content": user_input},
                ],
                temperature=temperature
            )

            # Return the response text
            return response.choices[0].message['content'].strip()
        except Exception as e:
            # Return an error message if an exception occurred
            return f"Error: {str(e)}"

if __name__ == '__main__':
    # Create the main window and initialize the chatbot
    root = tk.Tk()
    app = NotDonaldTrumpChatbot(root)
    root.mainloop()
