const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

let clients = [
  {
    id: 1,
    name: 'Anna Kendrick',
    phone: '+1-415-555-0192',
    ssn: '321-54-9876',
    email: 'anna.k@hollywood.com',
    dob: '1985-08-09'
  },
  {
    id: 2,
    name: 'Tom Cruise',
    creditCard: '4000056655665556',
    address: '123 Top Gun Ave, LA, CA',
    phone: '+1-213-555-0156'
  }
];

app.get('/client/:id', (req, res) => {
  const client = clients.find(c => c.id === parseInt(req.params.id));
  if (!client) return res.status(404).send({ error: 'Not found' });
  res.send(client);
});

app.post('/client', (req, res) => {
  const newId = clients.length + 1;
  const newClient = { id: newId, ...req.body };
  clients.push(newClient);
  res.status(201).send(newClient);
});

app.listen(4000, () => console.log('Client API running on port 4000'));