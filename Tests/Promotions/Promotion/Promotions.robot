*** Settings ***
Resource    PromotionsKW.robot
*** Variables ***


*** Test Cases ***
TC-01-CRUD promotions
    [Tags]    Promotion Controller
    KW-CRUD Promotions

TC-02-Import Promotions
    [Tags]    Promotion Controller
    KW-Import Promotion

TC-03-Search Promotion By Filter
    [Tags]    Promotion Controller
    KW-Search Promotion


