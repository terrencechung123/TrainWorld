import { useState } from "react";
import { useHistory } from "react-router";
import styled from "styled-components";
import ReactMarkdown from "react-markdown";
import { Button, Error, FormField, Input, Label, Textarea } from "../styles";

function NewTicket({ user }) {
  const [price, setPrice] = useState("");
  const [trainId, setTrainId] = useState("");
  const [userId, setUserId] = useState("");
  const [errors, setErrors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const history = useHistory();


  // function handleSubmit(e) {
  //   e.preventDefault();
  //   setIsLoading(true);
  //   fetch("/tickets", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify({
  //       price: price,
  //       train_id: trainId,
  //       user_id: userId,
  //     }),
  //   }).then((r) => {
  //     setIsLoading(false);
  //     if (r.ok) {
  //       history.push("/");
  //     } else {
  //       r.json().then((err) => setErrors(err.errors));
  //     }
  //   });
  // }
  function handleSubmit(e) {
    e.preventDefault();
    setIsLoading(true);
    Promise.all([
      fetch(`/trains/${trainId}`).then((r) => r.json()),
      fetch(`/users/${userId}`).then((r) => r.json()),
    ])
      .then(([trainData, userData]) => {
        const body = {
          price: price,
          train_id: trainId,
          user_id: userId,
        };
        return fetch("/tickets", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        });
      })
      .then((r) => {
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
        <h2>Create Ticket</h2>
        <form onSubmit={handleSubmit}>
          <FormField>
            <Label htmlFor="price">Price</Label>
            <Input
              type="number"
              id="price"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </FormField>
          <FormField>
            <Label htmlFor="trainId">Train ID</Label>
            <Input
              type="number"
              id="trainId"
              value={trainId}
              onChange={(e) => setTrainId(e.target.value)}
            />
          </FormField>
          <FormField>
            <Label htmlFor="userId">User ID</Label>
            <Input
              type="number"
              id="userId"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
          </FormField>
          <FormField>
            <Button color="primary" type="submit">
              {isLoading ? "Loading..." : "Submit Ticket"}
            </Button>
          </FormField>
          <FormField>
            {errors.map((err) => (
              <Error key={err}>{err}</Error>
            ))}
          </FormField>
        </form>
      </WrapperChild>
      <WrapperChild>
        <h1>{price}</h1>
        <p>
          <cite>By {user.username}</cite>
        </p>
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

export default NewTicket;