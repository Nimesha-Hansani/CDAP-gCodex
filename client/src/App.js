import React from 'react';
import './App.css';
import Home from './pages/home.js';
import About from './pages/about.js';
import UserMenu from './pages/UserMenu.js';

import './bootstrap.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'

function App() {
  return (
    <div className="App">
    <Router>

    <Route exact path="/" render={props => (
      <React.Fragment><Home/></React.Fragment>
    )}/>

    <Route path="/about" component={About}/>
    <Route path="/usermenu"component={UserMenu}/>

    </Router>
    </div>
  );
}

export default App;
