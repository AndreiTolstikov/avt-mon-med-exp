import time

from avt_mon_med_exp import mysql_monexp_db
from avt_mon_med_exp import prepare_domains_data
from avt_mon_med_exp import tw_search_experts


print('\n ---------------------------------------------------------------------')
print(' The avtMonMedExp app began to search and analyze experts on Twitter ...')
print(' -----------------------------------------------------------------------')

# avtMonExp start time
avtmonexp_start_time = time.time()

print('\n ---')
print(' Timestamp (UTC): ', time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime(avtmonexp_start_time)))

# Prepare domains data from JSON file (by default "domains_data.json") for further processing
domains_data_file_name = r'domains_data.json'

print('\n ---')
print(' Prepare data from <%s> file...' % domains_data_file_name)

all_domains_json = prepare_domains_data.load_domains_data(domains_data_file_name)

# Prepare to work with monexp_db (as MySQL)

# Create MySQLMonExpDb() class instance
monexp_db = mysql_monexp_db.MySQLMonExpDb()


# Drop monexp_db
print('\n ---')
print(' Drop <monexp_db> database...')
monexp_db.drop_db()


# Create monexp_db
print('\n ---')
print(' Create <monexp_db> database...')
monexp_db.create_db()

# Create DB tables in monexp_db
print('\n ---')
print(' Create tables in <monexp_db> database...')
monexp_db.create_db_tables()

# Create TwSearchExperts() class instance
ts_experts = tw_search_experts.TwSearchExperts()

# Search domain experts from Twitter users
print('\n ---')
print(' Search and analysis experts from Twitter users...')
ts_experts.tw_search_and_analysis_experts(all_domains_json, True, 
                                            monexp_db, avtmonexp_start_time)

# avtMonExp end time
avtmonexp_end_time = time.time()

# The avtMonExp run elapsed time
avtmonexp_run_elapsed_time = avtmonexp_end_time - avtmonexp_start_time 

print('\n ---')
print(' Timestamp (UTC): ', time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime(avtmonexp_end_time)))

print('\n ---------------------------------------------------------------------')
print(' The avtMonMedExp app successfully completed.')
print(' -----------------------------------------------------------------------')
print(' Elapsed time: ', time.strftime("%H:%M:%S", time.gmtime(avtmonexp_run_elapsed_time)))
print(' -----------------------------------------------------------------------')
