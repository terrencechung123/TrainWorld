import { useState, useEffect } from "react";
import { useParams, useHistory } from "react-router-dom";
import { Button, FormField, Input, Label } from "../styles";

function UpdateTicket({ user }) {
  const [trainId, setTrainId] = useState("");
  const [userId, setUserId] = useState("");
  const [price, setPrice] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState(null);
  const { id } = useParams();
  const history = useHistory();

  useEffect(() => {
    fetch(`/tickets/${id}`)
      .then((r) => r.json())
      .then((ticket) => {
        setPrice(ticket.price);
        setTrainId(ticket.train_id);
        setUserId(ticket.user_id);
      });
  }, [id, user.id]);

  function handleChange(e) {
    const { name, value } = e.target;
    if (name === "train_id") {
      setTrainId(value);
    } else if (name === "user_id") {
      setUserId(value);
    } else if (name === "price") {
      setPrice(value);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsLoading(true);
    const updateData = {
      price: price,
      train_id: trainId,
      user_id: userId,
    };
    fetch(`/tickets/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    }).then((response) => {
      setIsLoading(false);
      if (response.ok) {
        history.push("/");
      } else {
        response.json().then((err) => setErrors(err.errors));
      }
    });
  }
  
  return (
    <div>
      <h1>Edit Ticket</h1>
      <form onSubmit={handleSubmit}>
        <FormField>
          <Label htmlFor="price">Price:</Label>
          <Input
            type="number"
            name="price"
            id="price"
            value={price}
            onChange={handleChange}
            required
          />
        </FormField>
        <FormField>
          <Label htmlFor="train_id">Train:</Label>
          <Input
            type="number"
            name="train_id"
            id="train_id"
            value={trainId}
            onChange={handleChange}
            required
          />
        </FormField>
        <FormField>
          <Label htmlFor="user_id">User:</Label>
          <Input
            type="number"
            name="user_id"
            id="user_id"
            value={userId}
            onChange={handleChange}
            required
          />
        </FormField>
        <Button disabled={isLoading} type="submit">
          {isLoading ? "Loading..." : "Update Ticket"}
        </Button>
        {errors && (
          <ul>
            {errors.map((error) => (
              <li key={error}>{error}</li>
            ))}
          </ul>
        )}
      </form>
    </div>
  );
}

export default UpdateTicket;