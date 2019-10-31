import axios from 'axios';

export const login = user => {
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