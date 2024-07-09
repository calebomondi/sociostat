//Handles Message Visibility
function showHidden() {
    var hidden = document.getElementById('message');
    hidden.style.visibility = 'visible';
}

//AJAX
$(document).ready(function () {
    //post All
    $('#postFormAll').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postAll,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormAll')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post All Carousel
    $('#postFormCaroAll').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postAllCaro,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormCaroAll')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post FB
    $('#postFormFb').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postFb,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormFb')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post FB Carousel
    $('#postFormCaroFb').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postFbCaro,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormCaroFb')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post FB Text
    $('#postFormTxt').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postFbText,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormTxt')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post IG
    $('#postFormIg').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postIg,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormIg')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post IG Story
    $('#postFormStory').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postIgStory,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormStory')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post IG Carousel
    $('#postFormCaroIg').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postIgCaro,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormCaroIg')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //setup
    $('#postFormSet').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: setupUrl,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormSet')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Sumbit.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
});

//Which Site Is ACtive
function fbDash(id) {
    var fb = document.getElementById('fbSite');
    var ig = document.getElementById('igSite');
    var set = document.getElementById('setSite');
    

    if(id == 0) {
        //FB
        ig.style.borderLeft = 'none';
        set.style.borderLeft = 'none';
        
        fb.style.borderLeft = '3px solid var(--white)';
    } else if (id == 1){
        //IG
        ig.style.borderLeft = '3px solid var(--white)';
        fb.style.borderLeft = 'none';
        set.style.borderLeft = 'none';
        
    } else if (id == 2){
        //SET
        set.style.borderLeft = '3px solid var(--white)';
        fb.style.borderLeft = 'none';
        ig.style.borderLeft = 'none';
        
    }else {
        fb.style.borderLeft = 'none';
        ig.style.borderLeft = 'none';
        set.style.borderLeft = 'none';
        
    }
}
document.getElementById('fbDash').addEventListener('click', () => {fbDash(0)});
document.getElementById('igDash').addEventListener('click', () => {fbDash(1)});
document.getElementById('setDash').addEventListener('click', () => {fbDash(2)});


function getPath() {
    var currentPath = window.location.pathname;
    var pathSegments = currentPath.split('/');
    if (pathSegments[1] == 'facebook')
        fbDash(0);
    else if(pathSegments[1] == 'instagram')
        fbDash(1);
    else if(pathSegments[1] == 'setup')
        fbDash(2);
    else
        fbDash(4)

    var dashB = document.getElementById('dashB');
    var viewB = document.getElementById('viewB');
    var trendB = document.getElementById('trendB');
    var compB = document.getElementById('compB');
    console.log(pathSegments[2])
    if (pathSegments[2] == 'dashboard'){
        viewB.style.borderBottom = 'none';
        trendB.style.borderBottom = 'none';
        compB.style.borderBottom = 'none';
    }
    else if(pathSegments[2] == 'views') {
        dashB.style.borderBottom = 'none';
        
        trendB.style.borderBottom = 'none';
        compB.style.borderBottom = 'none';
    }
    
    else if(pathSegments[2] == 'trends') {
        dashB.style.borderBottom = 'none';
        viewB.style.borderBottom = 'none';
        
        compB.style.borderBottom = 'none';
        if (pathSegments[1] == 'facebook')
            loadgraphFb();
        if(pathSegments[1] == 'instagram')
            loadgraphIg();
        resizeCanvas();
    }
    else if(pathSegments[2] == 'comparison') {
        dashB.style.borderBottom = 'none';
        viewB.style.borderBottom = 'none';
        trendB.style.borderBottom = 'none';
        loadgraphComp();
    }
    
}
//onload
getPath()
//on path change
window.addEventListener('popstate', getPath);

//charts
function loadgraphIg() {
    console.log('AM IN LINE FUNC IG!');
    fetch('/instagram/trends/process')
            .then(response => response.json())
            .then(data => {
                // Assuming the response data is an array of chart data objects
                if (data.length > 0) {
                    createChart('myChart', data[0]); // First dataset
                    createChart('myChart2', data[1]); // Second dataset
                }
            })
            .catch(error => console.error('Error fetching chart data:', error));
}
function loadgraphFb() {
    console.log('AM IN LINE FUNC FB!');
    fetch('/facebook/trends/process')
            .then(response => response.json())
            .then(data => {
                // Assuming the response data is an array of chart data objects
                if (data.length > 0) {
                    createChart('myChart3', data[0]); // First dataset
                    createChart('myChart4', data[1]); // Second dataset
                }
            })
            .catch(error => console.error('Error fetching chart data:', error));
}
function loadgraphComp() {
    console.log('AM IN LINE COMP!');
    fetch('/all/trends/process')
            .then(response => response.json())
            .then(data => {
                // Assuming the response data is an array of chart data objects
                if (data.length > 0) {
                    createChart('myChart5', data[0]); // First dataset
                    createChart('myChart6', data[1]); // Second dataset
                }
            })
            .catch(error => console.error('Error fetching chart data:', error));
}

const canvas = document.getElementById('myChart');
const canvas2 = document.getElementById('myChart2');
const canvas3 = document.getElementById('myChart3');
const canvas4 = document.getElementById('myChart4');
const canvas5 = document.getElementById('myChart5');
const canvas6 = document.getElementById('myChart6');
const container = document.getElementById('lgCont');
function resizeCanvas() {
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    canvas2.width = container.clientWidth;
    canvas2.height = container.clientHeight;
    canvas3.width = container.clientWidth;
    canvas3.height = container.clientHeight;
    canvas4.width = container.clientWidth;
    canvas4.height = container.clientHeight;
    canvas5.width = container.clientWidth;
    canvas5.height = container.clientHeight;
    canvas6.width = container.clientWidth;
    canvas6.height = container.clientHeight;
}

function createChart(canvasId, data) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}