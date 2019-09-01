import {combineReducers} from 'redux';
import userReducer from './userReducer'; //many reducers
import searchReducer from './searchReducer';
import analyzeReducer from './analyzeReducer';

export default combineReducers({
    user: userReducer, // auth: authReducer
    search: searchReducer,
    analyze: analyzeReducer
});