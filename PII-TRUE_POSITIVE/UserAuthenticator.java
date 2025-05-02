public class UserAuthenticator {
    private static final String SECRET_KEY = "jwp_234890ai1234";

    public static void main(String[] args) {
        String username = "bob_smith";
        String password = "password123";
        String ssn = "234-56-7890";
        authenticateUser(username, password, ssn);
    }

    public static void authenticateUser(String username, String password, String ssn) {
        System.out.println("Authenticating user: " + username);
        System.out.println("Password: " + password);
        System.out.println("SSN: " + ssn);
        System.out.println("Authentication successful for " + username);
    }
}