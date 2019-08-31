import {USER_LOGIN} from '../actions/types';

const initialState = {
    data: [], 
    loading: false
}

export default function(state = initialState, action){
    switch(action.type){
        case USER_LOGIN:
            console.log(action.payload);
            return{
                ...state,
                data: action.payload,
                loading: false
            };
        default:
            return state;
    }
}