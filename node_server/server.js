const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();

const DATA_FILE = 'data.json';

// Enable CORS for all origins
app.use(cors());
app.use(express.json());

// Function to safely read and parse JSON file
function readDataFile() {
  try {
    const fileContent = fs.readFileSync(DATA_FILE, 'utf8');
    return fileContent ? JSON.parse(fileContent) : [];
  } catch (error) {
    // If the file doesn't exist or has invalid JSON, initialize it as an empty array
    return [];
  }
}

// Endpoint to receive and store data
app.post('/store', (req, res) => {
  const newData = req.body;

  if (!Array.isArray(newData)) {
    return res.status(400).json({ error: 'Invalid data format. Expected an array.' });
  }

  try {
    // Safely read existing data from the file
    const currentData = readDataFile();

    // Merge new data into the existing array
    const updatedData = [...currentData, ...newData];

    // Write updated data to the file
    fs.writeFileSync(DATA_FILE, JSON.stringify(updatedData, null, 2));

    res.status(200).json({ message: 'Data stored successfully' });
  } catch (err) {
    res.status(500).json({ error: 'Failed to store data', details: err.message });
  }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
