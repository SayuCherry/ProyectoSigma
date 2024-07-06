<?php
header('Content-Type: application/json');
$progressData = [
    1 => 70,
    2 => 45,
    3 => 90,
];

$courseId = $_GET['course_id'];
$percentage = isset($progressData[$courseId]) ? $progressData[$courseId] : 0;

echo json_encode(['percentage' => $percentage]);
?>
