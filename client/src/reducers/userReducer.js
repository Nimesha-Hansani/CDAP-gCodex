import {USER_LOGIN, ITEMS_LOADING} from '../actions/types';

const initialState = {
    data: [], 
    loading: false
}

export default function(state = initialState, action){
    switch(action.type){
        case USER_LOGIN:
            return{
                ...state,
                data: action.payload,
                loading: false
            };
        case ITEMS_LOADING:
            return{
                 ...state,
                 loading: true
            };
        default:
            return state;
    }
}