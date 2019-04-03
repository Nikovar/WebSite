function getOptions(input, href, additional) {
    return fetch(`${href}?q=${input}${additional ? '&' + additional : ''}`, {credentials: 'same-origin'})
        .then((response) => {
            return response.json()
        }).then((json) => {
            return {options: json}
        });
}

export const getSymbolOptions = (input, book_id) => getOptions(input, '/get_symbols_api', `book_id=${book_id}`);
