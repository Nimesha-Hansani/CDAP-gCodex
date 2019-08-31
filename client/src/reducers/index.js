import {combineReducers} from 'redux';
import userReducer from './userReducer'; //many reducers

export default combineReducers({
    user: userReducer, // auth: authReducer
});