import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { Box, Button } from "../styles";

function TrainList() {
  const [trains, setTrains] = useState([]);

  useEffect(() => {
    fetch("/trains")
      .then((r) => r.json())
      .then(setTrains);
  }, []);

  return (
    <Wrapper>
      {trains.length > 0 ? (
        trains.map((train) => (
          <Train key={train.id}>
            <Box>
              <h2>{train.title}</h2>
              <p>
                <em>Time to Complete: {train.minutes_to_complete} minutes</em>
                &nbsp;·&nbsp;
                <cite>By {train.user.username}</cite>
              </p>
              <ReactMarkdown>{train.instructions}</ReactMarkdown>
            </Box>
          </Train>
        ))
      ) : (
        <>
          <h2>No Trains Found</h2>
          <Button as={Link} to="/new">
            Make a New Train
          </Button>
        </>
      )}
    </Wrapper>
  );
}

const Wrapper = styled.section`
  max-width: 800px;
  margin: 40px auto;
`;

const Train = styled.article`
  margin-bottom: 24px;
`;

export default TrainList;
