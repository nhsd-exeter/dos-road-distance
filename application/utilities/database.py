import os
import json
import psycopg2
import psycopg2.extras
from utilities import secrets, logger, message, common

secret_store = os.environ.get("SECRET_STORE")
profile = os.environ.get("PROFILE")

def connect_to_database(env, event, start):
    db = DB()
    logger.log_for_audit("Setting DB connection details")
    if not db.db_set_connection_details(env, event, start):
        logger.log_for_error("Error DB Parameter(s) not found in secrets store.")
        message.send_failure_slack_message(event, start)
        raise ValueError("DB Parameter(s) not found in secrets store")
    return db.db_connect(event, start)


def does_record_exist(db, row_dict, table_name):
    """
    Checks to see if record already exists in db table with the id
    """
    record_exists = False
    full_table_name = "pathwaysdos." + table_name
    try:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = """select * from """ + full_table_name + """ where id=%s"""
            cursor.execute(select_query, (row_dict["id"],))
            if cursor.rowcount != 0:
                record_exists = True
    except (Exception, psycopg2.Error) as e:
        logger.log_for_error(
            "Select from table {0} by id failed - {1} => {2}".format(full_table_name, row_dict["id"], str(e)),
        )
        raise e
    return record_exists


def execute_db_query(db_connection, query, data, line, values, summary_count_dict):
    cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(query, data)
        db_connection.commit()
        common.increment_summary_count(summary_count_dict, values)
        logger.log_for_audit(
            "action: Process row | operation: {0} | id: {1} | description: {2} | line number: {3}".format(
                values["action"], values["id"], values["name"], line
            )
        )
    except Exception as e:
        logger.log_for_error("Line {} in transaction failed. Rolling back".format(line))
        logger.log_for_error("Error: {}".format(e))
        db_connection.rollback()
    finally:
        cursor.close()


class DB:
    def __init__(self) -> None:
        print("Initialising DB Class")
        self.db_host = ""
        self.db_name = ""
        self.db_user = ""
        self.db_password = ""

    def db_set_connection_details(self, env, event, start):
        secret_list = secrets.SECRETS().get_secret_value(secret_store, event, start)
        formatted_secrets = json.loads(secret_list, strict=False)
        db_host_key = "DB_HOST"
        db_user_key = "DB_USER"
        db_password_key = "DB_USER_PASSWORD"
        if env == "performance":
            db_host_key = "DB_PERFORMANCE_HOST"
            db_password_key = "DB_PERFORMANCE_PASSWORD"
        elif env == "regression":
            db_host_key = "DB_REGRESSION_HOST"

        if formatted_secrets is None:
            logger.log_for_diagnostics("Secrets not set")
        elif db_host_key not in formatted_secrets:
            logger.log_for_diagnostics("No DB_HOST secret var set")
        elif db_user_key not in formatted_secrets:
            logger.log_for_diagnostics("No DB_USER secret var set")
        elif db_password_key not in formatted_secrets:
            logger.log_for_diagnostics("No DB_PASSWORD secret set")
        else:
            logger.log_for_diagnostics("Host: {}".format(self.db_host))
            logger.log_for_diagnostics("User: {}".format(self.db_user))
            logger.log_for_diagnostics("DB_PASSWORD secret set")
            if profile != "prod" and env != "performance":
                self.db_name = "pathwaysdos_{}".format(env)
            else:
                self.db_name = "pathwaysdos"
            logger.log_for_diagnostics("DB Name: {}".format(self.db_name))
            return True
        return False

    def db_connect(self, event, start):
        try:
            return psycopg2.connect(
                host=self.db_host, dbname=self.db_name, user=self.db_user, password=self.db_password
            )
        except Exception:
            logger.log_for_error("Connection parameters not set correctly")
            message.send_failure_slack_message(event, start)
            raise psycopg2.InterfaceError()
