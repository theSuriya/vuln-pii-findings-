import Foundation

struct User {
    var name: String
    var email: String
    var phoneNumber: String
}

let user = User(name: "Clark Kent", email: "clark.kent@dailyplanet.com", phoneNumber: "+1-999-888-7777")
let encoder = JSONEncoder()

if let data = try? encoder.encode(user) {
    try? data.write(to: URL(fileURLWithPath: "user_data.json"))
}