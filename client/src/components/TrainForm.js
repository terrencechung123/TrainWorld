import { useEffect, useState } from "react";

function TrainForm({ conductorId, onAddTrain }) {
  const [trains, setTrains] = useState([]);
  const [trainId, setTrainId] = useState("");
  // const [price, setPrice] = useState("");
  const [formErrors, setFormErrors] = useState([]);

  useEffect(() => {
    fetch("/trains")
      .then((r) => r.json())
      .then(setTrains);
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    const formData = {
      train_id: trainId,
      conductor_id: conductorId,
      // price: parseInt(price),
    };
    fetch("/train_rides", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    }).then((r) => {
      if (r.ok) {
        r.json().then((newTrain) => {
          onAddTrain(newTrain);
          setFormErrors([]);
        });
      } else {
        r.json().then((err) => setFormErrors(err.errors));
      }
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="train_id">Train:</label>
      <select
        id="train_id"
        name="train_id"
        value={trainId}
        onChange={(e) => setTrainId(e.target.value)}
      >
        <option value="">Select a train</option>
        {trains.map((train) => (
          <option key={train.id} value={train.id}>
            {train.name}
          </option>
        ))}
      </select>
      {/* <label htmlFor="train_id">Price:</label>
      <input
        type="number"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      /> */}
      {formErrors.length > 0
        ? formErrors.map((err) => (
            <p key={err} style={{ color: "red" }}>
              {err}
            </p>
          ))
        : null}
      <button type="submit">Add To Conductor</button>
    </form>
  );
}

export default TrainForm;
