-- MAIN FUNCTION
CREATE OR REPLACE FUNCTION MAP_ID AS (x, x_name, en) ->
	CASE 
		WHEN en THEN
			CASE 
				WHEN x_name = 'activity_type_id' 
				THEN MAP_ACTIVITY_TYPE_EN(x)
				WHEN x_name = 'application_id' 
				THEN MAP_APPLICATION_EN(x)
				WHEN x_name = 'area_id' 
				THEN MAP_AREA_NAME_EN(x)
				WHEN x_name = 'contract_reg_type_id' 
				THEN MAP_CONTRACT_REG_TYPE_EN(x)
				WHEN x_name = 'ejari_property_type_id' 
				THEN MAP_EJARI_PROPERTY_TYPE_EN(x)
				WHEN x_name = 'escrow_agent_id' 
				THEN MAP_ESCROW_AGENT_EN(x)
				WHEN x_name = 'land_type_id' 
				THEN MAP_LAND_TYPE_EN(x)
				WHEN x_name = 'legal_status_id' 
				THEN MAP_LEGAL_STATUS_EN(x)
				WHEN x_name = 'legal_type_id' 
				THEN MAP_LEGAL_TYPE_EN(x)
				WHEN x_name = 'license_source_id' 
				THEN MAP_LICENSE_SOURCE_EN(x)
				WHEN x_name = 'license_type_id' 
				THEN MAP_LICENSE_TYPE_EN(x)
				WHEN x_name = 'master_community_id' 
				THEN MAP_MASTER_COMMUNITY_EN(x)
				WHEN x_name = 'nationality_id' 
				THEN MAP_NATIONALITY_EN(x)
				WHEN x_name = 'nearest_landmark_id' 
				THEN MAP_NEAREST_LANDMARK_EN(x)
				WHEN x_name = 'nearest_mall_id' 
				THEN MAP_NEAREST_MALL_EN(x)
				WHEN x_name = 'nearest_metro_id' 
				THEN MAP_NEAREST_METRO_EN(x)
				WHEN x_name = 'parking_allocation_type_id' 
				THEN MAP_PARKING_ALLOCATION_TYPE_EN(x)
				WHEN x_name = 'permit_status_id' 
				THEN MAP_PERMIT_STATUS_EN(x)
				WHEN x_name = 'procedure_id' 
				THEN MAP_PROCEDURE_EN(x)
				WHEN x_name = 'project_classification_id' 
				THEN MAP_PROJECT_CLASSIFICATION_EN(x)
				WHEN x_name = 'project_status_id' 
				THEN MAP_PROJECT_STATUS_EN(x)
				WHEN x_name = 'project_type_id' 
				THEN MAP_PROJECT_TYPE_EN(x)
				WHEN x_name = 'property_sub_type_id' 
				THEN MAP_PROPERTY_SUB_TYPE_EN(x)
				WHEN x_name = 'property_type_id' 
				THEN MAP_PROPERTY_TYPE_EN(x)
				WHEN x_name = 'property_usage_id' 
				THEN MAP_PROPERTY_USAGE_EN(x)
				WHEN x_name = 'reg_type_id' 
				THEN MAP_REG_TYPE_EN(x)
				WHEN x_name = 'request_source_id' 
				THEN MAP_REQUEST_SOURCE_EN(x)
				WHEN x_name = 'rooms_id' 
				THEN MAP_ROOMS_EN(x)
				WHEN x_name = 'sercive_category_id' 
				THEN MAP_SERVICE_CATEGORY_EN(x)
				WHEN x_name = 'service_id' 
				THEN MAP_SERVICE_EN(x)
				WHEN x_name = 'status_id' 
				THEN MAP_STATUS_EN(x)
				WHEN x_name = 'tenant_type_id' 
				THEN MAP_TENANT_TYPE_EN(x)
				WHEN x_name = 'trans_group_id' 
				THEN MAP_TRANS_GROUP_EN(x)
				WHEN x_name = 'usage_id' 
				THEN MAP_USAGE_EN(x)
				WHEN x_name = 'zoning_authority_id' 
				THEN MAP_ZONING_AUTHORITY_EN(x)
			END
		ELSE
			CASE 
				WHEN x_name = 'activity_type_id' 
				THEN MAP_ACTIVITY_TYPE_AR(x)
				WHEN x_name = 'application_id' 
				THEN MAP_APPLICATION_AR(x)
				WHEN x_name = 'area_id' 
				THEN MAP_AREA_NAME_AR(x)
				WHEN x_name = 'contract_reg_type_id' 
				THEN MAP_CONTRACT_REG_TYPE_AR(x)
				WHEN x_name = 'ejari_property_type_id' 
				THEN MAP_EJARI_PROPERTY_TYPE_AR(x)
				WHEN x_name = 'escrow_agent_id' 
				THEN MAP_ESCROW_AGENT_AR(x)
				WHEN x_name = 'land_type_id' 
				THEN MAP_LAND_TYPE_AR(x)
				WHEN x_name = 'legal_status_id' 
				THEN MAP_LEGAL_STATUS_AR(x)
				WHEN x_name = 'legal_type_id' 
				THEN MAP_LEGAL_TYPE_AR(x)
				WHEN x_name = 'license_source_id' 
				THEN MAP_LICENSE_SOURCE_AR(x)
				WHEN x_name = 'license_type_id' 
				THEN MAP_LICENSE_TYPE_AR(x)
				WHEN x_name = 'master_community_id' 
				THEN MAP_MASTER_COMMUNITY_AR(x)
				WHEN x_name = 'nationality_id' 
				THEN MAP_NATIONALITY_AR(x)
				WHEN x_name = 'nearest_landmark_id' 
				THEN MAP_NEAREST_LANDMARK_AR(x)
				WHEN x_name = 'nearest_mall_id' 
				THEN MAP_NEAREST_MALL_AR(x)
				WHEN x_name = 'nearest_metro_id' 
				THEN MAP_NEAREST_METRO_AR(x)
				WHEN x_name = 'parking_allocation_type_id' 
				THEN MAP_PARKING_ALLOCATION_TYPE_AR(x)
				WHEN x_name = 'permit_status_id' 
				THEN MAP_PERMIT_STATUS_AR(x)
				WHEN x_name = 'procedure_id' 
				THEN MAP_PROCEDURE_AR(x)
				WHEN x_name = 'project_classification_id' 
				THEN MAP_PROJECT_CLASSIFICATION_AR(x)
				WHEN x_name = 'project_status_id' 
				THEN MAP_PROJECT_STATUS_AR(x)
				WHEN x_name = 'project_type_id' 
				THEN MAP_PROJECT_TYPE_AR(x)
				WHEN x_name = 'property_sub_type_id' 
				THEN MAP_PROPERTY_SUB_TYPE_AR(x)
				WHEN x_name = 'property_type_id' 
				THEN MAP_PROPERTY_TYPE_AR(x)
				WHEN x_name = 'property_usage_id' 
				THEN MAP_PROPERTY_USAGE_AR(x)
				WHEN x_name = 'reg_type_id' 
				THEN MAP_REG_TYPE_AR(x)
				WHEN x_name = 'request_source_id' 
				THEN MAP_REQUEST_SOURCE_AR(x)
				WHEN x_name = 'rooms_id' 
				THEN MAP_ROOMS_AR(x)
				WHEN x_name = 'sercive_category_id' 
				THEN MAP_SERVICE_CATEGORY_AR(x)
				WHEN x_name = 'service_id' 
				THEN MAP_SERVICE_AR(x)
				WHEN x_name = 'status_id' 
				THEN MAP_STATUS_AR(x)
				WHEN x_name = 'tenant_type_id' 
				THEN MAP_TENANT_TYPE_AR(x)
				WHEN x_name = 'trans_group_id' 
				THEN MAP_TRANS_GROUP_AR(x)
				WHEN x_name = 'usage_id' 
				THEN MAP_USAGE_AR(x)
				WHEN x_name = 'zoning_authority_id' 
				THEN MAP_ZONING_AUTHORITY_AR(x)
			END
	END;

-- EN FUNCTION
CREATE OR REPLACE FUNCTION MAP_ID_EN AS (x, x_name) -> MAP_ID(x, x_name, True);

-- AR FUNCTION
CREATE OR REPLACE FUNCTION MAP_ID_AR AS (x, x_name) -> MAP_ID(x, x_name, False);