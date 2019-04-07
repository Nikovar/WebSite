import C from '../constants';


const initialState = {
    book_id: null,
    page: null,
    symbols: [],
    symbol: null,
    text_chunk: '',
};


export default function editor(state=initialState, action) {

    switch (action.type) {

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
