*** Settings ***
Library    Catalog
Library    JSONLibrary
Variables    CatalogVar
Library    serviceSpec

*** Variables ***

*** Keywords ***
KW-Create Catalog Product
#Step 1 : Create Catalog
    ${create_catalog}=    Create Catalog       ${create_catalog_json}   product
    should be equal     ${create_catalog.status_code}     ${201}
    ${catalog_response_body} =  Convert String to JSON      ${create_catalog.text}
    ${catalog_id}=   set variable    ${catalog_response_body['id']}
    ${catalog_description}=     set variable    ${catalog_response_body['description']}
    ${catalog_code}=     set variable    ${catalog_response_body['code']}
    ${catalog_name}=     set variable    ${catalog_response_body['name']}
    ${catalog_Type}=    set variable    ${catalog_response_body['catalogType']}

    @{Data_Check}   create list     ${catalog_code}     ${catalog_name}     ${catalog_Type}
    DB Search All       ${Data_Check}   catalog      _id.key     ${catalog_id}

    ${get_catalog} =    Get Catalog by ID   ${catalog_id}
    should be equal     ${get_catalog.status_code}     ${200}

    ${get_catalog_by_code} =    Get Catalog by Code   ${catalog_code}
    should be equal     ${get_catalog_by_code.status_code}     ${200}

    ${get_catalog_by_name} =    Get Catalog by Name   ${catalog_name}
    should be equal     ${get_catalog_by_name.status_code}     ${200}

    ${Search_catalog_Type}=     Get Catalog by Type  Product
    should be equal     ${Search_catalog_Type.status_code}     ${200}

#Step 2: Update Catalog
    ${update_catalog}=    Update Catalog       ${update_catalog_json}   product     ${catalog_id}
#    log to console      ${update_catalog.text}
    should be equal     ${update_catalog.status_code}     ${200}
    ${update_catalog_response_body} =  Convert String to JSON      ${update_catalog.text}
    ${catalog_description_updated}   set variable    ${update_catalog_response_body['description']}

    @{Data_Check}   create list     ${catalog_name}     ${catalog_Type}     ${catalog_description_updated}
    DB Search All       ${Data_Check}   catalog      _id.key     ${catalog_id}

    log to console      Service Specification name before update is : "${catalog_description}"and after update is "${catalog_description_updated}"
    should not be equal     ${catalog_description}        ${catalog_description_updated}

#Step 3 : Patch Life Cycle Status
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Test
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Active
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Launched
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Retired
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Obsolete
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Test
    should be equal     ${patch_lifecycle.status_code}     ${400}

#Step 4 : Delete Catalog
    ${delete_catalog}=     Delete Catalog   ${catalog_id}
    should be equal     ${delete_catalog.status_code}     ${204}

    ${get_catalog} =    Get Catalog by ID   ${catalog_id}
    should be equal     ${get_catalog.status_code}     ${404}

KW-Create Catalog Service
#Step 1 : Create Catalog
    ${create_catalog}=    Create Catalog       ${create_catalog_json}   service
#    log to console      ${create_catalog.text}
    should be equal     ${create_catalog.status_code}     ${201}
    ${catalog_response_body} =  Convert String to JSON      ${create_catalog.text}
    ${catalog_id}=   set variable    ${catalog_response_body['id']}
    ${catalog_description}=     set variable    ${catalog_response_body['description']}
    ${catalog_code}=     set variable    ${catalog_response_body['code']}
    ${catalog_name}=     set variable    ${catalog_response_body['name']}
    ${catalog_Type}=    set variable    ${catalog_response_body['catalogType']}

    @{Data_Check}   create list     ${catalog_code}     ${catalog_name}      ${catalog_description}
    DB Search All       ${Data_Check}   catalog      _id.key     ${catalog_id}

#Step 2: Update Catalog
    ${update_catalog}=    Update Catalog       ${update_catalog_json}   product     ${catalog_id}
#    log to console      ${update_catalog.text}
    should be equal     ${update_catalog.status_code}     ${200}
    ${update_catalog_response_body} =  Convert String to JSON      ${update_catalog.text}
    ${catalog_description_updated}   set variable    ${update_catalog_response_body['description']}

    @{Data_Check}   create list     ${catalog_name}      ${catalog_description_updated}
    DB Search All       ${Data_Check}   catalog      _id.key     ${catalog_id}

    log to console      Service Specification name before update is : "${catalog_description}"and after update is "${catalog_description_updated}"
    should not be equal     ${catalog_description}        ${catalog_description_updated}

