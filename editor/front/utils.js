export const BLACK = '#000000';
export const WHITE = '#ffffff';
export const SQUARE_BRACKET = 'square-bracket';

export const COLOR_SCHEME = {
    0: "#9400d3",
    1: "#ff0000",
    2: "#008080",
    3: "#ffa500",
    4: "#0000ff",
    5: "#ffff00",
    6: "#87cefa",
};

function getOptions(input, href, additional) {
    return fetch(`${href}?q=${input}${additional ? '&' + additional : ''}`, {credentials: 'same-origin'})
        .then((response) => {
            return response.json()
        }).then((json) => {
            return json.result;
        });
}

export const getContexts = (input) => getOptions(input, '/editor/contexts/');
export const getContextTypes = (input) => getOptions(input, '/editor/context_types')