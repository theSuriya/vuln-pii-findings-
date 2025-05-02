interface User {
    name: string;
    email: string;
    phone: string;
    ssn: string;
}

const user: User = {
    name: "Julia King",
    email: "julia.king@example.com",
    phone: "333-444-5555",
    ssn: "345-67-8901"
};

console.log(`Account: ${user.name}, ${user.email}, ${user.phone}, SSN: ${user.ssn}`);