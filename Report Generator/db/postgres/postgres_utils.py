from db.postgres.postgres_al import PostgresAL


class PostgresUtils:
    """
        Postgres utilities
    """

    def __init__(self):
        """
        Initialize the postgres utils class
        """
        self.__postgres = PostgresAL()