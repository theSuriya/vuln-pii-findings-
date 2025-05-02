class User
    attr_accessor :name, :email, :phone, :ssn

    def initialize(name, email, phone, ssn)
      @name = name
      @email = email
      @phone = phone
      @ssn = ssn
    end

    def display_info
      "Name: #{@name}, Email: #{@email}, Phone: #{@phone}, SSN: #{@ssn}"
    end
end

def add_user(user_list, name, email, phone, ssn)
    new_user = User.new(name, email, phone, ssn)
    user_list << new_user
    puts "Added user: #{name}"
end

def list_users(user_list)
    if user_list.empty?
      puts "No users found."
    else
      puts "\nUser List:"
      user_list.each { |user| puts user.display_info }
    end
end

users = []
add_user(users, "David Lee", "david.lee@example.com", "555-123-4567", "345-67-8901")
add_user(users, "Emma Wilson", "emma.wilson@example.com", "444-555-6666", "456-78-9012")
list_users(users)