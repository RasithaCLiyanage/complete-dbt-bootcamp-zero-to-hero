import snowflake.connector
import os
import logging
import sys
import traceback
import yaml



def check_snowflake_connection():
    # get Snowflake connection parameters from ~/.dbt/profiles.yml
    # open ~/.dbt/profiles.yml and read the connection parameters
    conn = None

    with open(os.path.expanduser("~/.dbt/profiles-debug.yml"), 'r') as file:
        profiles = yaml.safe_load(file)
        # print(profiles.get('udemy_dbt_course', {}).get('outputs', {}).get('dev', {}))
        snowflake_profile = profiles.get('udemy_dbt_course', {}).get('outputs', {}).get('dev', {})
        if snowflake_profile:
            user = snowflake_profile.get('user')
            password = snowflake_profile.get('password')
            account = snowflake_profile.get('account')
            warehouse = snowflake_profile.get('warehouse')
            database = snowflake_profile.get('database')
            schema = snowflake_profile.get('schema')
        else:
            logging.error("Snowflake profile not found in ~/.dbt/profiles.yml")
            return


    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        conn.cursor().execute("SELECT CURRENT_VERSION()")
        logging.info("Snowflake connection successful.")
    except Exception as e:
        logging.error("Error connecting to Snowflake: %s", e)
        logging.debug("Traceback: %s", traceback.format_exc())
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    check_snowflake_connection()
    logging.info("Snowflake connection check completed.")
    sys.exit(0)