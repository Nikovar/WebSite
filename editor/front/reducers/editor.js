import C from '../constants';


const initialState = {
    book_id: null,
    page: 1,
    number_pages: null,
    symbols: [],
    symbol: null,
    existences: null,
    text_chunk: '',
    error: '',
    isFetching: false,
};


export default function editor(state=initialState, action) {

    switch (action.type) {

        case C.UPDATE_PAGE_REQUEST: 
            return {
                ...state,
                ifFetching: true,
                error: ''
            }

        case C.UPDATE_PAGE_SUCCESS: 
            return {
                ...state,
                ...action.data,
                isFetching: false,
            }

        case C.UPDATE_PAGE_FAILURE: 
            return {
                ...state,
                error: action.error,
                isFetching: false

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

        default:
            return state;
    }
}
