package main

import "fmt"

type User struct {
    Name  string
    Email string
    Phone string
    SSN   string
}

func (u User) DisplayInfo() string {
    return fmt.Sprintf("Name: %s, Email: %s, Phone: %s, SSN: %s", u.Name, u.Email, u.Phone, u.SSN)
}

func AddUser(userList *[]User, name, email, phone, ssn string) {
    newUser := User{name, email, phone, ssn}
    *userList = append(*userList, newUser)
    fmt.Printf("Added user: %s\n", name)
}

func ListUsers(userList []User) {
    if len(userList) == 0 {
        fmt.Println("No users found.")
    } else {
        fmt.Println("\nUser List:")
        for _, user := range userList {
            fmt.Println(user.DisplayInfo())
        }
    }
}

func main() {
    var users []User
    AddUser(&users, "Frank Miller", "frank.miller@example.com", "777-888-9999", "567-89-0123")
    AddUser(&users, "Grace Taylor", "grace.taylor@example.com", "222-333-4444", "678-90-1234")
    ListUsers(users)
}