import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { Box, Button } from "../styles";

const TrainList = () => {
    const [trains, setTrains] = useState([]);

    useEffect(()=>{
        fetch("/trains").then((r)=>{
            if (r.ok){
                r.json().then((trains)=>setTrains(trains));
            }
        })
    },[])

    function handleDeleteTrain(id) {
        fetch(`/trains/${id}`, {
            method: "DELETE",
        }).then((r) => {
            if (r.ok) {
                setTrains((trains) =>
                trains.filter((train) => train.id !== id)
                );
            }
        });
    }

    return (
        <Wrapper>
            {trains.length > 0 ? (
                trains.map((train) => (
                    <Train key={train.id}>
                        <Box>
                            <h2>{"Train"}</h2>
                            <h2>{"Title: "+train.title}</h2>
                            <h2>{train.description}</h2>
                            <img src={train.image_url}/>
                            <div>
                            <Button onClick={() => handleDeleteTrain(train.id)}>
                                Delete train
                            </Button>
                            </div>
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

export default TrainList