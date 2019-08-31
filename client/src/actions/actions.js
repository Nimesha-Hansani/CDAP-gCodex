import axios from 'axios';
import {USER_LOGIN} from './types';


export const login = user => {
    console.log("ela2");
    return axios
    .post('/users/login',{
        username :user.USERNAME,
        password :user.PASSWORD

    })
    .then(res => {
        return res.data;
    }
    )
}

export const loadSitePage = user => dispatch => {

    return axios
    .post('/users/login', {
        username :user.USERNAME,
        password :user.PASSWORD
    })
    .then(res => dispatch({
        type: USER_LOGIN,
        payload: res.data
    }))
}


