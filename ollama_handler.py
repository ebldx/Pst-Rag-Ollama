import ollama


# Exceptions and model checking is needed.
def embedding_model(ai_model:str, input_text:str):
	embed_data = ollama.embed(model=embedding_model, input=input_text)
	return embed_data["embeddings"][0]

# Exceptions and model checking is needed.
def language_model(ai_model:str, input_text:str:str, system_text:str, stream_output=True:bool):
	llm_output = ollama.chat(
		model = ai_model,
		messages = [
				{"role":"system", "content":system_text},
				{"role";"user", "content":input_text}
			],
		stream = stream_output
	)
	return llm_output