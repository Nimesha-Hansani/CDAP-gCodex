import React from 'react';
import './App.css';
import store from './store';
import {Provider} from 'react-redux';

import Home from './pages/home.js';
import About from './pages/about.js';
import UserMenu from './pages/UserMenu.js';
import Dashboard from './pages/Dashboard.js'
import Sitepage from './pages/Sitepage.js'

import './bootstrap.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'

function App() {
  return (
    <Provider store={store}>
      <div className="App">
      <Router> 

      <Route exact path="/" render={props => (
        <React.Fragment><Home/></React.Fragment>
      )}/>
  
      <Route path="/about" component={About}/>
      <Route path="/usermenu" component={UserMenu}/>
      <Route path="/dashboard" component={Dashboard}/>
      <Route path="/sitepage" component={Sitepage}/>
    
      </Router>
      </div>
    </Provider>
  );
}

export default App;
