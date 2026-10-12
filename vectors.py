def vector_similarity(vector_a, vector_b):
	dot_product = sum([x * y for x, y in zip(vector_a, vector_b)])
	magnitude_a = sum([x ** 2 for x in vector_a]) ** 0.5
	magnitude_b = sum([x ** 2 for x in vector_b]) ** 0.5
	return dot_product / (magnitude_a * magnitude_b)