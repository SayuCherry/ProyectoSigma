document.addEventListener('DOMContentLoaded', () => {
    const courses = document.querySelectorAll('.course');
    
    courses.forEach(course => {
        const courseId = course.getAttribute('data-course-id');
        
        fetch(`get_progress.php?course_id=${courseId}`)
            .then(response => response.json())
            .then(data => {
                const progressBar = course.querySelector('.progress');
                progressBar.style.width = `${data.percentage}%`;
                progressBar.textContent = `${data.percentage}%`;
            })
            .catch(error => console.error('Error:', error));
    });
});
