-- Script creates a view need_meeting that lists all students that have a score under 80(strict) and no last_meeting or more than 1 month
CREATE OR REPLACE VIEW need_meeting AS SELECT name FROM students s WHERE (s.score < 80) AND ((s.last_meeting IS NULL) OR (TIMESTAMPDIFF(MONTH, s.last_meeting, CURDATE()) > 1)); 
