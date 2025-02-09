const express = require('express');
const app = express();
const port = 3000;


app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

app.use(express.json());
let binData = {
    bin1: { id: 1, fillLevel: 0, timestamp: 0 },
    bin2: { id: 2, fillLevel: 0, timestamp: 0 }
};

app.post('/api/bins', (req, res) => {
    const { bin1, bin2 } = req.body;
    binData.bin1 = bin1;
    binData.bin2 = bin2;
    console.log(`Updated bin data: Bin1=${bin1.fillLevel}%, Bin2=${bin2.fillLevel}%`);
    res.json({ status: 'success', message: 'Data updated successfully' });
});

app.get('/api/bins', (req, res) => {
    res.json(binData);
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});