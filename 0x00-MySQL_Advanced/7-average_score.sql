-- Script creates a stored procedure ComputeAverageScoreForUser that computes and stores the average score for a student 
DELIMITER &&
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
	BEGIN
		DECLARE average FLOAT DEFAULT NULL;
		SET average = (SELECT AVG(score) FROM corrections WHERE user_id=user_id);
		UPDATE users SET average_score = average WHERE id=user_id;
	END;
&&

DELIMITER ;
