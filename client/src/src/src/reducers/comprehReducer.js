import {COMREHENSION_ITEMS, COMREHENSION_LOADING} from '../actions/types';

const initialSearchState = {
    data: [], 
    loading: false
}

export default function(state = initialSearchState, action){
    switch(action.type){
        case COMREHENSION_ITEMS:
            return{
                data: action.payload,
                loading: false
            };
        case COMREHENSION_LOADING:
            return{
                 ...state,
                 loading: true
            };
        default:
            return state;
    }
}