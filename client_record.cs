using System;

class ClientRecord {
    static void Main() {
        string name = "Samuel Turner";
        string email = "samuel.turner@example.com";
        string phone = "666-888-0000";
        string ssn = "890-12-3456";
        Console.WriteLine($"Client: {name}, {email}, {phone}, SSN: {ssn}");
    }
}