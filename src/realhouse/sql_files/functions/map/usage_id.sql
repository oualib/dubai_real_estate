CREATE OR REPLACE FUNCTION MAP_USAGE_EN AS (x) ->
    CASE 
        WHEN x = 1  THEN 'Residential'
        WHEN x = 2  THEN 'Offices'
        WHEN x = 3  THEN 'Mixed'
        WHEN x = 4  THEN 'Retail'
        WHEN x = 5  THEN 'Parking'
        WHEN x = 6  THEN 'Parking'
        WHEN x = 7  THEN 'Stores'
        WHEN x = 8  THEN 'Clinic'
        WHEN x = 9  THEN 'Education'
        WHEN x = 13 THEN 'Hospitality'
        WHEN x = 14 THEN 'Public Facility'
        WHEN x = 17 THEN 'Healthcare'
        WHEN x = 18 THEN 'Recreational'
        WHEN x = 19 THEN 'Open Space'
        WHEN x = 22 THEN 'Transportation'
        WHEN x = 24 THEN 'Future Development'
    END;

CREATE OR REPLACE FUNCTION MAP_USAGE_AR AS (x) ->
    CASE 
        WHEN x = 1  THEN 'سكني'
        WHEN x = 2  THEN 'تجاري'
        WHEN x = 3  THEN 'مختلط'
        WHEN x = 4  THEN 'التجزئه'
        WHEN x = 5  THEN 'وقوف السيارات'
        WHEN x = 6  THEN 'وقوف السيارات'
        WHEN x = 7  THEN 'متاجر'
        WHEN x = 8  THEN 'عيادة'
        WHEN x = 9  THEN 'تعليم'
        WHEN x = 13 THEN 'ضيافة'
        WHEN x = 14 THEN 'مرفق عام'
        WHEN x = 17 THEN 'الرعاية الصحية'
        WHEN x = 18 THEN 'ترفيهية'
        WHEN x = 19 THEN 'الفضاء المفتوح'
        WHEN x = 22 THEN 'مواصلات'
        WHEN x = 24 THEN 'التنمية المستقبلية'
    END;