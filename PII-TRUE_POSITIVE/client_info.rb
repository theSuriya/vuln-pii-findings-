class ClientInfo
    def initialize
      @name = "Edward Franklin"
      @email = "edward.franklin@example.com"
      @phone = "777-888-9999"
      @address = "789 Pine Rd, Hilltown"
    end
  
    def display
      puts "Client: #{@name}, #{@email}, #{@phone}, #{@address}"
    end
  end
  
  client = ClientInfo.new
  client.display