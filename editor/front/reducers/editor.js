import C from '../constants';


const initialState = {

};


export default function editor(state=initialState, action) {

    switch (action.type) {

        case C.SAVE_ANNOTATIONS_REQUEST: 
            return {
                ...state,
                isLoading: true
            }

        default:
            return state;
    }
}