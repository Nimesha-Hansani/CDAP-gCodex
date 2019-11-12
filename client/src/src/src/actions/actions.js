import axios from 'axios';
import {USER_LOGIN, ITEMS_LOADING, SEARCH_ITEMS, SEARCH_LOADING, ANALYZE_ITEMS, ANALYZE_LOADING,
    COMREHENSION_ITEMS, COMREHENSION_LOADING, COMPLEXITY_ITEMS, COMPLEXITY_LOADING, PREDICTION_ITEMS, PREDICTION_LOADING} from './types';


export const login = user => {
    return axios
    .post('/users/login',user) 
    .then(res => {
        return res.data;
    }
    )
}

export const signout = () => {
    return axios
    .post('/users/signout') 
    .then(res => {
        return res.data;
    }
    )
}




export const loadSitePage = () => dispatch => {
    dispatch(setItemsLoading());
    return axios
    .get('/users/getUserRepo')
    .then(res => dispatch({
        type: USER_LOGIN,
        payload: res.data
    }))
};

export const searching = (type, keyword) => dispatch => {
    dispatch(setSearchLoading());
    return axios
    .get('/users/searchByInputs', {params: {search: type, keyword: keyword}})
    .then(res => dispatch({
        type: SEARCH_ITEMS,
        payload: res.data
    }))
};


//repo structure
export const analyzing = (repo_name) => async dispatch => {
    dispatch(setAnalyzeLoading());
    return await axios
    .get('users/readContents', {params: {repo: repo_name}})
    .then(res => dispatch({
        type: ANALYZE_ITEMS,
        payload: res.data
    }))
};


//comprehension
export const comprehension = (repo_name) => async dispatch => {
    dispatch(comprehensionLoading());
    return await axios
    .get('users/comprehension', {params: {repo: repo_name}})
    .then(res => dispatch({
        type: COMREHENSION_ITEMS,
        payload: res.data
    }))
};


//complexity

export const halsted = (repo_name) => async dispatch => {
    dispatch(complexityLoading());
    return await axios
    .get('users/halstead', {params: {repo: repo_name}})
    .then(res => dispatch({
        type: COMPLEXITY_ITEMS,
        payload: res.data
    }))
};


// prediction
export const prediction = (repo_name) => async dispatch => {
    dispatch(predictionLoading());
    return await axios
    .get('users/forcasting', {params: {repo: repo_name}})
    .then(res => dispatch({
        type: PREDICTION_ITEMS,
        payload: res.data
    }))
};




// loading..
export const setItemsLoading = () => {
    return{
        type: ITEMS_LOADING
    }
}

export const setSearchLoading = () => {
    return{
        type: SEARCH_LOADING
    }
}

export const setAnalyzeLoading = () => {
    return{
        type: ANALYZE_LOADING
    }
}

export const comprehensionLoading = () => {
    return{
        type: COMREHENSION_LOADING
    }
}


export const complexityLoading = () => {
    return{
        type: COMPLEXITY_LOADING
    }
}


export const predictionLoading = () => {
    return{
        type: PREDICTION_LOADING
    }
}
