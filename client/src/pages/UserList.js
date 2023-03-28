import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { Box, Button } from "../styles";
function UserList() {
    const [users, setUsers] = useState([])
    useEffect(()=>{
        fetch("/users").then((r)=>{
            if (r.ok){
                r.json().then((users)=>setUsers(users));
            }
        })
        },[])
    return (
        <Wrapper>
            {users.length > 0 ? (
                users.map((user) => (
                <User key={user.id}>
                    <Box>
                    <h2>{"User"}</h2>
                    <h2>{"Username: "+user.username}</h2>
                    <h2>{"Image: "+user.image_url}</h2>
                    <h2>{"Bio: "+user.bio}</h2>
                    {/* <h2>{"User Train: "+user.train}</h2> */}
                    {/* <h2>{"User: "+user.ticket}</h2>
                    <ReactMarkdown>{user.description}</ReactMarkdown> */}
                    </Box>
                </User>
                ))
            ) : (
                <>
                <h2>No Users Found</h2>
                <Button as={Link} to="/">
                    Go home
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
const User = styled.article`
    margin-bottom: 24px;
`;
export default UserList;