const fs = require('fs');

function saveInvoice(data) {
  const invoice = {
    customer: data.customer,
    email: data.email,
    address: data.address,
    card: data.card,
    amount: data.amount
  };

  fs.writeFileSync(`invoices/${data.customer}_invoice.json`, JSON.stringify(invoice, null, 2));
}

saveInvoice({
  customer: "Peter Parker",
  email: "peter.parker@dailybugle.net",
  address: "20 Ingram Street, Queens, NY",
  card: "378282246310005",
  amount: 129.99
});