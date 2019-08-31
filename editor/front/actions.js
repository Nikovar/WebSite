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
            text_chunk
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

export function selectTextCoordinates(selected_text_coordinates) {
    return (dispatch, getState) => {
        dispatch({
            type: C.SELECT_TEXT_COORDINATES,
            data: {
                selected_text_coordinates: selected_text_coordinates
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
            error: () => {
                dispatch({type: C.UPDATE_PAGE_FAILURE, error: errorMessageToString()})
            }
        })
    }
}

export function tmpSaveSymbol(data) {
    return (dispatch, getState) => {
        dispatch({
            type: C.SYMBOL_SAVE_REQUEST
        });

        data.csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val();
        data.page = getState().editor.page;

        $.ajax({
            type: 'POST',
            url: `store_location/`,
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

export function hideContextModal() {
    return (dispatch, getState) => {
        dispatch({
            type: C.HIDE_CONTEXT_MODAL,
        });
    }
}

export function showContextModal() {
    return (dispatch, getState) => {
        dispatch({
            type: C.SHOW_CONTEXT_MODAL,
        });
    }
}

export function saveNewContext(type_id, description) {
    return (dispatch, getState) => {
        dispatch({
            type: C.SAVE_NEW_CONTEXT_REQUEST
        });

        $.ajax({
            type: 'POST',
            url: `store_context/`,
            dataType: 'json',
            data: {
                type_id: type_id,
                description: description,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
            },
            success: (data) => {
                if (data.status) {
                    alert('Вы успешно создали новый контекст!');
                    dispatch({
                        type: C.SAVE_NEW_CONTEXT_SUCCESS,
                        data: data
                    });
                } else {
                    console.log('somethins wrong...')
                    dispatch({
                        type: C.SAVE_NEW_CONTEXT_FAILURE
                    });
                }
            },
            error: () => {
                console.log('TOTALY HAT')
                dispatch({
                    type: C.SAVE_NEW_CONTEXT_FAILURE
                });
            }
        })
    }
}
