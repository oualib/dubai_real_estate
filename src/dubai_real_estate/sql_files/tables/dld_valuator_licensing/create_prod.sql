CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
	"valuation_company_number" Int128 COMMENT '[PK] Valuation company registration number',
	"valuation_company_name_english" Nullable(String) COMMENT '[NAME] Valuation company official name',
	"valuation_company_name_arabic" Nullable(String) COMMENT '[NAME] Valuation company name in Arabic',
	"valuator_number" Nullable(Int128) COMMENT '[REF] Individual valuator license number',
	"valuator_name_english" Nullable(String) COMMENT '[NAME] Licensed valuator full name',
	"valuator_name_arabic" Nullable(String) COMMENT '[NAME] Licensed valuator name in Arabic',
	"license_start_date" Nullable(Date) COMMENT '[DATE] Valuator license start date',
	"license_end_date" Nullable(Date) COMMENT '[DATE] Valuator license expiration date',
	"valuator_nationality_english" Nullable(String) COMMENT '[ENUM] Valuator nationality',
	"valuator_nationality_arabic" Nullable(String) COMMENT '[ENUM] Valuator nationality in Arabic',
	"is_female" Nullable(Bool) COMMENT '[BOOL] Gender indicator (1=female, 0=male)'
) 
ENGINE = MergeTree()
PRIMARY KEY("valuation_company_number")
COMMENT 'Licensed property valuators and valuation companies';