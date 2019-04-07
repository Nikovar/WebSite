import C from './constants';


export function init(book_id, page, symbols, text_chunk) {
    return {
        type: C.MENU_INIT,
        data: {
            book_id, 
            page, 
            symbols,
            text_chunk
        }
    }
}

export function get_contexts() {
    return (dispatch, getState) => {
        console.log('IN GET_CONTEXTS!!!!')
    }
}

export function selectSymbol(symbol) {
    return (dispatch, getState) => {
        dispatch({
            type: C.SELECT_SYMBOL, 
            data: {
                symbol
            }
        });
    }
}
