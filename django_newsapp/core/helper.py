
def handle_uploaded_file(f, file_name):
	with open(filename, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)