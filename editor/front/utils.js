function getOptions(input, href, additional) {
    return fetch(`${href}?q=${input}${additional ? '&' + additional : ''}`, {credentials: 'same-origin'})
        .then((response) => {
            return response.json()
        }).then((json) => {
            return json
        });
}

export const getSymbolOptions = (input, book_id) => getOptions(input, '/editor/symbols', `book_id=${book_id}`);
