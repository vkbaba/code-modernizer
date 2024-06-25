<?php
require_once 'main.class.php';

$main = new Main();
$users = $main->getUsers();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legacy PHP App</title>
    <script src="js/script.js"></script>
</head>
<body>
    <h1>User List</h1>
    <table id="userTable">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
        </tr>
        <?php foreach ($users as $user): ?>
        <tr>
            <td><?php echo $user['id']; ?></td>
            <td><?php echo $user['name']; ?></td>
            <td><?php echo $user['email']; ?></td>
        </tr>
        <?php endforeach; ?>
    </table>

    <h2>Add New User</h2>
    <form id="addUserForm">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br>
        <button type="submit">Add User</button>
    </form>
</body>
</html>