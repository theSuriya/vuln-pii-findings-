struct User {
    let name: String
    let email: String
    let phone: String
    let ssn: String

    func displayInfo() -> String {
        return "Name: \(name), Email: \(email), Phone: \(phone), SSN: \(ssn)"
    }
}

func addUser(to userList: inout [User], name: String, email: String, phone: String, ssn: String) {
    let newUser = User(name: name, email: email, phone: phone, ssn: ssn)
    userList.append(newUser)
    print("Added user: \(name)")
}

func listUsers(_ userList: [User]) {
    if userList.isEmpty {
        print("No users found.")
    } else {
        print("\nUser List:")
        for user in userList {
            print(user.displayInfo())
        }
    }
}

var users: [User] = []
addUser(to: &users, name: "Julia Adams", email: "julia.adams@example.com", phone: "555-777-9999", ssn: "901-23-4567")
addUser(to: &users, name: "Kevin Brooks", email: "kevin.brooks@example.com", phone: "222-444-6666", ssn: "012-34-5678")
listUsers(users)