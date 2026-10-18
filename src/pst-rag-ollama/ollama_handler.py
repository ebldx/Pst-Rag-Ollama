import ollama

def embedding_model(model_name:str, input_text:str):
	if (check_embed_model(model_name)):
		embed_data = ollama.embed(model=model_name, input=input_text)
		return embed_data["embeddings"][0]
	else:
		raise ValueError("Invalid model.")

def language_model(model_name:str, input_text:str, system_text:str, stream_output:bool=True):
	if (check_lang_model(model_name)):
		llm_output = ollama.chat(
			model = model_name,
			messages = [
					{"role":"system", "content":system_text},
					{"role":"user", "content":input_text}
				],
			stream = stream_output
		)
		return llm_output
	else:
		raise ValueError("Invalid model.")

def check_embed_model(model_name:str):
	if (len(model_name) >= 1):
		try:
			if (not(model_name in [ollama.list()["models"][i].model for i in range(len(ollama.list()["models"]))])):
				pull = ollama.pull(model_name, stream=True)
				prev_progress = ""
				for progress in pull:
					if (progress["status"] != prev_progress):
						print(progress["status"], flush=True)
						prev_progress = progress["status"]
			return "embedding" in ollama.show(model_name)["capabilities"]
		except ollama.ResponseError:
			return False
	else:
		return False

def check_lang_model(model_name:str):
	if (len(model_name) >= 1):
		try:
			if (not(model_name in [ollama.list()["models"][i].model for i in range(len(ollama.list()["models"]))])):
				pull = ollama.pull(model_name, stream=True)
				prev_progress = ""
				for progress in pull:
					if (progress["status"] != prev_progress):
						print(progress["status"], flush=True)
						prev_progress = progress["status"]
			return "completion" in ollama.show(model_name)["capabilities"]
		except ollama.ResponseError:
			return False
	else:
		return False