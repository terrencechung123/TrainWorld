import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { Box, Button } from "../styles";

function TicketList() {
  const [tickets, setTickets] = useState([]);


  useEffect(() => {
    fetch("/tickets")
    .then((r) => r.json())
    .then(setTickets);
  }, []);


  function handleDeleteTicket(id) {
    fetch(`/tickets/${id}`, {
      method: "DELETE",
    }).then((r) => {
      if (r.ok) {
        setTickets((tickets) =>
        tickets.filter((ticket) => ticket.id !== id)
        );
      }
    });
  }

  const updateTicket = async (id, data) => {
    const response = await fetch(`/tickets/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message);
    }

    const ticketData = await response.json();
    return ticketData;
  };

  // function handleUpdateTicket(newTicket){
  //   setTickets(tickets => [...tickets, newTicket])
  // }

  // async function updateTicket(){
  //   const updateData = {
  //     price: formData.price,
  //     train_id: formData.train_id,
  //     user_id: formData.user_id
  //   }
  // }






  return (
    <Wrapper>
      {tickets.length > 0 ? (
        tickets.map((ticket) => (
          <Ticket key={ticket.id}>
            <Box>
              <h2>{"Ticket"}</h2>
              <h2>{"Price: "+ticket.price}</h2>
              <h2>{"Train: "+ticket.train.title}</h2>
              <h2>{"User: "+ticket.user.username}</h2>
              <Button onClick={() => handleDeleteTicket(ticket.id)}>
                Delete ticket
              </Button>
              <Button as={Link} to="/update">
          Update Ticket
        </Button>
              {/* <p>
                <em>Time to Complete: {ticket.minutes_to_complete} minutes</em>
                &nbsp;·&nbsp;
                <cite>By {ticket.user.username}</cite>
              </p> */}
              <ReactMarkdown>{ticket.description}</ReactMarkdown>
            </Box>
          </Ticket>
        ))
      ) : (
        <>
          <h2>No Tickets Found</h2>
          <Button as={Link} to="/new">
            Make a New Ticket
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

const Ticket = styled.article`
  margin-bottom: 24px;
`;

export default TicketList;
