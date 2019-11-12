import {SEARCH_ITEMS, SEARCH_LOADING} from '../actions/types';

const initialSearchState = {
    result: [], 
    loading: false
}

export default function(state = initialSearchState, action){
    switch(action.type){
        case SEARCH_ITEMS:
            return{
                result: action.payload,
                loading: false
            };
        case SEARCH_LOADING:
            return{
                 ...state,
                 loading: true
            };
        default:
            return state;
    }
}