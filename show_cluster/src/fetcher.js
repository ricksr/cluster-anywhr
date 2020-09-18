const axios = require("axios");

const all_coords = async () => {
    const url = `https://24tflrq9y9.execute-api.us-east-1.amazonaws.com/prod/get-all-coordinates`
    let finalData;
    await axios.get(url)
    .then(resp => finalData=resp)
    .catch(err => finalData=err);
    return finalData;
    // console.log(resp);
};

// export default all_coords;
// 
module.export = all_coords;
// all_coords();