import statistics
from typing import List

from records.abstract_migration_record import AbstractMigrationRecord


class RecordsNormalizer:

    @staticmethod
    def get_quartile(norm_value) -> int:
        """
        Get the quartile from normalized value
        :param norm_value:  Normalized value
        :param std_dev: Standard deviation
        :return:  The quartile
        """
        if norm_value < -2.698:
            return 1
        elif -2.698 <= norm_value <= -0.6745:
            return 2
        elif -0.6745 <= norm_value <= 0.6745:
            return 3
        elif 0.6745 < norm_value <= 2.698:
            return 4
        else:
            return 5

    @staticmethod
    def normalize_records_difficulty(records_list: List[AbstractMigrationRecord]) -> list:
        """
        Get the normalize difficulty
        :param records_list: List of records
        :return: List of records
        """
        scores_list = list(map(lambda x: x.get_difficulty_score(), records_list))

        if len(records_list) < 1:
            return []

        st_dev = statistics.stdev(scores_list)
        mean = statistics.mean(scores_list)

        ret_list = []
        norm_val_list = []

        # Normalize the scores
        for rec in records_list:
            norm_val = (rec.get_difficulty_score() - mean) / st_dev
            quartile = RecordsNormalizer.get_quartile(norm_val)
            norm_val_list.append(norm_val)

            rec.set_normalized_score(norm_val)
            rec.set_difficulty_segment(quartile)
            ret_list.append(rec)

        min_normalize = min(norm_val_list)
        shift = 1 - min_normalize

        # Shit all the scores to 1
        for rec in ret_list:
            norm_val = rec.get_normalized_score()
            rec.set_normalized_score(norm_val + shift)

        return ret_list
