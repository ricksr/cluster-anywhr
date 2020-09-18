import React, {useEffect, useState, useCallback} from 'react';
import { HexGrid, Layout, Hexagon, GridGenerator, Text } from 'react-hexgrid';
import {Input, Button, InputGroup} from 'reactstrap';


import anywhr from './anywhr.png';
import styles from './Contain.css';
import './Hex.css'
import dat from './fetcher';
const axios = require('axios');


const url = "https://24tflrq9y9.execute-api.us-east-1.amazonaws.com/prod/";
const App = () => {
  const [hexName, setHexName] = useState();
  const [newHex, setNewHex] = useState();
  const [dogs, setDogs] = useState([]);

  const handleHexName = (e) => {setHexName(e.target.value);}
  const handleNewHex = (e) => {setNewHex(e.target.value);}

  const loadDogs = useCallback(() => {
    axios.get(`${url}get-all-coordinates`).then((response) => {
      console.log(response);
      setDogs(response.data);
    });
  }, []);

  useEffect(() => {
    console.log(module);
    loadDogs();
  }, [loadDogs]);


  const handleSearchSubmit = (e) => {
    console.log(hexName);
    console.log(dogs);
    dogs.body.map(i => console.log(i.q, i.r, i.s))
  }

  const handleAddSubmit = (e) => {
    console.log(e);
    console.log(newHex);
  }
  
  

  return (
    <div className={styles.containerAll}>
      <div className={styles.barTop}>
        <img src={anywhr} alt="anywhr" />
      </div>
      <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-around" }}>
        <div>
        <InputGroup size="sm">
          <Input
            addon
            type="text"
            placeholder="Search By Name"
            name="Search Hex"
            value={hexName}
            onChange={handleHexName}
          />
          </InputGroup>
          <br />
          <InputGroup><Button color="primary" onClick={handleSearchSubmit}>Find whr?</Button></InputGroup>
          
          </div>
          <br />
          <div>
          <InputGroup>
          <Input
            className={styles.inputBox}
            type="text"
            placeholder="Add a Hex"
            name="Search Hex"
            value={newHex}
            onChange={handleNewHex}
          />
          </InputGroup>
          <br />
          <InputGroup><Button color="primary" onClick={handleAddSubmit}>Add Hexagon - Hotspot</Button></InputGroup>
        </div>
      </div>

      <div className="Hex">
      
              <div>{ dogs.body.map(i => (
                
                 <h1>{i.q}</h1>
               ))
            }</div>
        <HexGrid width={1200} height={1000}>
          <Layout size={{ x: 100, y: 100 }}>
            
            <Hexagon q={0} r={-1} s={1} fill="pat-2" />
            <Hexagon q={0} r={1} s={-1} />
            <Hexagon q={1} r={-1} s={0}>
              <Text>1, -1, 0</Text>
            </Hexagon>
            <Hexagon q={1} r={0} s={-1}>
              <Text>1, 0, -1</Text>
            </Hexagon>
          </Layout>
        </HexGrid>
      </div>
     
    </div>
  );
}

export default App;
