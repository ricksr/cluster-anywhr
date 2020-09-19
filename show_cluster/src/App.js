import React, { useEffect, useState, useCallback } from "react";
import { HexGrid, Layout, Hexagon, Text } from "react-hexgrid";
import { Input, Button, InputGroup } from "reactstrap";
import { isEmpty } from "lodash-es";

import anywhr from "./anywhr.png";
import styles from "./Contain.css";
import "./Hex.css";
const axios = require("axios");

const url = "https://24tflrq9y9.execute-api.us-east-1.amazonaws.com/prod/";

const App = () => {
  const [hexName, setHexName] = useState();
  const [newHex, setNewHex] = useState();
  const [srcHex, setSrcHex] = useState();
  const [side, setSide] = useState();
  const [Hexagons, setHexagons] = useState([]);
  const [vals, setVals] = useState([]);
  const [search, setSearch] = useState(false);
  const [removeHexName, setRemoveHexName] = useState();

  const handleHexName = (e) => {
    setHexName(e.target.value);
  };
  const handleNewHex = (e) => {
    setNewHex(e.target.value);
  };
  const handleSrcHex = (e) => {
    setSrcHex(e.target.value);
  };
  const handleSide = (e) => {
    setSide(e.target.value);
  };
  const handleRemoveHex = (e) => {
    setRemoveHexName(e.target.value);
  };

  const loadHexagons = useCallback(() => {
    axios.get(`${url}get-all-coordinates`).then((response) => {
      // console.log(response);
      setHexagons(response.data);
    });
  }, []);

  useEffect(() => {
    loadHexagons();
  }, [loadHexagons]);

  const handleSearchSubmit = async () => {
    if (!isEmpty(hexName)) {
      await axios.get(`${url}get-hex-by-name?name=${hexName}`)
        .then((response) => {
          setVals(response);
          setSearch(true);
          // console.log(response)
          !isEmpty(response.data) &&
            response.data.hexagons.map((i) => {
              vals.push(i);
              setVals(vals);
            });
          alert("Please see here - " + `${url}get-hex-by-name?name=${hexName}`);
          // console.log(vals)
          setVals();
          setHexName('');
        });
    } else {
      alert('Enter data');
    }
  };

  const handleAddSubmit = async () => {
    if (!isEmpty(srcHex) && !isEmpty(newHex) && !isEmpty(side)) {
      await axios.post(`${url}add-hex?src=${srcHex}&new=${newHex}&loc=${side}`)
        .then(() => {
          loadHexagons();
          setSrcHex('');
          setSide('');
          setNewHex('');
        })
        .catch((err) => {
          alert(err);
        });
    }
    else {
      alert('Enter all data');
    }
  };

  const handleRemoveSubmit = async () => {
    if (!isEmpty(removeHexName)) {
      await axios.post(`${url}remove-hex?src=${removeHexName}`)
        .then((response) => {
          if (response.data.err) {
            alert("Not possible to remove");
          } else {
            alert("success");
          }
          setRemoveHexName('');
          loadHexagons();
        });
    } else {
      alert('Enter Hex Name to remove');
    }
  };

  return (
    <div className={styles.containerAll}>
      <div className={styles.barTop}>
        <img src={anywhr} alt="anywhr" />
      </div>
      <div style={{ margin: "auto", width: "1000px" }}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              justifyContent: "space-evenly",
              display: "flex",
            }}
          >
            <div
              style={{
                display: "flex",
              }}
            >
              <Input
                style={{ width: "200px", marginRight: "20px" }}
                addon
                type="text"
                placeholder="Search By Name"
                name="Search Hex"
                value={hexName}
                onChange={handleHexName}
              />
              <Button color="primary" onClick={handleSearchSubmit}>
                Find whr?
              </Button>
            </div>
            <br />
            <div
              style={{
                display: "flex",
              }}
            >
              <Input
                style={{ width: "200px", marginRight: "20px" }}
                className={styles.inputBox}
                type="text"
                placeholder="Hex Name to Remove"
                name="New Hex Name"
                value={removeHexName}
                onChange={handleRemoveHex}
              />
              <Button color="primary" onClick={handleRemoveSubmit}>
                Remove Hexagon - Hotspot
              </Button>
            </div>
          </div>
          <br />
          <div style={{ margin: "auto" }}>
            <div style={{ display: "flex", margin: "auto" }}>
              <Input
                style={{ width: "200px", marginRight: "20px" }}
                className={styles.inputBox}
                type="text"
                placeholder="Add a Hex"
                name="New Hex Name"
                value={newHex}
                onChange={handleNewHex}
              />
              <Input
                style={{ width: "200px", marginRight: "20px" }}
                className={styles.inputBox}
                type="text"
                placeholder="New Hex Source"
                name="Name src"
                value={srcHex}
                onChange={handleSrcHex}
              />
              <Input
                style={{ width: "220px", marginRight: "30px" }}
                className={styles.inputBox}
                type="text"
                placeholder="which side of Source - 0--5"
                name="Search Hex"
                value={side}
                onChange={handleSide}
              />
              <Button color="primary" onClick={handleAddSubmit}>
                Add Hexagon - Hotspot
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="Hex">
        <HexGrid width={1000} height={400} viewBox="-70 -70 150 100">
          <Layout size={{ x: 4, y: 4 }}>
            {!isEmpty(Hexagons) &&
              Hexagons.body.map((i) => (
                <Hexagon q={i.q} r={i.r} s={i.s}>
                  <Text>{i.hex_name.name}</Text>
                </Hexagon>
              ))}
          </Layout>
        </HexGrid>
      </div>
    </div>
  );
};

export default App;