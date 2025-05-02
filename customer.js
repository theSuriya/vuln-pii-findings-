// Mock API client for customer data
class CustomerAPI {
    constructor() {
      this.customers = [
        { id: 1, name: 'Bob Builder', phone: '+44 7700 900890', ssn: '223-45-6789' },
        { id: 2, name: 'Eve Online', phone: '+1-303-555-0123', email: 'eve.online@gameworld.com' }
      ];
    }
  
    getCustomer(id) {
      return this.customers.find(c => c.id === id);
    }
  }
  
  const api = new CustomerAPI();
  console.log(api.getCustomer(2));