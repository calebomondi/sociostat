//function to retrieve data from localstorage
window.onload = function() {
    // Retrieve data from localStorage
    var localStorageData = localStorage.getItem('user') || 'abc@example.com';
    console.log('LOADEDED > ',localStorageData);

    // Send data to Django view using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/processLS/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            console.log('Data sent successfully!');
        } else {
            console.log('Error in sending data: ', xhr.status, xhr.statusText);
        }
    };

    xhr.send(JSON.stringify({ 'localStorageData': localStorageData }));
};
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
        }
    }
    }
    return cookieValue;
};
document.addEventListener('DOMContentLoaded', () => {
    // Get the form element
    const form = document.getElementById('postFormSet');
    // Add an event listener to the form's submit event
    form.addEventListener('submit', function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();
        // Get the form data
        var email = document.getElementById('id_email').value;
        // Convert the FormData object to a JSON string
        const user = {}
        user.email = email;
        // Save the form data to localStorage
        localStorage.clear();
        localStorage.setItem('user', JSON.stringify(user))
        // Allow the form submission to continue
        form.submit();
    });
});

