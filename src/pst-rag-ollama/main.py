import ollama
import os
import ollama_handler as oh
import pst_handler as ph
import vectors

print("")
embed_model_name = ""
while (not(oh.check_embed_model(embed_model_name))):
	embed_model_name = input("Enter a valid embedding model name: ")

print("")
lang_model_name = ""
while (not(oh.check_lang_model(lang_model_name))):
	lang_model_name = input("Enter a valid language model name: ")

print("")
pst_filename = ""
while (not(os.path.exists(pst_filename))):
	pst_filename = input("Please enter a valid path to your .pst file: ")

print("")
preexisting_json = None
valid_input = False
while (not(valid_input)):
	preexisting_json = input("Do you have a preexisting .json file? (y/N): ").lower().strip()
	if ((preexisting_json == "") or (preexisting_json == "n")):
		preexisting_json = False
		valid_input = True
	elif (preexisting_json == "y"):
		preexisting_json = True
		valid_input = True

print("")
if (preexisting_json):
	json_filename = ""
	while (not(os.path.exists(json_filename))):
		json_filename = input("Please enter a valid path to your .json file: ")
	ThisDataset = ph.Dataset(embed_model_name, pst_filename, json_filename=json_filename)
else:
	ThisDataset = ph.Dataset(embed_model_name, pst_filename)

print("")
user_prompt = ""
while (user_prompt == ""):
	user_prompt = input("Please provide a user prompt: ")

print("\nEmbedding user prompt...")
up_vectors = oh.embedding_model(embed_model, user_prompt)

print("\nCalculating similarities between user prompt and dataset...")
similarities = ThisDataset.check_similarity(up_vectors)
similarities.sort(key=lambda x: x[1], reverse=True)

# Add calculation to see how many emails to include!
max_emails = 3
extracted_emails = similarities[:max_emails]

# Make email presentation prettier.
system_text = f"""
	You are a helpful assistant, answer only using these provided emails as a source. If you are unable to fulfill this requirement, state so clearly. If you use general knowledge when answering the user prompt, state so clearly.

	Provided emails:
	{extracted_emails}
"""

print("Sending content to language model...")
result = oh.language_model(lang_model_name, user_prompt, system_text)
print("\nAnswer: ")
for chunk in result:
	print(chunk["message"]["content"], end="", flush=True)

#