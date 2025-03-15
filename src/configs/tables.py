####################################################
# Tables Postgre Adventureworks
####################################################

# Mapping of source queries to target tables
source_queries_to_tables = {
    #schema humanresources
    "SELECT * FROM humanresources.department": "stg.stg_department",
    "SELECT * FROM humanresources.employee": "stg.stg_employee",
    "SELECT * FROM humanresources.employeedepartmenthistory": "stg.stg_employeedepartmenthistory",
    "SELECT * FROM humanresources.employeepayhistory": "stg.stg_employeepayhistory",
    
    #schema production
    "SELECT * FROM production.culture": "stg.stg_culture",
    "SELECT * FROM production.location": "stg.stg_location",
    "SELECT * FROM production.product": "stg.stg_product",
    "SELECT * FROM production.productcategory": "stg.stg_productcategory",
    "SELECT * FROM production.productdescription": "stg.stg_productdescription",
    "SELECT * FROM production.productreview": "stg.stg_productreview",

    #schema purchasing
    "SELECT * FROM purchasing.productvendor": "stg.stg_productvendor",

    #schema sales
    "SELECT * FROM sales.countryregioncurrency": "stg.stg_countryregioncurrency",
}
