from tkinter import *
import customtkinter 
import openai
import os
import pickle


root = customtkinter.CTk()
root.title("iChat Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico') # https://tkinter.com/ai_lt.ico


# Color Scheme

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


# Submit to ChatGPT
def speak():
	if chat_entry.get():
		filename = "api_key"
		try:
			if os.path.isfile(filename):
				input_file = open(filename, 'rb')

				# Load the data from the file into a variable
				variable = pickle.load(input_file)

				# Query ChatGPT
				# Define API Key to ChatGPT
				openai.api_key = variable

				# Creat an instance
				openai.Model.list()

				# Define our Query / Response
				response = openai.Completion.create(
					model="text-davinci-003",
					prompt=chat_entry.get(),
					temperature=0.5,
					max_tokens=60,
					top_p=1.0,
					frequency_penalty=0.0,
					presence_penalty=0.0
					)

				my_text.insert(END, (response["choices"][0]["text"]).strip())
				my_text.insert(END, "\n\n")
				
			else:
				# Create the file
				input_file = open(filename, 'wb')
				input_file.close()

				# Error message on API Key
				my_text.insert(END, "\n\n You need an API Key to Talk with ChatGPT. Get one here: \nhttps://beta.openai.com/account/api-keys")

		except Exception as e:
			my_text.insert(END, f"\n\n There was an error! \n\n{e}")
	else:
		my_text.insert(END, "\n\n Did you forget to type what you thought?? \n")


# Clear Screen
def clear():
	# Clear main response box
	my_text.delete(1.0,END)

	# Clear input entry box
	chat_entry.delete(0,END)

# Edit API Key
def key():
	
	# Define a Filename
	filename = "api_key"

	try:
		if os.path.isfile(filename):
			input_file = open(filename, 'rb')

			# Load the data from the file into a variable
			variable = pickle.load(input_file)

			# Output variable to entry text box
			api_entry.insert(END, variable)
		else:
			# Create the file
			input_file = open(filename, 'wb')
			input_file.close()

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error! \n\n{e}")



	# Resize App
	root.geometry('600x750')
	# Reshow API Frame
	api_frame.pack(pady=30)



# Save API Key
def save_key():
	# Deine the file
	filename = "api_key"

	try:

		# Open File
		output_file = open(filename,'wb')

		# Add the data to the file
		pickle.dump(api_entry.get(),output_file)

		# Delete Entry Box
		api_entry.delete(0,END)

		# Disappear Save Widget
		api_frame.pack_forget()
		# Resize App
		root.geometry('600x600')

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error! \n\n{e}")

# Text Frame for Responses

text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)


# Text Widget for Responses

my_text = Text(text_frame,
	bg ="#343638",
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground="#1F538D"
	)
my_text.grid(row=0, column=0)

#Scrollbar for Text Widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)

text_scroll.grid(row=0, column=1, sticky="ns")


# Scrollbar for textbox
my_text.configure(yscrollcommand=text_scroll.set)


# Entry box
chat_entry = customtkinter.CTkEntry(root,
	placeholder_text="Start your chat here...",
	width=535,
	height=50,
	border_width=1)
chat_entry.pack(pady=10)

# Button Frame
button_frame = customtkinter.CTkFrame(root,fg_color="#242424")
button_frame.pack(pady=30)


# Create Submit Button
submit_button = customtkinter.CTkButton(button_frame,
	text="Speak to ChatGPT",
	command=speak)
submit_button.grid(row=0, column=0, padx=25)

# Create Clear Button
clear_button = customtkinter.CTkButton(button_frame,
	text="Clear Chat",
	command=clear)
clear_button.grid(row=0, column=1, padx=35)

# Create API Button
api_button = customtkinter.CTkButton(button_frame,
	text="Update API Key",
	command=key)
api_button.grid(row=0, column=2, padx=25)


# Add API Key Frame
api_frame = customtkinter.CTkFrame(root,border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text = "Enter your API key:",
	width = 350,
	height = 50,
	border_width=1)
api_entry.grid(row=0, column=0, padx=2, pady=20)


# Add API Save Button
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)



root.mainloop()