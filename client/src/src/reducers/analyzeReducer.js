import {ANALYZE_ITEMS, ANALYZE_LOADING} from '../actions/types';

const initialSearchState = {
    analyze: [], 
    loading: false
}

export default function(state = initialSearchState, action){
    switch(action.type){
        case ANALYZE_ITEMS:
            return{
                analyze: action.payload,
                loading: false
            };
        case ANALYZE_LOADING:
            return{
                 ...state,
                 loading: true
            };
        default:
            return state;
    }
}