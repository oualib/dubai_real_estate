INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT 
	FORMAT_INT("valuation_company_number") AS "valuation_company_number",
	FIRST_AR(FORMAT_VARCHAR("valuation_company_name_ar"), FORMAT_VARCHAR("valuation_company_name_en"), NULL) AS "valuation_company_name_ar_final",
	FIRST_EN(FORMAT_VARCHAR("valuation_company_name_en"), FORMAT_VARCHAR("valuation_company_name_ar"), NULL) AS "valuation_company_name_en_final",
	FORMAT_INT("valuator_number") AS "valuator_number",
	FIRST_AR(FORMAT_NAME("valuator_name_ar"), FORMAT_NAME("valuator_name_en"), NULL) AS "valuator_name_ar_final",
	FIRST_EN(FORMAT_NAME("valuator_name_en"), FORMAT_NAME("valuator_name_ar"), NULL) AS "valuator_name_en_final",
	"license_start_date" AS "license_start_date",
	"license_end_date" AS "license_end_date",
	FORMAT_INT("valuator_nationality_id") AS "valuator_nationality_id",
	FORMAT_BOOL("gender_id") AS "is_female"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/35cb239c-1e3a-4183-b5ae-37fa5cb81ce4/resource/cf7f677e-220e-420d-a417-06ea83496bf0/download/valuator_licensing.csv',
    'CSVWithNames'
);