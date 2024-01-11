document.getElementById('currentYear').textContent = new Date().getFullYear();

{% if submit_timeout %}
    animateProgressBar({{ submit_timeout }});
    submitAfterTimeout({{ submit_timeout }});
{% endif %}

function submitAfterTimeout(timeoutInSeconds) {
    setTimeout(function() {
        var form = document.forms[0];

        if (form) {
            form.submit();
        } else {
            console.error('Form not found.');
        }
    }, timeoutInSeconds * 1000);
}

function animateProgressBar(durationInSeconds) {
    var progressBar = document.getElementById('loadingProgress');
    var progress = 0;
    var interval = 20; // Update every 20 milliseconds
    var increment = (100 / (durationInSeconds * 1000 / interval));

    var animationInterval = setInterval(function() {
        progress += increment;
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);

        if (progress >= 100) {
            clearInterval(animationInterval);
        }
    }, interval);
}