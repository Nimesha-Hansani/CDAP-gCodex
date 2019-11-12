import {PREDICTION_ITEMS, PREDICTION_LOADING} from '../actions/types';

const initialSearchState = {
    data: [], 
    loading: false
}

export default function(state = initialSearchState, action){
    switch(action.type){
        case PREDICTION_ITEMS:
            return{
                data: action.payload,
                loading: false
            };
        case PREDICTION_LOADING:
            return{
                 ...state,
                 loading: true
            };
        default:
            return state;
    }
}