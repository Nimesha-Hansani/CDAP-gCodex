import axios from 'axios';
import {USER_LOGIN, ITEMS_LOADING, SEARCH_ITEMS, SEARCH_LOADING, ANALYZE_ITEMS, ANALYZE_LOADING} from './types';


export const login = user => {
    return axios
    .post('/users/login',user) 
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

export const analyzing = (repo_name) => dispatch => {
    dispatch(setAnalyzeLoading());
    return axios
    .get('users/readContents', {params: {repo: repo_name}})
    .then(res => dispatch({
        type: ANALYZE_ITEMS,
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

