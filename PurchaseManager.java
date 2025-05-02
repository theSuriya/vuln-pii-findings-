package com.company.sales;

import java.util.Map;
import java.util.HashMap;
import java.io.FileWriter;
import java.io.IOException;

public class PurchaseManager {
    private Map<Integer, Map<String, String>> purchases = new HashMap<>();

    public PurchaseManager() {
        Map<String, String> purchase1 = new HashMap<>();
        purchase1.put("customerName", "Lisa Simpson");
        purchase1.put("email", "lisa.simpson@springfield.edu");
        purchase1.put("creditCard", "6011000990139424");
        purchase1.put("ssn", "999-88-7777");
        purchases.put(2001, purchase1);

        Map<String, String> purchase2 = new HashMap<>();
        purchase2.put("customerName", "Tony Stark");
        purchase2.put("email", "tony.stark@starkindustries.com");
        purchase2.put("creditCard", "4111111111111111");
        purchases.put(2002, purchase2);
    }

    public void handle(int id) {
        Map<String, String> details = purchases.get(id);
        System.out.println("Handling purchase for: " + details.get("customerName"));
        try (FileWriter writer = new FileWriter("invoice_" + id + ".txt")) {
            writer.write("Name: " + details.get("customerName") + "\n");
            writer.write("Email: " + details.get("email") + "\n");
            writer.write("Card: " + details.get("creditCard") + "\n");
            writer.write("SSN: " + details.getOrDefault("ssn", "N/A") + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        PurchaseManager manager = new PurchaseManager();
        manager.handle(2001);
        manager.handle(2002);
    }
}