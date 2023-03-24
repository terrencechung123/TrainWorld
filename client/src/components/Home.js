import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [conductors, setConductors] = useState([]);

  useEffect(() => {
    fetch("/conductors")
      .then((r) => r.json())
      .then(setConductors);
  }, []);

  function handleDelete(id) {
    fetch(`/conductors/${id}`, {
      method: "DELETE",
    }).then((r) => {
      if (r.ok) {
        setConductors((conductors) =>
          conductors.filter((conductor) => conductor.id !== id)
        );
      }
    });
  }

  return (
    <section className="container">
      {conductors.map((conductor) => (
        <div key={conductor.id} className="card">
          <h2>
            <Link to={`/conductors/${conductor.id}`}>{conductor.name}</Link>
          </h2>
          <p>Avatar: {conductor.avatar}</p>
          <button onClick={() => handleDelete(conductor.id)}>Delete</button>
        </div>
      ))}
    </section>
  );
}

export default Home;
