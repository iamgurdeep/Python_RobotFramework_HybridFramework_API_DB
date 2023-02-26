*** Settings ***
Resource    CatalogKW.robot

*** Variables ***


*** Test Cases ***
#TC-01-Create Catalog Product
#    [Tags]    Catalog Controller
#    [Documentation]    This test case is executed to verify CRUD APIs for Product Catalog management
#    KW-Create Catalog Product

#TC-02-Create Catalog Service
#    [Tags]    Catalog Controller
#    [Documentation]    This test case is executed to verify CRUD APIs for Service Catalog management
#    KW-Create Catalog Service
#
#TC-03-Create Catalog Resource
#    [Tags]    Catalog Controller
#    [Documentation]    This test case is executed to verify CRUD APIs for Resource Catalog management
#    KW-Create Catalog resource
#
#TC-04 Catalog Get All Calls
#    [Tags]    Catalog Controller
#    [Documentation]    This test case is executed to verify GET all API of Catalog Management
#    KW-Catalog Get All Calls
#
#TC-05-Get Catalog By Search
#    [Tags]    Catalog Controller
#    [Documentation]    This test case is executed to verify GET By Search API of Catalog Management
#    KW-Get Catalog By Search
#
#TC-06-Get Catalog By Type
#    [Tags]    Catalog Controller
#    [Documentation]    This test case is executed to verify GET By Type API of Catalog Management
#    KW-Get Catalog By Type
#
#TC-07-Catalog LCM PATCH Negative
#    [Tags]    Catalog Controller
#    [Documentation]    This test case is executed to verify Catalog LCM PATCH Negative validations Catalog Management
#    KW-Catalog LCM PATCH Negative

TC-08-Catalog Error Message Validation
    KW-Catalog Error Message Validation