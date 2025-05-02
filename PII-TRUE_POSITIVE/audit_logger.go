package main

import (
    "encoding/json"
    "fmt"
    "os"
)

type Record struct {
    UserID    string `json:"user_id"`
    Email     string `json:"email"`
    IPAddress string `json:"ip_address"`
    SSN       string `json:"ssn"`
}

func logEvent(record Record) {
    file, _ := os.Create("audit_log.json")
    defer file.Close()
    json.NewEncoder(file).Encode(record)
}

func main() {
    r := Record{
        UserID:    "u001",
        Email:     "logan.wolverine@xmen.org",
        IPAddress: "192.168.0.15",
        SSN:       "321-45-9876",
    }
    logEvent(r)
    fmt.Println("Audit log created.")
}