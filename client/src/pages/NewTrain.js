import { useState } from "react";
import { useHistory } from "react-router";
import styled from "styled-components";
import { Button, Error, FormField, Input, Label, Textarea } from "../styles";

function NewTrain() {
    const [title, setTitle] = useState("");
    const [image, setImage] = useState("");
//   const [origin, setOrigin] = useState("");
//   const [destination, setDestination] = useState("");
//   const [departureTime, setDepartureTime] = useState("");
//   const [arrivalTime, setArrivalTime] = useState("");
//   const [capacity, setCapacity] = useState("");
    const [errors, setErrors] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const history = useHistory();

    function handleSubmit(e) {
        e.preventDefault();
        setIsLoading(true);
        const body = {
            title: title,
            image: image,
    //   origin: origin,
    //   destination: destination,
    //   departure_time: departureTime,
    //   arrival_time: arrivalTime,
    //   capacity: capacity,
        };
        fetch("/trains", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        }).then((r) => {
            setIsLoading(false);
            if (r.ok) {
                history.push("/");
            } else {
                r.json().then((err) => setErrors(err.errors));
            }
        });
    }

  return (
    <Wrapper>
      <WrapperChild>
        <h2>Create Train</h2>
        <form onSubmit={handleSubmit}>
          <FormField>
            <Label htmlFor="title">Title</Label>
            <Input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </FormField>
          {/* <FormField>
            <Label htmlFor="origin">Origin</Label>
            <Input
              type="text"
              id="origin"
              value={origin}
              onChange={(e) => setOrigin(e.target.value)}
            />
          </FormField>
          <FormField>
            <Label htmlFor="destination">Destination</Label>
            <Input
              type="text"
              id="destination"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
            />
          </FormField>
          <FormField>
            <Label htmlFor="departureTime">Departure Time</Label>
            <Input
              type="datetime-local"
              id="departureTime"
              value={departureTime}
              onChange={(e) => setDepartureTime(e.target.value)}
            />
          </FormField>
          <FormField>
            <Label htmlFor="arrivalTime">Arrival Time</Label>
            <Input
              type="datetime-local"
              id="arrivalTime"
              value={arrivalTime}
              onChange={(e) => setArrivalTime(e.target.value)}
            />
          </FormField>
          <FormField>
            <Label htmlFor="capacity">Capacity</Label>
            <Input
              type="number"
              id="capacity"
              value={capacity}
              onChange={(e) => setCapacity(e.target.value)}
            />
          </FormField> */}
          <FormField>
            <Button color="primary" type="submit">
              {isLoading ? "Loading..." : "Create Train"}
            </Button>
          </FormField>
          <FormField>
            {errors.map((err) => (
              <Error key={err}>{err}</Error>
            ))}
          </FormField>
        </form>
    </WrapperChild>
</Wrapper>
);
}

const Wrapper = styled.section`
  max-width: 1000px;
  margin: 40px auto;
  padding: 16px;
  display: flex;
  gap: 24px;
`;

const WrapperChild = styled.div`
  flex: 1;
`;

export default NewTrain;