import os
import json
from aspose.email.storage.pst import PersonalStorage
from aspose.email.mapi import MapiMessage
import ollama_handler as oh
import vectors


class Dataset:
	def __init__(self, embedding_model:str, pst_filename:str, json_filename:str="vector_data.json"):
		self.pst_filename = pst_filename
		self.json_filename = json_filename
		if (not(os.path.exists(json_filename))):
			self.embed_pst()

	def embed_pst(self):
		pst_file = PersonalStorage.from_file(self.pst_filename)
		folders = pst_file.root_folder.get_sub_folder()
		print("Extracting emails...")
		data = extract_email_info(folders, pst_file)
		print("Embedding emails...")
		vector_data = []
		for email_nr, email in enumerate(data, start=1):
			print(f"\tEmail {email_nr} of {len(data)}")
			embed_text = f"Folder: {email["folder"]} To: {email["to"]} From: {email["from_name"]} <{email["from_email"]}> CC: {email["cc"]} BCC: {email["bcc"]} Delivery time: {email["delivery_time"]} Subject: {email["subject"]} Content: {email["content"]}"
			email_vectors = oh.embedding_model(self.embedding_model, embed_text)
			print(f"\t\tEmbedding finished.")
			vector_data.append((email, email_vectors))
			print(f"\t\tVector data saved.")
		json_file = open(this.json_filename, "w")
		json_file.write(json.dumps(vector_data))
		json_file.close()
		print(f"Embedding data saved to {this.json_filename}\n")

	def check_similarity(self, vector:list):
		json_file = open(this.json_filename, "r")
		vector_data = json.loads(json_file)
		json_file.close()

		similarities = []
		for i, email, email_vectors in enumerate(vector_data):
			similarities.append((email, vectors.vector_similarity(email_vectors, vector[i])))
		return similarities
		

# Add typehint.
def extract_email_info(folders, pst_file):
	output = []
	for folder_nr, folder in enumerate(folders, start=1):
		print(f"\tFolder {folder_nr}/{len(folders)}")
		print(f"\t\tFolder name: {folder.display_name}")
		if (folder.has_sub_folders):
			folder_sub_folders = folder.get_sub_folders()
			print("\t\tEntering sub folders...")
			output += extract_email_info(folder_sub_folders, pst_file)
		elif (folder.content_count == 0):
			print("\t\tThe folder is empty.")
		else:
			print(f"\t\tThe folder has {folder.content_count} emails.")
			folder_content = folder.get_contents()
			for email_nr, email in enumerate(folder_content, start=1):
				print(f"\t\tEmail {email_nr}/{folder.content_count}")
				email_info = pst_file.extract_message(email)
				email_content = email_info.body
				print(f"\t\t\tSubject: {mail_info.subject}")
				if (len(email_content) <= 0):
					print("\t\t\tNo email content, skipping...")
				else:
					print("\t\t\tStarting formatting")
					email_content = format_text(email_content)
				email_data = {
					"folder":folder.display_name,
					"to":email_info.display_to,
					"from_name":email_info.sender_name,
					"from_email":email_info.sender_email_address,
					"cc":email_info.display_cc,
					"bcc":email_info.display_bcc,
					"delivery_time":email_info.delivery_time,
					"subject":email_info.subject,
					"content":email_content
				}
				output.append(email_data)
				print(f"\t\t\tSaved: {mail_info.subject}")

# Removes unnaturally large words to remove bannner images which slaughter the context windows of smaller language models.
def format_text(input_text:str, max_word_length:str=60):
	sorted_words = sorted(str(input_text).split(), key=len)
	output_text = str(input_text)
	while (len(sorted_words[-1]) > 60):
		output_text = " ".join(output_text.split(sorted_words[-1]))
		sorted_words = sorted(str(input_text).split(), key=len)
		if (len(output_text) <= 0):
			output_text = str(input_text)
			break #Text would've been emptied.
	return output_text


#