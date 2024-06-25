<?php
class Main {
    private $users = [
        ['id' => 1, 'name' => 'John Doe', 'email' => 'john@example.com'],
        ['id' => 2, 'name' => 'Jane Smith', 'email' => 'jane@example.com'],
        ['id' => 3, 'name' => 'Bob Johnson', 'email' => 'bob@example.com'],
    ];

    public function getUsers() {
        return $this->users;
    }

    public function addUser($name, $email) {
        $newId = count($this->users) + 1;
        $newUser = ['id' => $newId, 'name' => $name, 'email' => $email];
        $this->users[] = $newUser;
        return ['success' => true, 'user' => $newUser];
    }
}