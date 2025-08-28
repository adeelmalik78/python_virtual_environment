###
### This script checks for column names should begin with first character of each word in the table name followed by an underscore
###
### Author: Adeel Malik

###
### Helpers come from Liquibase
###
from liquibase_checks_python import liquibase_utilities as lb
from liquibase_checks_python import liquibase_json as lbsnapshot
import sys
import wordninja


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


def abbr_table(input_data):
    """
    Return abbreviation of each dictionary word.

    Args:
        input_data: A list of strings to check.

    Returns:
        Abbreviation of each dictionary word.
    """

    abbr = ""

    for word in input_data:
        abbr = abbr + word[0]

    return abbr


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

### Retrieve database object the liquibase policy check is examining
database_object = lb.get_database_object()

# ### Retrieve object type and object name
object_type = database_object.getObjectTypeName().lower()

if "table" in object_type:

    table_name = database_object.getName()

    # Find words in table name
    dictionary_words = []
    dictionary_words = find_dictionary_words(table_name)

    # Obtain abbreviations of words in table name
    table_abbr = abbr_table(dictionary_words)
    # print (script_name + "Dictionary words in table name: " + str(dictionary_words) + ", abbreviation: " + table_abbr)

    # We need to ensure that numeric columns are not in scope ... 
    # So we need to detect column type.

    ###
    ### We will get column's data type from snapshot --> get table object from snapshot --> get column objects from table object
    ### Based on the requirement that column must by numeric.
    ###
    snapshot_object = lb.get_snapshot()
    table_from_snapshot = lbsnapshot.get_table(snapshot_object, table_name)

    columns_from_snapshot = lbsnapshot.get_columns(snapshot_object, table_name)

    bad_columns = []
    
    for column_from_snapshot in columns_from_snapshot:

        column_name = column_from_snapshot["column"]["name"]
        column_type = lbsnapshot.get_column_type_name(column_from_snapshot)

        if not "int" in column_type:
            # Non-numeric columns only

            expected_column_name_initial = table_abbr.lower() + "_"
            
            column_name_matched = expected_column_name_initial in column_name.lower()

            if not column_name_matched:
                bad_columns.append(column_name)
                print (script_name + "Table name: " + table_name + ", Column names: " + str(bad_columns) + ", Column type: " + column_type + ", " + str(column_name_matched)) 


    liquibase_status.fired = True
    status_message = "Column name \"" + f"{str(bad_columns)}" + "\" invalid. column names should begin with first character of each word in the table name followed by an underscore, in this case, \"" + expected_column_name_initial + "\""
    liquibase_status.message = status_message
    sys.exit(1)

False