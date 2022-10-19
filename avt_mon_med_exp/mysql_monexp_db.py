"""
MIT License

Copyright (c) 2017 Packt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
May 2017
@author: Burkhard A. Meier
"""

"""
Changes and additions were made by:
@authors: A.V.T. Software (Sole Proprietorship Vita Tolstikova: Andrei Tostikov, Vita Tolstikova)
"""

import sys
# import traceback

# import MySQLdb as mysql

import mysql.connector as mysql

# from mysql.connector import errorcode

from . import mysql_monexp_db_config as db_conf


class MySQLMonExpDb():
    """
    Connecting and working with the <monexp_db> as the MySQL database
    """

    # class variable for project's database
    DB_NAME = 'monexp_db'


    # ------------------------------------------------------
    def show_mysql_error(self):
        """
        Show MySQLdb Errors via exc_info() method from sys Package
        """

        print('*** MySQLdb Error ***')
        # err_type, err_value, trace_info = sys.exc_info()
        err_type, err_value = sys.exc_info()
        print('*** Error Tуре: ', err_type)
        print('*** Error Value: ', err_value)


    # ------------------------------------------------------
    def show_mysql_warning(self):
        """
        Show MySQLdb Warnings via exc_info() method from sys Package
        """

        print('*** MySQLdb Warning ***')
        # warn_type, warn_value, trace_info = sys.exc_info()
        warn_type, warn_value = sys.exc_info()
        print('*** Warning Tуре: ', warn_type)
        print('*** Warning Value: ', warn_value)


    # ------------------------------------------------------
    def connect(self):
        """
        Connect to MySQL Server as 'user': '<your-user>'
        """

        try:
            # connect by unpacking dictionary credentials
            conn = mysql.connect(**db_conf.monexp_db_config)

            # create cursor
            cursor = conn.cursor()

            return conn, cursor

        except mysql.Error:
            
            self.show_mysql_error()
            



    # ------------------------------------------------------
    def close(self, cursor, conn):
        """
        Close connection to MySQL Server
        
        Arguments:
            cursor {MySQLdЬ.cursors.Cursor} -- cursor object for CRUD with <monexp_db> database
            conn {Connection} -- the connection object for MySQL server
        """

        try:
            # close cursor
            cursor.close()

            # close connection to MySQL
            conn.close()

        except mysql.Error:
            self.show_mysql_error()

    # ------------------------------------------------------
    def show_databases(self):
        """
        Lists the databases on the MySQL server host
        """

        try:
            # connect to MySQL
            conn, cursor = self.connect()

            # print results
            cursor.execute("SHOW DATABASES")
            print(cursor)
            print(cursor.fetchall())

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()



    # ------------------------------------------------------
    def create_db(self):
        """
        Create <monexp_db> database
        """

        try:
            # connect to MySQL
            conn, cursor = self.connect()

            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci".
                    format(MySQLMonExpDb.DB_NAME))

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def drop_db(self):
        """
        Drop <monexp_db> database
        """

        try:
            # connect to MySQL
            conn, cursor = self.connect()

            cursor.execute(
                "DROP DATABASE {}".format(MySQLMonExpDb.DB_NAME))

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()

    # ------------------------------------------------------
    def use_db(self, cursor):
        """
        Select <monexp_db> for use (Expects open connection)
        
        Arguments:
            cursor {MySQLdЬ.cursors.Cursor} -- cursor object for CRUD with <monexp_db> database
        """

        try:
            # select DB
            cursor.execute("USE {}".format(MySQLMonExpDb.DB_NAME))

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def create_db_tables(self):
        """
        Create <monexp_db> model (schema)
        """

        try:

            # connect to MySQL
            conn, cursor = self.connect()

            # use avtMonExpDB (MySQL database)
            self.use_db(cursor)

            # (1) create "keyword_type" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS keyword_type (                                   \
                  keyword_type_id INT NOT NULL AUTO_INCREMENT,                                          \
                  keyword_type VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,   \
                  PRIMARY KEY (keyword_type_id)                                                         \
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")

            # (2) create "keyword_category" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS keyword_category (                                   \
                  keyword_category_id INT NOT NULL AUTO_INCREMENT,                                          \
                  keyword_category VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,   \
                  PRIMARY KEY (keyword_category_id)                                                         \
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")


            # (3) create "keyword" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS keyword (                                    \
                    keyword_id INT NOT NULL AUTO_INCREMENT,                                         \
                    keyword VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  \
                    keyword_score INT NOT NULL,                                                     \
                    keyword_type_id INT NOT NULL,                                                   \
                    keyword_category_id INT NOT NULL,                                               \
                    PRIMARY KEY (keyword_id),                                                       \
                    FOREIGN KEY (keyword_type_id)                                                   \
                        REFERENCES keyword_type(keyword_type_id)                                    \
                        ON UPDATE NO ACTION                                                         \
                        ON DELETE CASCADE,                                                          \
                    FOREIGN KEY (keyword_category_id)                                               \
                        REFERENCES keyword_category(keyword_category_id)                            \
                        ON UPDATE NO ACTION                                                         \
                        ON DELETE CASCADE                                                           \
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")

            # (4) create "domain" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS domain (                                 \
                  domain_id INT NOT NULL AUTO_INCREMENT,                                        \
                  domain VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL, \
                  PRIMARY KEY (domain_id)                                                       \
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")

            # (5) create "domain_keyword_bridge" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS domain_keyword_bridge (  \
                    domain_id INT NOT NULL,                                     \
                    keyword_id INT NOT NULL,                                    \
                    PRIMARY KEY (domain_id, keyword_id),                        \
                    FOREIGN KEY (domain_id)                                     \
                        REFERENCES domain(domain_id)                            \
                        ON UPDATE NO ACTION                                     \
                        ON DELETE CASCADE,                                      \
                    FOREIGN KEY (keyword_id)                                    \
                        REFERENCES keyword(keyword_id)                          \
                        ON UPDATE NO ACTION                                     \
                        ON DELETE CASCADE                                       \
                ) ENGINE=InnoDB")

            # (6) create "tw_expert" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS tw_expert (                                        \
                    tw_expert_id INT NOT NULL AUTO_INCREMENT,                                             \
                    tw_id_str VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,      \
                    tw_screen_name VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL, \
                    tw_name VARCHAR(55) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,        \
                    tw_description VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,         \
                    tw_statuses_count INT NOT NULL,                                                       \
                    tw_statuses_count_score INT NOT NULL,                                                 \
                    tw_followers_count INT NOT NULL,                                                      \
                    tw_followers_count_score INT NOT NULL,                                                \
                    tw_friends_count INT NOT NULL,                                                        \
                    tw_friends_count_score INT NOT NULL,                                                  \
                    tw_location VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,            \
                    expert_location_lat FLOAT(12,6) DEFAULT NULL,                                                             \
                    expert_location_lng FLOAT(12,6) DEFAULT NULL,                                                             \
                    tw_lang VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,                 \
                    domain_keywords_score INT NOT NULL,                                                   \
                    expert_keywords_score INT NOT NULL,                                                   \
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                               \
                    PRIMARY KEY (tw_expert_id)                                                            \
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")

            # (7) create "tw_expert_domain_bridge" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS tw_expert_domain_bridge (\
                    tw_expert_id INT NOT NULL,                                  \
                    domain_id INT NOT NULL,                                     \
                    PRIMARY KEY (tw_expert_id, domain_id),                      \
                    FOREIGN KEY (tw_expert_id)                                  \
                        REFERENCES tw_expert(tw_expert_id)                      \
                        ON UPDATE NO ACTION                                     \
                        ON DELETE CASCADE,                                      \
                    FOREIGN KEY (domain_id)                                     \
                        REFERENCES domain(domain_id)                            \
                        ON UPDATE NO ACTION                                     \
                        ON DELETE CASCADE                                       \
                ) ENGINE=InnoDB")


            # (8) create "tw_expert_keywords" table inside "monexp_db"
            cursor.execute("CREATE TABLE IF NOT EXISTS tw_expert_keywords ( \
                    tw_expert_keywords_id INT NOT NULL AUTO_INCREMENT,      \
                    tw_expert_id INT NOT NULL,                              \
                    keyword_id INT NOT NULL,                                \
                    keyword_count INT NOT NULL,                             \
                    domain_id INT NOT NULL,                                 \
                    PRIMARY KEY (tw_expert_keywords_id),                    \
                    FOREIGN KEY (tw_expert_id)                              \
                        REFERENCES tw_expert(tw_expert_id)                  \
                        ON UPDATE NO ACTION                                 \
                        ON DELETE CASCADE,                                  \
                    FOREIGN KEY (keyword_id)                                \
                        REFERENCES keyword(keyword_id)                      \
                        ON UPDATE NO ACTION                                 \
                        ON DELETE CASCADE,                                  \
                    FOREIGN KEY (domain_id)                                 \
                        REFERENCES domain(domain_id)                        \
                        ON UPDATE NO ACTION                                 \
                        ON DELETE CASCADE                                   \
                ) ENGINE=InnoDB")

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def drop_db_tables(self):
        """
        Drop all tables in <monexp_db> database
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            #(1) drop "tw_expert_domain_bridge" table
            cursor.execute("DROP TABLE IF EXISTS tw_expert_domain_bridge")

            #(2) drop "tw_expert_keywords" table
            cursor.execute("DROP TABLE IF EXISTS tw_expert_keywords")

            #(3) drop "tw_expert" table
            cursor.execute("DROP TABLE IF EXISTS tw_expert")

            #(4) drop "domain_keyword_bridge" table
            cursor.execute("DROP TABLE IF EXISTS domain_keyword_bridge")

            #(5) drop "keyword" table
            cursor.execute("DROP TABLE IF EXISTS keyword")

            #(6) drop "keyword_type" table
            cursor.execute("DROP TABLE IF EXISTS keyword_type")

            #(7) drop "keyword_category" table
            cursor.execute("DROP TABLE IF EXISTS keyword_category")

            #(8) drop "domain" table
            cursor.execute("DROP TABLE IF EXISTS domain")

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()

    # ------------------------------------------------------
    def show_db_tables(self):
        """
        Show all tables from <monexp_db> database
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()


            # show tables from "monexp_db"
            cursor.execute("SHOW TABLES FROM {}".format(MySQLMonExpDb.DB_NAME))
            print(cursor.fetchall())

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def num_records_in_db_table(self, cursor, table_name):
        """
        Calculating number of records in <table_name> DB table
        
        Arguments:
            cursor {MySQLdЬ.cursors.Cursor} -- cursor object for CRUD with <monexp_db> database
            table_name {str} -- the name of DB table in <monexp_db> database

        Returns:
            [int] -- number of records in <table_name> DB table
        """

        try:
            # execute command
            cursor.execute("SELECT * FROM {}".format(table_name))

            all_records_t = cursor.fetchall()

            num_records = len(all_records_t)

            return num_records

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def insert_keyword_type_in_db(self, conn, cursor, keyword_type):
        """
        Insert new record in <keyword_type> DB table
        
        Arguments:
            conn {Connection} -- the connection object for MySQL server
            cursor {MySQLdЬ.cursors.Cursor} -- cursor object for CRUD with <monexp_db> database
            
            keyword_type {str} -- <keyword_type> data
        """

        try:
            # use <keyword_type> data as iteratable tuple
            cursor.execute("INSERT INTO keyword_type(keyword_type) VALUES(%s)", (keyword_type,))

            # commit transaction
            conn.commit()

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def insert_keyword_category_in_db(self, conn, cursor, keyword_category):
        """
        Insert new record in <keyword_category> DB table
        
        Arguments:
            conn {Connection} -- the connection object for MySQL server
            cursor {MySQLdЬ.cursors.Cursor} -- cursor object for CRUD with <monexp_db> database
            keyword_category {str} -- <keyword_category> data
        """

        try:
            # use <keyword_category> data as iteratable tuple
            cursor.execute("INSERT INTO keyword_category(keyword_category) VALUES(%s)", (keyword_category,))

            # commit transaction
            conn.commit()

        except mysql.Error:
            self.show_mysql_error()



    def insert_domain_in_db(self, domain):
        """
        Insert new record in <domain> DB table
        
        Arguments:
            domain {str} -- domain name

        Returns:
            [int] -- <domain_id> for new inserted record in <domain> DB table
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            # execute SELECT SQL command for retrieve <domain> from <domain> DB table
            cursor.execute("SELECT * FROM domain WHERE domain = %s LIMIT 1", (domain,))

            selected_record_t = cursor.fetchone()

            # If The current <domain> is not in the <monexp_db>
            # than insert it to <domain> table
            if selected_record_t is None:
                cursor.execute("INSERT INTO domain(domain) VALUES(%s)", (domain,))
                # commit transaction to <monexp_db>
                conn.commit()
                # Re-perform SELECT for get <domain_id> for new inserted record
                cursor.execute("SELECT * FROM domain WHERE domain = %s LIMIT 1", (domain,))
                domain_id = cursor.fetchone()[0]
            else:
                domain_id = selected_record_t[0]

            # close cursor and connection
            self.close(cursor, conn)

            return domain_id

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def insert_keyword_in_db(self, keyword, keyword_score, keyword_type, keyword_category, domain_id):
        """
        Insert new record in <keyword> DB table
        
        Arguments:
            keyword {str} -- keyword name as follows (depending on the <keyword_type> value)
                             1. tag(e.g. 'eGov'), 
                             2. screen_name(e.g. '@eGov'), 
                             3. hashtag (e.g. '#eGov'), 
                             4. phrase (only for keyword_type = 'domain', e.g. 'Open Data')
            keyword_score {int} -- <keyword_score> that is specified in domains_data.json 
                                   on a five-point scale (e.g. for "eGov":5 keyword_score = 5)
            keyword_type {str} -- 'domain' or 'expert'
            keyword_category {str} -- 'tag', 'screen_name', 'hashtag', or 'phrase'
            domain_id {int} -- <domain_id> from <domain> DB table

        Returns:
            [int] -- <keyword_id> for new inserted record in <keyword> DB table
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            # execute SELECT SQL command for retrieve <keyword> from <keyword> DB table
            cursor.execute("SELECT * FROM keyword WHERE keyword = %s LIMIT 1", (keyword,))

            selected_record_t = cursor.fetchone()

            # If the current <keyword> is not in the <keyword> DB table
            # than insert it to <keyword> DB table
            if selected_record_t is None:
                # execute SELECT SQL command for retrieve <keyword_type_id> from <keyword_type> DB table
                cursor.execute("SELECT * FROM keyword_type WHERE keyword_type = %s LIMIT 1", (keyword_type,))
                keyword_type_id = cursor.fetchone()[0]

                # execute SELECT SQL command for retrieve <keyword_category_id> from <keyword_category> DB table
                cursor.execute("SELECT * FROM keyword_category WHERE keyword_category = %s LIMIT 1", (keyword_category,))
                keyword_category_id = cursor.fetchone()[0]

                # execute INSERT SQL command for insert new record in <keyword> DB table
                cursor.execute("INSERT INTO keyword(keyword, keyword_score, keyword_type_id, keyword_category_id) \
                               VALUES(%s, %s, %s, %s)", (keyword, keyword_score, keyword_type_id, keyword_category_id))

                # commit transaction to <monexp_db>
                conn.commit()

                # Re-perform SELECT for get <keyword_id> for new inserted record
                cursor.execute("SELECT * FROM keyword WHERE keyword = %s LIMIT 1", (keyword,))
                keyword_id=cursor.fetchone()[0]

                # execute INSERT SQL command for insert domain_id and <keyword_id> in <domain_keyword_bridge> DB table
                cursor.execute("INSERT INTO domain_keyword_bridge(domain_id, keyword_id) VALUES(%s, %s)",
                               (domain_id, keyword_id))
                # commit transaction to <monexp_db>
                conn.commit()
            else:
                keyword_id = selected_record_t[0]

            # close cursor and connection
            self.close(cursor, conn)

            return keyword_id

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def find_tw_expert_in_db(self, tw_user_id_str):
        """
        Find record with <tw_user_id_str> in <tw_expert> DB table (expert data)
        
        Arguments:
            tw_user_id_str {str} -- The string representation of the unique identifier for Twitter User

        Returns:
            [int] -- One of the two following values as a result:
                     1. <tw_expert_id> (if record with <tw_user_id_str> was found in <tw_expert> DB table)
                     2. <tw_expert_id = -1> (if record with <tw_user_id_str> was not found in <tw_expert> DB table)
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            # execute SELECT SQL command for retrieve <tw_id_str> from <tw_expert> DB table
            cursor.execute("SELECT * FROM tw_expert WHERE tw_id_str = %s LIMIT 1", (tw_user_id_str,))

            selected_record_t = cursor.fetchone()

            # If The current <tw_id_str> is not in the <tw_expert> DB table
            # return tw_expert_id = -1
            if selected_record_t is None:
                tw_expert_id = -1
            else:
                tw_expert_id = selected_record_t[0]

            # close cursor and connection
            self.close(cursor, conn)

            return tw_expert_id

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def insert_tw_expert_in_db(self,
                               tw_user_id_str,
                               tw_user_screen_name,
                               tw_user_name,
                               tw_user_description,
                               tw_user_statuses_count,
                               tw_user_statuses_count_score,
                               tw_user_followers_count,
                               tw_user_followers_count_score,
                               tw_user_friends_count,
                               tw_user_friends_count_score,
                               tw_user_location,
                               expert_location_lat,
                               expert_location_lng,
                               tw_user_lang,
                               tw_user_domain_keywords_score,
                               tw_user_expert_keywords_score,
                               domain_id):
        """
        1. Insert new record in <tw_expert> DB table
        2. Insert new record in <tw_expert_domain_bridge> DB table
           for create many-to-many relation between <tw_expert> and <domain> DB tables
        (NOTE: More about Twitter User Object and User Data Dictionary by following link: 
        https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object)

        
        Arguments:
            tw_user_id_str {str} -- The string representation of the unique identifier for Twitter User
            tw_user_screen_name {str} -- The screen name, handle, or alias that this user identifies themselves with
            tw_user_name {str} -- The name of the user, as they've defined it
            tw_user_description {str} --  The user-defined UTF-8 string describing their account
            tw_user_statuses_count {int} -- The number of Tweets (including retweets) issued by the user
            tw_user_statuses_count_score {int} -- The score for the <tw_user_statuses_count> value on a five-point scale
            tw_user_followers_count {int} -- The number of followers this account currently has
            tw_user_followers_count_score {int} -- The score for the <tw_user_followers_count> value on a five-point scale
            tw_user_friends_count {int} -- The number of users this account is following (AKA their “followings”)
            tw_user_friends_count_score {int} -- The score for the <tw_user_friends_count_score> value on a five-point scale
            tw_user_location {str} -- The user-defined location for this account's profile
            expert_location_lat {float} -- The latitude of the location of the expert, 
                                           which is derived from the <tw_user_location> value using geocoding
                                            (None (NULL in DB) if the expert location could not be determined)
            expert_location_lng {float} -- The longitude of the location of the expert, 
                                           which is derived from the <tw_user_location> value using geocoding
                                           (None (NULL in DB) if the expert location could not be determined)
            tw_user_lang {str} -- The BCP 47 code for the user's self-declared user interface language
            tw_user_domain_keywords_score {int} -- The score for the all domain keywords that were found for Twitter user.
                                                   Calculated as a weighted average.
            tw_user_expert_keywords_score {int} -- The score for the all expert keywords that were found for Twitter user.
                                                   Calculated as a weighted average.
            domain_id {int} -- <domain_id> from <domain> DB table

        Returns:
            [int] -- <tw_expert_id> for new inserted record in <tw_expert> DB table
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            # execute INSERT SQL command for insert <tw_expert> in <tw_expert> DB table
            cursor.execute('INSERT INTO tw_expert( \
                tw_id_str, tw_screen_name, tw_name, tw_description, tw_statuses_count, tw_statuses_count_score,\
                tw_followers_count, tw_followers_count_score, tw_friends_count, tw_friends_count_score, tw_location,\
                expert_location_lat, expert_location_lng, tw_lang, domain_keywords_score, expert_keywords_score)\
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (tw_user_id_str, tw_user_screen_name, tw_user_name, tw_user_description,
                                       tw_user_statuses_count, tw_user_statuses_count_score,
                                       tw_user_followers_count, tw_user_followers_count_score,
                                       tw_user_friends_count, tw_user_friends_count_score,
                                       tw_user_location, expert_location_lat, expert_location_lng, tw_user_lang,
                                       tw_user_domain_keywords_score, tw_user_expert_keywords_score))

            # commit transaction to <monexp_db>
            conn.commit()
            
            # Re-perform SELECT for get <keyword_id> for new inserted record
            cursor.execute("SELECT * FROM tw_expert WHERE tw_id_str = %s LIMIT 1", (tw_user_id_str,))
            tw_expert_id = cursor.fetchone()[0]
            
            # execute INSERT SQL command for insert <tw_expert_id> and <domain_id> in <tw_expert_domain_bridge> DB table
            cursor.execute("INSERT INTO tw_expert_domain_bridge(tw_expert_id, domain_id) VALUES(%s, %s)",
                           (tw_expert_id, domain_id))
            
            # commit transaction to <monexp_db>
            conn.commit()

            # close cursor and connection
            self.close(cursor, conn)

            return tw_expert_id

        except mysql.Error:
            self.show_mysql_error()



    # ------------------------------------------------------
    def insert_tw_expert_keywords_in_db(self,
                                        tw_expert_id,
                                        domain_id,
                                        domain_analysis_tw_user_field_keywords_dict,
                                        expert_analysis_tw_user_field_keywords_dict):
        """
        Insert new record in <tw_expert_keywords> DB table
        
        Arguments:
            tw_expert_id {int} -- <tw_expert_id> from <tw_expert> DB table
            domain_id {int} -- <domain_id> from <domain> DB table
            domain_analysis_tw_user_field_keywords_dict {dict} -- results of analysis all domain keywords
            expert_analysis_tw_user_field_keywords_dict {dict} -- results of analysis all expert keywords 
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            # 1. Add keywords from  <domain_analysis_tw_user_field_keywords_dict>
            for keyword in domain_analysis_tw_user_field_keywords_dict:
                keyword_count = domain_analysis_tw_user_field_keywords_dict[keyword]
                if domain_analysis_tw_user_field_keywords_dict[keyword] > 0:
                    # execute SELECT SQL command for retrieve <keyword> from <keyword> DB table
                    cursor.execute("SELECT * FROM keyword WHERE keyword = %s LIMIT 1", (keyword,))
                    keyword_id = cursor.fetchone()[0]

                    # execute INSERT SQL command for insert new record in <tw_expert_keywords> DB table
                    cursor.execute("INSERT INTO tw_expert_keywords(tw_expert_id, keyword_id, keyword_count, domain_id) \
                                   VALUES(%s, %s, %s, %s)", (tw_expert_id, keyword_id, keyword_count, domain_id))

                    # commit transaction to <monexp_db>
                    conn.commit()

            # 2. Add keywords from  <expert_analysis_tw_user_field_keywords_dict>
            for keyword in expert_analysis_tw_user_field_keywords_dict:
                keyword_count = expert_analysis_tw_user_field_keywords_dict[keyword]
                if expert_analysis_tw_user_field_keywords_dict[keyword] > 0:
                    # execute SELECT SQL command for retrieve <keyword> from <keyword> DB table
                    cursor.execute("SELECT * FROM keyword WHERE keyword = %s LIMIT 1", (keyword,))
                    keyword_id = cursor.fetchone()[0]

                    # execute INSERT SQL command for insert new record in <tw_expert_keywords> DB table
                    cursor.execute("INSERT INTO tw_expert_keywords(tw_expert_id, keyword_id, keyword_count, domain_id) \
                                   VALUES(%s, %s, %s, %s)", (tw_expert_id, keyword_id, keyword_count, domain_id))

                    # commit transaction to <monexp_db>
                    conn.commit()

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()


    # ------------------------------------------------------
    def create_keywords_reference_db_tables(self, keywords_type_list, keywords_category_list):
        """
        Create following DB tables: 
            1. <keyword_type>
            2. <keyword_category>
        
        Arguments:
            keywords_type_list {list} -- ['domain', 'expert']
            keywords_category_list {list} -- ['tag', 'screen_name', 'hashtag', 'phrase']
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            # count number of records in <keyword_type> DB table
            num_records_in_keyword_type_db_table = self.num_records_in_db_table(cursor, 'keyword_type')

            # insert <keywords_type_list> values in <keyword_type> DB table
            # if <keyword_type> DB table is empty
            if num_records_in_keyword_type_db_table == 0:
                for keyword_type in keywords_type_list:
                    self.insert_keyword_type_in_db(conn, cursor, keyword_type)

            # count number of records in <keyword_category> DB table
            num_records_in_keyword_category_db_table = self.num_records_in_db_table(cursor, 'keyword_category')

            # insert <keywords_category_list> values in <keyword_category> DB table
            # if <keyword_category> DB table is empty
            if num_records_in_keyword_category_db_table == 0:
                for keyword_category in keywords_category_list:
                    self.insert_keyword_category_in_db(conn, cursor, keyword_category)

            # close cursor and connection
            self.close(cursor, conn)

        except mysql.Error:
            self.show_mysql_error()

    # ------------------------------------------------------
    def find_tw_expert_location_place_lat_lng_in_db(self, domain):
        """
        For preparing data for displaying experts for each domain on Google Map:
            1. Find record for specified <domain> in <domain> DB table
            2. Find record(s) with <expert_location_lat> and <expert_location_lng>,
               which are not NULL in <tw_expert> DB table (expert data) for specified <domain>
        
        Arguments:
            domain {str} -- domain name

        Returns:
            [tuple] -- <selected_domain_record_t> data from found record in <domain> DB table 
                       (or None) 
            [tuple] -- <selected_experts_records_t> data from found record(s) in <tw_expert> DB table
                       (or None) 
        """

        try:

            # connect to MySQL Server
            conn, cursor = self.connect()

            # use monexp_db
            self.use_db(cursor)

            selected_domain_record_t = tuple()
            selected_experts_records_t = tuple()

            #1. Find specified domain in <domain> DB table

            # execute SELECT SQL command for retrieve <domain> from <domain> DB table
            cursor.execute("SELECT domain_id FROM domain WHERE domain = %s LIMIT 1", (domain,))

            selected_domain_record_t = cursor.fetchone()

            # If the specified <domain> is not in the <domain> DB table then
            # return selected_domain_record_t=None and selected_experts_records_t=None
            if selected_domain_record_t is None:
                return selected_domain_record_t, selected_experts_records_t

            # Find record(s) with <expert_location_lat> and <expert_location_lng>,
            # which are not NULL in <tw_expert> DB table (expert data) for specified <domain>
            else:
                domain_id = selected_domain_record_t[0]

                # execute SELECT SQL command for retrieve <expert_location_lat> and <expert_location_lng>,
                # which are not NULL from <tw_expert> DB table
                cursor.execute("SELECT te.tw_location, te.expert_location_lat, te.expert_location_lng  \
                               FROM tw_expert AS te                                                    \
                               INNER JOIN  tw_expert_domain_bridge AS tedb                             \
                               ON te.tw_expert_id = tedb.tw_expert_id                                  \
                               WHERE tedb.domain_id = %s                                               \
                               AND NOT(te.expert_location_lat IS NULL and te.expert_location_lng IS NULL)",
                               (domain_id,))

                selected_experts_records_t = cursor.fetchall()

            # close cursor and connection
            self.close(cursor, conn)

            return selected_domain_record_t, selected_experts_records_t

        except mysql.Error:
            self.show_mysql_error()
