import React from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import { Home } from "./";
import {ItemDetail} from "./";
function App() {
  return (
    <div className="App">
      <Router basename="shopbridge">
        <Switch>
          <Route path="/" exact component={Home} />
          
          <Route path="/item/:id" component={ItemDetail} />
          
          <Route render={() => <Redirect to="/"/>} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
