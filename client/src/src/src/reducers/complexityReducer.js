import {COMPLEXITY_ITEMS, COMPLEXITY_LOADING} from '../actions/types';

const initialSearchState = {
    data: [], 
    loading: false
}

export default function(state = initialSearchState, action){
    switch(action.type){
        case COMPLEXITY_ITEMS:
            return{
                data: action.payload,
                loading: false
            };
        case COMPLEXITY_LOADING:
            return{
                 ...state,
                 loading: true
            };
        default:
            return state;
    }
}