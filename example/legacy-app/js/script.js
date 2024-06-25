document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('addUserForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        addUser();
    });
});

function addUser() {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'master-ajax.php', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                addUserToTable(response.user);
                document.getElementById('name').value = '';
                document.getElementById('email').value = '';
            } else {
                alert('Error: ' + response.message);
            }
        }
    };
    xhr.send('action=addUser&name=' + encodeURIComponent(name) + '&email=' + encodeURIComponent(email));
}

function addUserToTable(user) {
    var table = document.getElementById('userTable');
    var row = table.insertRow(-1);
    var cellId = row.insertCell(0);
    var cellName = row.insertCell(1);
    var cellEmail = row.insertCell(2);

    cellId.textContent = user.id;
    cellName.textContent = user.name;
    cellEmail.textContent = user.email;
}