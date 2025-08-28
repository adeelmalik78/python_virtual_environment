###
### This script checks for Numeric primary key should begin with ID_ followed by first character of each word in the table name
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

### Retrieve object type and object name
object_type = database_object.getObjectTypeName().lower()

if "primarykey" in object_type:
    pk_name = database_object.getName().lower()
    # print (script_name + "Primary key name=" + pk_name + ", Object type=" + object_type)
 
    pk_table_name = database_object.getTable().getName()

    # Find words in table name
    dictionary_words = []
    dictionary_words = find_dictionary_words(pk_table_name)

    # Obtain abbreviations of words in table name
    table_abbr = abbr_table(dictionary_words)
    print (script_name + "Dictionary words in table name: " + str(dictionary_words) + ", abbreviation: " + table_abbr)

    # Obtain columns from primary key
    pk_columns = database_object.getColumns()
    for pk_each_column in pk_columns:
        # print (script_name + "Primary key name=" + pk_name + ", Table name: " + pk_table_name + ", Column name:" + pk_each_column.getName())

        ###
        ### We will get column's data type from snapshot --> get table object from snapshot --> get column objects from table object
        ### Based on the requirement that column must by numeric.
        ###
        snapshot_object = lb.get_snapshot()
        table_from_snapshot = lbsnapshot.get_table(snapshot_object, pk_table_name)

        columns_from_snapshot = lbsnapshot.get_columns(snapshot_object, pk_table_name)

        for column_from_snapshot in columns_from_snapshot:

            # If column from snapshot matches with column in primary key ...
            if column_from_snapshot["column"]["name"] in pk_each_column.getName():
                column_type = lbsnapshot.get_column_type_name(column_from_snapshot)
                print (script_name + "Primary key name=" + pk_name + ", Table name: " + pk_table_name + ", Column name:" + pk_each_column.getName() + "Column type: " + column_type)

                # Fail the check if column type is not numeric and if it does not adhere to ID_ followed by table name abbreviation
                if not ("int" in column_type and ("ID_" + table_abbr) == pk_each_column.getName() ) :
                    liquibase_status.fired = True
                    status_message = "Primary key \"" + f"{pk_each_column.getName()}" + "\" invalid. It does not conform to numeric primary key should begin with ID_ followed by first character of each word in the table name \"" + pk_table_name + "\""
                    liquibase_status.message = status_message
                    sys.exit(1)

False