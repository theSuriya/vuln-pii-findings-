#include <fstream>
#include <string>

int main() {
    std::ofstream file("accounts.txt");
    file << "Name: Bruce Banner\n";
    file << "Email: bruce.banner@gamma.org\n";
    file << "Phone: +1-123-456-7890\n";
    file.close();
    return 0;
}