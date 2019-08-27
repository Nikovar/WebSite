def get_text(book_descriptor):
    with book_descriptor.open('r') as book_file:
        text = book_file.read()
    return text
