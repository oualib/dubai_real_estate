CREATE OR REPLACE TABLE
        "{dld_database}"."{dld_table}"(
        "procedure_number" Nullable(Int128) COMMENT '[REF] Valuation procedure reference number',
        "row_status_code" Nullable(String) COMMENT '[STATUS] Record status code for data quality control',
        "procedure_year" Int128 COMMENT '[YEAR] Year when valuation procedure was conducted',
        "instance_date" Nullable(Date) COMMENT '[DATE] Date of valuation assessment',
        "area_name_english" Nullable(String) COMMENT '[GEO] Geographic area of valued property',
        "area_name_arabic" Nullable(String) COMMENT '[GEO] Geographic area in Arabic',
        "property_type_english" Nullable(String) COMMENT '[ENUM] Type of property valued (Unit|Villa|Land|Building|etc.)',
        "property_type_arabic" Nullable(String) COMMENT '[ENUM] Type of property valued in Arabic',
        "property_sub_type_english" Nullable(String) COMMENT '[ENUM] Detailed property subcategory for valuation',
        "property_sub_type_arabic" Nullable(String) COMMENT '[ENUM] Detailed property subcategory in Arabic',
        "procedure_area" Nullable(Float32) COMMENT '[UNIT:sqm] Property area used in valuation calculation',
        "actual_area" Nullable(Float32) COMMENT '[UNIT:sqm] Measured property area in square meter',
        "property_total_value" Nullable(Float32) COMMENT '[CURRENCY:AED] Total assessed property value in AED',
        "actual_worth" Nullable(Float32) COMMENT '[CURRENCY:AED] Actual market worth assessment in AED - benchmark for market pricing'
) 
ENGINE = MergeTree()
PRIMARY KEY("procedure_year")
COMMENT 'Official property valuations and market assessments by DLD valuators';