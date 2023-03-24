import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TrainForm from "./TrainForm";

function Conductor() {
  const [{ data: conductor, error, status }, setConductor] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const { id } = useParams();

  useEffect(() => {
    fetch(`/conductors/${id}`).then((r) => {
      if (r.ok) {
        r.json().then((conductor) =>
          setConductor({ data: conductor, error: null, status: "resolved" })
        );
      } else {
        r.json().then((err) =>
          setConductor({ data: null, error: err.error, status: "rejected" })
        );
      }
    });
  }, [id]);

  function handleAddTrain(newTrain) {
    setConductor({
      data: {
        ...conductor,
        trains: [...conductor.trains, newTrain],
      },
      error: null,
      status: "resolved",
    });
  }

  if (status === "pending") return <h1>Loading...</h1>;
  if (status === "rejected") return <h1>Error: {error.error}</h1>;

  return (
    <section className="container">
      <div className="card">
        <h1>{conductor.name}</h1>
        <p>{conductor.avatar}</p>
      </div>
      <div className="card">
        <h2>Train Menu</h2>
        {conductor.trains.map((train) => (
          <div key={train.id}>
            <h3>{train.name}</h3>
            <p>
              <em>{train.avatar}</em>
            </p>
          </div>
        ))}
      </div>
      <div className="card">
        <h3>Add New Train</h3>
        <TrainForm conductorId={conductor.id} onAddTrain={handleAddTrain} />
      </div>
    </section>
  );
}

export default Conductor;
