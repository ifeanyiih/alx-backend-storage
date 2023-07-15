-- Script creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE num INT DEFAULT 0;
	DECLARE sums INT DEFAULT 0;
	SET num = (SELECT COUNT(score) FROM corrections WHERE corrections.user_id=user_id);
	SET sums = (SELECT SUM(score) FROM corrections WHERE corrections.user_id=user_id);
	UPDATE users SET average_score = sums/num WHERE id=user_id;
END
//
DELIMITER ;
