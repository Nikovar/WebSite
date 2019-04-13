
import C from './constants';
import { errorMessageToString } from 'utils';


export function init(book_id, page, number_pages, symbols, existences, text_chunk) {
    return {
        type: C.MENU_INIT,
        data: {
            book_id, 
            page, 
            number_pages,
            symbols,
            existences,
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
                symbol: symbol
            }
        });
    }
}

export function toggleSymbolAddition() {
    return (dispatch, getState) => {
        dispatch({
            type: C.SYMBOL_ADDITION
        });
    }
}

export function updatePage(page) {
    return (dispatch, getState) => {

        dispatch({
            type: C.UPDATE_PAGE_REQUEST
        });

        $.ajax({
            url: `get_page/${page}`,
            type: 'GET',
            dataType: 'json',
            success: data => {
                if (data.status) {
                    dispatch({
                        type: C.UPDATE_PAGE_SUCCESS,
                        data: {
                            page: page,
                            text_chunk: data.data.text_chunk
                        }
                    })
                } else {
                    dispatch({type: C.UPDATE_PAGE_FAILURE, error: errorMessageToString(data.errors)})
                }
            },
            error: () => {0
                dispatch({type: C.UPDATE_PAGE_FAILURE, error: errorMessageToString()})
            }
        })
    }
}
