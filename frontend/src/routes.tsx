import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import React from "react";
import { Rounds } from "./views/rounds";
import { Round } from "./views/round";
import { Home } from "./views/home";
import { Polls } from "./views/polls";

export const AppRouter = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Home} />
        {/* <Route path="/rounds" component={Rounds} /> */}
        <Route path="/round/:id" component={Round} />
        <Route path="/polls" component={Polls} />
      </Switch>
    </Router>
  );

}
