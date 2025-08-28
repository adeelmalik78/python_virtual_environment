###
### This script checks for to table name to consist of at least two words
###
### Author: Adeel Malik

###
### Helpers come from Liquibase
###
from liquibase_checks_python import liquibase_utilities as lb
import re
import sys
import wordninja

def extract_table_names(content):
    """Extract table names from CREATE TABLE content in SQL file."""
    table_names = []
            
    # Regular expression to match CREATE TABLE statements
    # Matches both [dbo].[TableName] and dbo.TableName formats
    pattern = r'CREATE\s+TABLE\s+(?:\[?dbo\]?\.)?\[?(\w+)\]?'
    
    matches = re.findall(pattern, content, re.IGNORECASE)
    table_names.extend(matches)
            
    return table_names


def find_dictionary_words(input_data):
    """
    Check which words are English dictionary words.
    
    Args:
        input_data:A mixed case string (e.g., "ToDoItem" or "todoItem")
        
    Returns:
        String: dictionary_words
        
    Examples:
        wordninja.split("toDoitem")
    """

    dictionary_words = []

    # Handle string input - split into words first
    dictionary_words = wordninja.split(input_data)
    
    return dictionary_words


def is_two_words(input_data):
    """
    Checks if a string consists of two dictionary words.

    Args:
        input_data: A list of strings to check.

    Returns:
        True if the string consists of two words, False otherwise.
    """

    two_words_found = False

    if len(input_data) >= 2:
        two_words_found = True
    else:
        two_words_found = False

    return two_words_found


# script_name = "table_name_is_two_words.py" + ": "
script_name = lb.get_script_path() + ": "


###
### Retrieve log handler
### Ex. liquibase_logger.info(message)
###
# liquibase_logger = liquibase_utilities.get_logger()
liquibase_logger = lb.get_logger()

###
### Retrieve status handler
###
# liquibase_status = liquibase_utilities.get_status()
liquibase_status = lb.get_status()

###
### Retrieve all changes in changeset
###
# changes = liquibase_utilities.get_changeset().getChanges()
changes = lb.get_changeset().getChanges()

###
### Loop through all changes
###
for change in changes:
    ###
    ###
    ### Split SQL into a list of strings to remove whitespace
    ###
    # sql_list = liquibase_utilities.generate_sql(change).split()
    # print (script_name + "sql_list:" + str(sql_list))

    table_names_list = []

    ### 
    ### Send the SQL to extract_table_names(string)
    ###
    # table_names_list = extract_table_names( liquibase_utilities.generate_sql(change) )
    table_names_list = extract_table_names( lb.generate_sql(change) )
    # print (script_name + "table name:" + str(table_names_list))

    for table_name in table_names_list:
        
        dictionary_words = []
        isTwoWords = False

        dictionary_words = find_dictionary_words(table_name)
        # print("Dictionary words: " + str(dictionary_words))

        isTwoWords = is_two_words(dictionary_words)
        # isPascalCase = is_pascal_case(dictionary_words)
        print (script_name + "Table name: " + table_name + ", " + str(isTwoWords))

        if not isTwoWords:
            liquibase_status.fired = True
            status_message = "Table name \"" + f"{table_name}" + "\" is NOT two words. Each table name must be at least two words."
            liquibase_status.message = status_message
            sys.exit(1)

False