-- Script creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
	BEGIN
		DECLARE u_id INT;
		DECLARE ssum FLOAT;
		DECLARE wsum FLOAT;
		DECLARE done INT DEFAULT FALSE;
		DECLARE cur1 CURSOR FOR SELECT w.user_id, w.weighted_score_sum, w.weight_sum
			FROM (
				SELECT DISTINCT c.user_id, SUM(c.score * p.weight)
					AS weighted_score_sum, SUM(p.weight) AS weight_sum
					FROM projects p INNER JOIN corrections c ON p.id = c.project_id GROUP BY c.user_id
			) AS w;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

		OPEN cur1;

		read_loop: LOOP
			FETCH cur1 INTO u_id, ssum, wsum;
			UPDATE users SET average_score = ssum / wsum WHERE id=u_id;

			IF done THEN
				LEAVE read_loop;
			END IF;
		END LOOP;

		CLOSE cur1;
	END;
//
DELIMITER ;
