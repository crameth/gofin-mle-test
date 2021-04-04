from config import db_config

import mysql.connector
import mysql.connector.errors as error

import collections

SCHEMA = [
    "customer_id",
    "registration_date",
    "branch_code",
    "outstanding",
    "credit_limit",
    "bill",
    "total_cash_usage",
    "total_retail_usage",
    "remaining_bill",
    "payment_ratio",
    "overlimit_percentage",
    "payment_ratio_3month",
    "payment_ratio_6month",
    "delinquency_score",
    "years_since_card_issuing",
    "total_usage",
    "remaining_bill_per_number_of_cards",
    "remaining_bill_per_limit",
    "total_usage_per_limit",
    "total_3mo_usage_per_limit",
    "total_6mo_usage_per_limit",
    "utilization_3month",
    "utilization_6month",
    "default_flag",
]

class Database:

    connection = None
    cursor = None

    def __init__(self):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()

        print("connected to DB")

        try:
            self.create_table()
        except:
            pass

        try:
            self.ingest_data()
        except:
            pass
    
    def create_table(self):
        # create table
        sql = "CREATE TABLE IF NOT EXISTS customers ( customer_id int PRIMARY KEY, registration_date date, branch_code char, outstanding double, credit_limit double, bill double, total_cash_usage double, total_retail_usage double, remaining_bill double, payment_ratio double, overlimit_percentage double, payment_ratio_3month double, payment_ratio_6month double, delinquency_score double, years_since_card_issuing double, total_usage double, remaining_bill_per_number_of_cards double, remaining_bill_per_limit double, total_usage_per_limit double, total_3mo_usage_per_limit double, total_6mo_usage_per_limit double, utilization_3month double, utilization_6month double, default_flag int )"

        self.cursor.execute(sql)
        self.connection.commit()

        print("created table")

        return

    def ingest_data(self):
        print("uploading csv data")

        # ingest data
        sql = "LOAD DATA INFILE '/data/cs_assignment' IGNORE INTO TABLE gojek.customers FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES"
        
        self.cursor.execute(sql)
        self.connection.commit()

        print("uploaded csv data")

        return

    def delete_table(self):
        sql = "DROP TABLE customer"
        
        self.cursor.execute(sql)
        self.connection.commit()

    # task 1.1
    def customer_info(self, id: int):
        sql = f"SELECT * FROM customers WHERE customer_id = {id}"

        self._execute_sql(sql)
        
        query_result = self.cursor.fetchone()

        result = {}
        if len(query_result) > 0:
            for i, data in enumerate(query_result):
                result[SCHEMA[i]] = data

        return result

    # task 1.2
    def registration_info(self, start_date: str, end_date: str):
        sql = f"SELECT registration_date, COUNT(customer_id) AS registration_count FROM customers WHERE registration_date BETWEEN '{start_date}' AND '{end_date}' GROUP BY registration_date ORDER BY registration_count DESC, registration_date ASC"

        self._execute_sql(sql)

        result = []
        for row in self.cursor.fetchall():
            registration = {
                'registration_date': row[0],
                'registration_count': row[1],
            }
            result.append(registration)
        
        return result

    # task 2.1
    def branch_default_rate(self):
        sql = "SELECT branch_code, AVG(default_flag) as default_rate FROM customers GROUP BY branch_code ORDER BY default_rate DESC, branch_code ASC"

        self._execute_sql(sql)

        result = []
        for row in self.cursor.fetchall():
            branch = {
                'branch_code': row[0],
                'default_rate': row[1],
            }
            result.append(branch)
        
        return result

    # task 2.2
    def branch_credit_line(self):
        sql = "SELECT C.branch_code, (SUM(C.credit_limit) / T.total_credit_limit) AS credit_line_ratio FROM (SELECT SUM(credit_limit) AS total_credit_limit FROM customers) AS T, customers AS C GROUP BY branch_code ORDER BY credit_line_ratio DESC, branch_code ASC"

        self._execute_sql(sql)

        result = []
        for row in self.cursor.fetchall():
            branch = {
                'branch_code': row[0],
                'credit_line_ratio': row[1],
            }
            result.append(branch)
        
        return result

    # task 2.3
    def branch_top_default(self):
        sql = "SELECT O.branch_code, O.customer_id, O.outstanding FROM (SELECT branch_code, customer_id, outstanding, ROW_NUMBER() OVER (PARTITION BY branch_code ORDER BY outstanding DESC) AS rn FROM customers) AS O WHERE O.rn <= 5 ORDER BY O.branch_code ASC, O.outstanding DESC"

        self._execute_sql(sql)

        result = {}
        for i, row in enumerate(self.cursor.fetchall()):
            if i % 5 == 0:
                result[row[0]] = []

            result[row[0]].append(row[1])

        return result

    def _execute_sql(self, sql: str):
        """
        Executes a SQL query. This is a wrapper function used to handle exceptions.
        :param sql: The SQL string to be executed.
        :return: No return value if no error; raises a DatabaseError otherwise.
        """
        try:
            self.cursor.execute(sql)
        except (error.ProgrammingError, error.DatabaseError) as err:
            raise DatabaseError(err)

    def _execute_and_commit_sql(self, sql: str):
        """
        Executes and commits a SQL query. This is a wrapper function used to handle exceptions.
        :param sql: The SQL string to be executed and committed.
        :return: No return value if no error; raises a DatabaseError otherwise.
        """
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except (error.ProgrammingError, error.DatabaseError) as err:
            raise DatabaseError(err)
