import { Route, Switch } from "react-router";
import Home from "./Home";
import Navbar from "./Navbar";
import Conductor from "./Conductor";

function App() {
  return (
    <>
      <Navbar />
      <Switch>
        <Route exact path="/conductors/:id">
          <Conductor />
        </Route>
        <Route exact path="/">
          <Home />
        </Route>
      </Switch>
    </>
  );
}

export default App;
