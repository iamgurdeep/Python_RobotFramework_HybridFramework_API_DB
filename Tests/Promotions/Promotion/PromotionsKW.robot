*** Settings ***
Library    Promotions
Library    JSONLibrary
Variables    PromotionsVar
Library    serviceSpec
Variables    serviceSpecVar
Library    MChar
Variables    MCharVar
Library    Pmetaext
Variables    PmetaextVar
Library    ProductSpec
Variables    ProductSpecVar

*** Variables ***

*** Keywords ***

KW-CRUD Promotions
#Step 1 : Create Tax
    ${create_response}=    Create Promotion       ${create_promotion_json}
    log to console      ${create_response.text}
    should be equal     ${create_response.status_code}     ${201}
    ${create_promotion_response_body}=    Convert String to JSON  ${create_response.text}
    log to console    ${create_promotion_response_body}
    ${promotion_id} =    set variable    ${create_promotion_response_body['id']}
    ${promotion_name} =    set variable    ${create_promotion_response_body['name']}
    ${promotion_type} =    set variable    ${create_promotion_response_body['type']}
    ${promotion_createdBy} =    set variable    ${create_promotion_response_body['createdBy']}
    ${promotion_externalID} =    set variable    ${create_promotion_response_body['externalID']}
    ${promotion_description} =    set variable    ${create_promotion_response_body['description']}
    ${promotion_promoApplicationLevel} =    set variable    ${create_promotion_response_body['promoApplicationLevel']}
    ${promotion_promotionClassification} =    set variable    ${create_promotion_response_body['promotionClassification']}
    ${promotion_code} =    set variable    ${create_promotion_response_body['code']}
    @{Data_Check}=    create list   ${promotion_id}   ${promotion_name}     ${promotion_type}       ${promotion_createdBy}      ${promotion_externalID}     ${promotion_description}        ${promotion_promoApplicationLevel}      ${promotion_promotionClassification}
    DB Search All       ${Data_Check}   promotion      _id     ${promotion_id}

    ${get_promotion_by_code}=      Get Promotion By Code   ${promotion_code}
    log to console     ${get_promotion_by_code.text}
    should be equal     ${get_promotion_by_code.status_code}     ${200}


#tep 2 : Update Promotions
    ${update_promotion}=      Update_Promotion    ${Update_Promotion_json}     ${promotion_id}
    log to console      ${update_promotion.text}
    should be equal     ${update_promotion.status_code}     ${200}
    ${update_promotion_body}=    Convert String to JSON  ${update_promotion.text}
    ${update_id} =    set variable    ${update_promotion_body['id']}
    log to console    update id is ========================${update_id}
    ${update_name} =    set variable    ${update_promotion_body['name']}
    ${update_promotion_type} =    set variable    ${update_promotion_body['type']}
    ${update_promotion_createdBy} =    set variable    ${update_promotion_body['createdBy']}
    ${update_promotion_externalID} =    set variable    ${update_promotion_body['externalID']}
    ${update_promotion_description} =    set variable    ${update_promotion_body['description']}
    ${update_promotion_promoApplicationLevel} =    set variable    ${update_promotion_body['promoApplicationLevel']}
    ${update_promotion_promotionClassification} =    set variable    ${update_promotion_body['promotionClassification']}
    @{Data_Check}=    create list   ${promotion_id}   ${update_name}     ${update_promotion_type}       ${update_promotion_createdBy}      ${update_promotion_externalID}     ${update_promotion_description}
    DB Search All       ${Data_Check}   promotion        _id     ${promotion_id}
    log to console      Updated Promotion name before update is : "${promotion_name}"and after update is "${update_name}"
    should not be equal     ${promotion_name}        ${update_name}


    # Get Promotion By ID
    ${get_promotion_by_id}=      Get Promotion By Id   ${promotion_id}
    should be equal     ${get_promotion_by_id.status_code}     ${200}
 # Get Promotion By Code

    #Step 6 : Patch Meta Extensions
    ${patch_response}=      Patch MetaExt Promotion     ${patch_resmetaext_json}    ${promotion_id}
    log to console      ${patch_response.text}
    should be equal     ${patch_response.status_code}      ${200}

#Step 9 : Patch Pro Status Change
    ${patch_lifecyclestatus}=   patch promotion lifecycle status        ${promotion_id}    Test
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}

    ${patch_lifecyclestatus}=   patch promotion lifecycle status  ${promotion_id}    Active
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}

    ${patch_lifecyclestatus}=   patch promotion lifecycle status  ${promotion_id}    Retired
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}

    ${patch_lifecyclestatus}=   patch promotion lifecycle status  ${promotion_id}    Obsolete
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}
#
#
#
# Delete Promotion

    ${delete_promotion} =    Delete Promotion 	${promotion_id}
#    log to console    ${delete_resource_spec.text}
    should be equal    ${delete_promotion.status_code}  ${204}
    log to console    "Promotion DELETED succesfully"




KW-Import Promotion
    ${create_response}=    Create Promotion       ${create_promotion_json}
    log to console      ${create_response.text}
    should be equal     ${create_response.status_code}     ${201}
    ${create_promotion_response_body}=    Convert String to JSON  ${create_response.text}
    log to console    ${create_promotion_response_body}
    ${promotion_id} =    set variable    ${create_promotion_response_body['id']}
    ${promotion_name} =    set variable    ${create_promotion_response_body['name']}
    ${promotion_type} =    set variable    ${create_promotion_response_body['type']}
    ${promotion_createdBy} =    set variable    ${create_promotion_response_body['createdBy']}
    ${promotion_externalID} =    set variable    ${create_promotion_response_body['externalID']}
    ${promotion_description} =    set variable    ${create_promotion_response_body['description']}
    ${promotion_promoApplicationLevel} =    set variable    ${create_promotion_response_body['promoApplicationLevel']}
    ${promotion_promotionClassification} =    set variable    ${create_promotion_response_body['promotionClassification']}
    ${promotion_code} =    set variable    ${create_promotion_response_body['code']}
    @{Data_Check}=    create list   ${promotion_id}   ${promotion_name}     ${promotion_type}       ${promotion_createdBy}      ${promotion_externalID}     ${promotion_description}        ${promotion_promoApplicationLevel}      ${promotion_promotionClassification}
    DB Search All       ${Data_Check}   promotion      _id     ${promotion_id}

    ${patch_lifecyclestatus}=   patch promotion lifecycle status        ${promotion_id}    Test
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}

    ${patch_lifecyclestatus}=   patch promotion lifecycle status  ${promotion_id}    Active
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}

    ${patch_lifecyclestatus}=   patch promotion lifecycle status  ${promotion_id}    Retired
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}

    ${patch_lifecyclestatus}=   patch promotion lifecycle status  ${promotion_id}    Obsolete
    should be equal     ${patch_lifecyclestatus.status_code}     ${200}
# Delete Promotion
    ${delete_promotion} =    Delete Promotion 	${promotion_id}
    should be equal    ${delete_promotion.status_code}  ${204}
    log to console    "Promotion DELETED succesfully"



KW-Search Promotion

 # Get Promotion By Search
    ${search_promotion}=      Search Promotion     lifecycleStatus=Design
    should be equal     ${search_promotion.status_code}     ${206}

    ${search_promotion}=      Search Promotion     lifecycleStatus=Test
    should be equal     ${search_promotion.status_code}     ${206}

    ${search_promotion}=      Search Promotion     lifecycleStatus=Active
    should be equal     ${search_promotion.status_code}     ${206}

    ${search_promotion}=      Search Promotion     lifecycleStatus=Obsolete
    should be equal     ${search_promotion.status_code}     ${200}
