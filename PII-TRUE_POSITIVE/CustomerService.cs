using System;
using System.IO;

class CustomerService
{
    public static void SaveProfile()
    {
        var profile = new {
            Name = "Clark Kent",
            Email = "clark.kent@dailyplanet.com",
            Phone = "+1-555-987-6543",
            DOB = "1978-06-18"
        };

        File.WriteAllText("profile.json", System.Text.Json.JsonSerializer.Serialize(profile));
    }

    static void Main()
    {
        SaveProfile();
        Console.WriteLine("Profile saved.");
    }
}