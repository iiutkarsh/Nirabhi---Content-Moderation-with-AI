document.addEventListener("DOMContentLoaded", function () {
    let homeBtn = document.getElementById("home");
    let reportBtn = document.getElementById("report");
    let loginBtn = document.getElementById("login");
    let registerBtn = document.getElementById("register");
    let textAnalysisBtn = document.getElementById("analysisBtn");


   
    homeBtn.addEventListener("click", function () {
        showSection("homepage");
    });

    reportBtn.addEventListener("click", function () {
        showSection("reportpage");
    });

    loginBtn.addEventListener("click", function () {
        showSection("loginpage");
    });
    registerBtn.addEventListener("click", function () {
        showSection("registerpage");
    });
    textAnalysisBtn.addEventListener("click", function () {
        showSection("analysispage");
    });

    function showSection(sectionId) {
        document.querySelectorAll('.section').forEach(section => {
            section.style.display = 'none';
        });

        document.getElementById(sectionId).style.display = 'block';
    }
});