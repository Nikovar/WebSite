import C from './constants';
import { errorMessageToString } from 'utils';


export function init(start_position, book_id, page, number_pages, symbols, existences, text_chunk) {
    return {
        type: C.MENU_INIT,
        data: {
            start_position,
            book_id, 
            page, 
            number_pages,
            symbols,
            existences,
            text_chunk,
            symbol: symbols.length ? symbols[0] : null
        }
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

export function toggleSymbolAddition(context) {
    return (dispatch, getState) => {
        dispatch({
            type: C.SYMBOL_ADDITION,
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
                            text_chunk: data.data.text_chunk,
                            existences: data.data.existences,
                            start_position: data.data.start_position
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

export function tmpSaveSymbol(context) {
    return (dispatch, getState) => {
        const {page} = getState().editor;
        const token = $('[name=csrfmiddlewaretoken]').val();

        dispatch({
            type: C.SYMBOL_SAVE_REQUEST
        });

        let data = {
            symbol_id: context.symbol.value,
            symbol_title: context.symbol.label,
            description: context.description,
            start: context.start,
            end: context.end,
            word_len: context.word_len,
            word_shift: context.word_shift,
            page: page,
            csrfmiddlewaretoken: token 
        }

        $.ajax({
            type: 'POST',
            url: `tmp_save_symbol/`,
            dataType: 'json',
            data: data,
            success: (data) => {
                if (data.status) {
                    alert('Вы успешно добавили символ!');
                    dispatch({
                        type: C.SYMBOL_SAVE_SUCCESS,
                        data: data
                    });
                } else {
                    console.log('somethins wrong...')
                    dispatch({
                        type: C.SYMBOL_SAVE_FAILURE
                    });
                }
            },
            error: () => {
                console.log('TOTALY HAT')
                dispatch({
                    type: C.SYMBOL_SAVE_FAILURE
                });
            }
        })
    }
}
