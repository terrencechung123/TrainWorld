import { Route, Switch } from "react-router";
import React, { useEffect, useState } from "react";
import Home from "./Home";
import Navbar from "./Navbar";
import Conductor from "./Conductor";
import Login from "../pages/Login";

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
      <Navbar user={user} setUser={setUser} />
      <main>
        <Switch>
          <Route exact path="/conductors/:id">
            <Conductor user={user} />
          </Route>
          <Route exact path="/">
            <Home />
          </Route>
        </Switch>
      </main>
    </>
  );
}

export default App;

//   return (
//     <>
//       <Navbar />
//       <Switch>
//         <Route exact path="/conductors/:id">
//           <Conductor />
//         </Route>
//         <Route exact path="/">
//           <Home />
//         </Route>
//       </Switch>
//     </>
//   );
// }

// export default App;
