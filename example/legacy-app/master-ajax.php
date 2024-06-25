<?php
require_once 'main.class.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'addUser') {
    $main = new Main();
    $name = isset($_POST['name']) ? $_POST['name'] : '';
    $email = isset($_POST['email']) ? $_POST['email'] : '';
    
    if ($name && $email) {
        $result = $main->addUser($name, $email);
        echo json_encode($result);
    } else {
        echo json_encode(['success' => false, 'message' => 'Invalid user data']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request']);
}