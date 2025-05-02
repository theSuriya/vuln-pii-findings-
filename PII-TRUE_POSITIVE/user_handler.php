<?php
class User {
    public $name;
    public $email;
    public $phone;
    public $ssn;

    public function __construct($name, $email, $phone, $ssn) {
        $this->name = $name;
        $this->email = $email;
        $this->phone = $phone;
        $this->ssn = $ssn;
    }

    public function displayInfo() {
        return "Name: $this->name, Email: $this->email, Phone: $this->phone, SSN: $this->ssn";
    }
}

function addUser(&$userList, $name, $email, $phone, $ssn) {
    $newUser = new User($name, $email, $phone, $ssn);
    array_push($userList, $newUser);
    echo "Added user: $name\n";
}

function listUsers($userList) {
    if (empty($userList)) {
        echo "No users found.\n";
    } else {
        echo "\nUser List:\n";
        foreach ($userList as $user) {
            echo $user->displayInfo() . "\n";
        }
    }
}

$users = [];
addUser($users, "Hannah Clark", "hannah.clark@example.com", "111-222-3333", "789-01-2345");
addUser($users, "Ian Wright", "ian.wright@example.com", "444-555-6666", "890-12-3456");
listUsers($users);
?>