#Step 3 : Patch Life Cycle Status
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Test
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Active
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Launched
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Retired
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Obsolete
    should be equal     ${patch_lifecycle.status_code}     ${200}

#Step 4 : Delete Catalog
    ${delete_catalog}=     Delete Catalog   ${catalog_id}
    should be equal     ${delete_catalog.status_code}     ${204}

    ${get_catalog} =    Get Catalog by ID   ${catalog_id}
    should be equal     ${get_catalog.status_code}     ${404}

KW-Create Catalog resource
#Step 1 : Create Catalog
    ${create_catalog}=    Create Catalog       ${create_catalog_json}   resource
#    log to console      ${create_catalog.text}
    should be equal     ${create_catalog.status_code}     ${201}
    ${catalog_response_body} =  Convert String to JSON      ${create_catalog.text}
    ${catalog_id}=   set variable    ${catalog_response_body['id']}
    ${catalog_description}=     set variable    ${catalog_response_body['description']}
    ${catalog_code}=     set variable    ${catalog_response_body['code']}
    ${catalog_name}=     set variable    ${catalog_response_body['name']}
    ${catalog_Type}=    set variable    ${catalog_response_body['catalogType']}


    @{Data_Check}   create list     ${catalog_code}     ${catalog_name}     ${catalog_description}
    DB Search All       ${Data_Check}   catalog      _id.key     ${catalog_id}

#Step 2: Update Catalog
    ${update_catalog}=    Update Catalog       ${update_catalog_json}   product     ${catalog_id}
#    log to console      ${update_catalog.text}
    should be equal     ${update_catalog.status_code}     ${200}
    ${update_catalog_response_body} =  Convert String to JSON      ${update_catalog.text}
    ${catalog_description_updated}   set variable    ${update_catalog_response_body['description']}

    @{Data_Check}   create list     ${catalog_name}     ${catalog_description_updated}
    DB Search All       ${Data_Check}   catalog      _id.key     ${catalog_id}

    log to console      Service Specification name before update is : "${catalog_description}"and after update is "${catalog_description_updated}"
    should not be equal     ${catalog_description}        ${catalog_description_updated}

#Step 3 : Patch Life Cycle Status
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Test
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Active
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Launched
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Retired
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Obsolete
    should be equal     ${patch_lifecycle.status_code}     ${200}

#Step 4 : Delete Catalog
    ${delete_catalog}=     Delete Catalog   ${catalog_id}
    should be equal     ${delete_catalog.status_code}     ${204}

    ${get_catalog} =    Get Catalog by ID   ${catalog_id}
    should be equal     ${get_catalog.status_code}     ${404}

KW-Catalog Get All Calls
     ${Get_catalog}=    Get Catalog
     should be equal     ${Get_catalog.status_code}     ${200}

KW-Get Catalog By Search
     ${Search_catalog}=     Get Catalog Search
     should be equal     ${Search_catalog.status_code}     ${200}

KW-Get Catalog By Type
    ${Search_catalog_Type}=     Get Catalog by Type      Product
    should be equal     ${Search_catalog_Type.status_code}     ${200}

KW-Catalog LCM PATCH Negative
    ${create_catalog}=    Create Catalog       ${create_catalog_json}   product
    should be equal     ${create_catalog.status_code}     ${201}
    ${catalog_response_body} =  Convert String to JSON      ${create_catalog.text}
    ${catalog_id}=   set variable    ${catalog_response_body['id']}

    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Retired
    should be equal     ${patch_lifecycle.status_code}     ${400}
    should contain    ${patch_lifecycle.text}   "Transition from 'Design' to 'Retired' is not allowed for CATALOG entity ","exception":"LifecycleStatusException"
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Test
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Active
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Launched
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Retired
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Obsolete
    should be equal     ${patch_lifecycle.status_code}     ${200}
    ${patch_lifecycle}=     Patch Update LifeCycleStatus Catalog   ${catalog_id}      Test
    should be equal     ${patch_lifecycle.status_code}     ${400}
    should contain    ${patch_lifecycle.text}   "Transition from 'Obsolete' to 'Test' is not allowed for CATALOG entity ","exception":"LifecycleStatusException"

KW-Catalog Error Message Validation
    ${create_catalog}=    Create Catalog       ${error_val_catalog_json}   product
    should be equal     ${create_catalog.status_code}     ${400}
    should contain    ${create_catalog.text}    "message":"INVALID_INPUT_REQUEST","errors":[{"detail":"#: required key [lifecycleStatus] not found","exception":"EntityValidationException"}]}