import C from '../constants';


const initialState = {
    book_id: null,
    start_position: 0,
    page: 1,
    number_pages: null,
    symbols: [],
    symbol: null,
    existences: {},
    text_chunk: '',
    selected_text_coordinates: {},
    error: '',
    isFetching: false,
    symbolAddition: false,
};


export default function editor(state=initialState, action) {

    switch (action.type) {

        case C.UPDATE_PAGE_REQUEST: 
            return {
                ...state,
                isFetching: true,
                error: ''
            }

        case C.UPDATE_PAGE_SUCCESS: 
            return {
                ...state,
                ...action.data,
                isFetching: false,
                selected_text_coordinates: {},
                symbolAddition: false
            }

        case C.UPDATE_PAGE_FAILURE: 
            return {
                ...state,
                error: action.error,
                isFetching: false
            }


        case C.SYMBOL_SAVE_REQUEST: 
            return {
                ...state,
                isFetching: true,
                error: ''
            }

        case C.SYMBOL_SAVE_SUCCESS:
            return {
                ...state,
                ...action.data,
                isFetching: false,
                symbolAddition: false,
                selected_text_coordinates: {}
            }

        case C.SYMBOL_SAVE_FAILURE:
            return {
                ...state,
                error: action.error,
                isFetching: false,
                selected_text_coordinates: {}
            }

        case C.MENU_INIT: 
            return {
                ...state,
                ...action.data
            }

        case C.SELECT_SYMBOL:
            return {
                ...state,
                ...action.data
            }

        case C.SELECT_TEXT_COORDINATES:
            return {
                ...state,
                ...action.data
            }

        case C.SYMBOL_ADDITION:
            return {
                ...state,
                symbolAddition: !state.symbolAddition
            }

        default:
            return state;
    }
}
