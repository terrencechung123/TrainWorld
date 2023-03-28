import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from "./NavBar";
import Login from "../pages/Login";
import TicketList from "../pages/TicketList";
import NewTicket from "../pages/NewTicket";
import UpdateTicket from "../pages/UpdateTicket";
import UserList from "../pages/UserList";
import TrainList from "../pages/TrainList";
import NewTrain from "../pages/NewTrain";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // auto-login
    fetch("/check_session").then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  if (!user) return <Login onLogin={setUser} />;

  return (
    <>
      <NavBar user={user} setUser={setUser} />
      <main>
        <Switch>
          <Route path="/users">
            <UserList user={user}/>
          </Route>
          <Route path="/trains">
            <TrainList/>
          </Route>
          <Route path="/new_train">
            <NewTrain/>
          </Route>
          <Route path="/new">
            <NewTicket user={user} />
          </Route>
          <Route path="/update/:id/edit">
            <UpdateTicket user={user}/>
          </Route>
          <Route path="/">
            <TicketList />
          </Route>
        </Switch>
      </main>
    </>
  );
}

export default App;
