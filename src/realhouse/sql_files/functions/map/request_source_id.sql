CREATE OR REPLACE FUNCTION MAP_REQUEST_SOURCE_EN AS (x) ->
    CASE 
        WHEN x = 1  THEN 'Dubai Land Department'
        WHEN x = 3  THEN 'Real Estate Registration Trustees Offices'
        WHEN x = 4  THEN 'Real Estate Services Trustees Offices'
        WHEN x = 5  THEN 'Real Estate Developers Offices'
        WHEN x = 15 THEN 'Dubai REST Smart Application'
    END;

CREATE OR REPLACE FUNCTION MAP_REQUEST_SOURCE_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'دائرة الاراضي والاملاك'
        WHEN x = 3 THEN 'مكاتب امين التسجيل العقاري'
        WHEN x = 4 THEN 'مكاتب امين الخدمات العقاري'
        WHEN x = 5 THEN 'مكاتب المطورين العقاريين'
        WHEN x = 15 THEN 'تطبيق دبي ريست'
    END;