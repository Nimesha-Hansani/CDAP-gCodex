import {combineReducers} from 'redux';
import userReducer from './userReducer'; //many reducers
import searchReducer from './searchReducer';
import analyzeReducer from './analyzeReducer';
import comprehReducer from './comprehReducer';
import complexityReducer from './complexityReducer';
import predictionReducer from './predictionReducer';

export default combineReducers({
    user: userReducer, // auth: authReducer
    search: searchReducer,
    analyze: analyzeReducer,
    comp: comprehReducer,
    complex: complexityReducer,
    predict: predictionReducer
});