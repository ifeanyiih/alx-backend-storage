-- Script creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
	BEGIN
		DECLARE sum_wscores FLOAT DEFAULT 0.00;
		DECLARE sum_weights FLOAT DEFAULT 0.00;
		CREATE VIEW weighted_scores AS SELECT c.user_id, c.score * p.weight AS weighted_score, p.weight
		FROM projects p INNER JOIN corrections c on p.id = c.project_id;

		SET sum_wscores = (SELECT SUM(weighted_score) FROM weighted_scores WHERE weighted_scores.user_id = user_id);
		SET sum_weights = (SELECT SUM(weight) FROM weighted_scores WHERE weighted_scores.user_id = user_id);

		UPDATE users SET average_score = sum_wscores/sum_weights WHERE id=user_id;

		DROP VIEW weighted_scores;
	END;
//
DELIMITER ;
