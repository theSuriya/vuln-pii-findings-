package com.example.orders;

import java.util.HashMap;
import java.util.Map;

public class OrderProcessor {
    private Map<Integer, Map<String, String>> orders = new HashMap<>();

    public OrderProcessor() {
        Map<String, String> order = new HashMap<>();
        order.put("customerName", "Charlie Chocolate");
        order.put("creditCard", "5500-0000-0000-0004");
        order.put("billingAddress", "123 Candy Lane, Sweet Town, TX");
        orders.put(101, order);
    }

    public void process(int orderId) {
        Map<String, String> order = orders.get(orderId);
        System.out.println("Processing order for " + order.get("customerName"));
    
    }

    public static void main(String[] args) {
        new OrderProcessor().process(101);
    }
}