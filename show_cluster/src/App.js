import React, {useEffect, useState, useCallback} from 'react';
import { HexGrid, Layout, Hexagon, GridGenerator, Text } from 'react-hexgrid';
import {Input, Button, InputGroup} from 'reactstrap';
import { isEmpty, constant } from 'lodash-es';

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
  const [vals, setVals] = useState({});

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

    axios.get(`${url}get-hex-by-name?name=${hexName}`).then((response) => {
      setVals(response);
      alert(vals);
    });
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
        <HexGrid width={1000} height={400} viewBox="-70 -70 150 100">
          <Layout size={{ x: 4, y: 4 }}>
            { 
            !isEmpty(dogs) && dogs.body.map(i => (
              <Hexagon q={i.q} r={i.r} s={i.s} >
                <Text>{i.hex_name.name}</Text>
              </Hexagon>
            ))
          }
          </Layout>
        </HexGrid>
      </div>
     
    </div>
  );
}

export default App;
