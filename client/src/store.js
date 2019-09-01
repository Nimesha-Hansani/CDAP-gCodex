import {createStore, applyMiddleware, compose} from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers/index';

function saveToLocalStorage(state) {
    try{
        const serializedState = JSON.stringify(state);
        localStorage.setItem('state', serializedState);
    }catch(e){
        console.log(e);
    }
}

function loadFromLocalStorage(){
    try{
        const serializedState = localStorage.getItem('state')
        if(serializedState === null ) return undefined
        return JSON.parse(serializedState)
    }catch(e){
        console.log(e)
        return undefined
    }
}

const persistedState = loadFromLocalStorage();

//const initialState = {};
const middleware = [thunk];

const store = createStore(rootReducer, persistedState, compose(
    applyMiddleware(...middleware),
));



store.subscribe(()=> saveToLocalStorage(store.getState()));




//do not delete followings
// const initialState = {};
// const middleware = [thunk];

// const store = createStore(rootReducer, initialState, compose(
//     applyMiddleware(...middleware),
// ));





export default store;