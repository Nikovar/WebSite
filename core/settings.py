APP_PATH = ''

ARTICLE_TITLE_LEN = 100

# use this errors for form.clean method
complex_error_messages = {
    'pass_identity': ' - Пароли должны совпадать.',
    'author_book': ' - У данного автора нет такой книги. Проверьте свои данные.'
}

error_messages = {
    'name': ' - В ФИО допустимы исключительно русские или исключительно английские символы.',
    'login': ' - Логин может состоять из английских символов, цифр, знака подчеркивания и иметь длину от 4 знаков.',
    'password': ' - Длина пароля должна быть не менее 6 символов.',
    'email': ' - Недействительный почтовый адрес.',
}
translated_error_messages = {
    'max_length': '',  # take off your hands! leave this code as is...
    'min_length': '',  # take off your hands! leave this code as is...
    'required': ' - Обязательные поля должны быть заполнены.',
}
