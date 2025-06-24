CREATE OR REPLACE FUNCTION MAP_LAND_TYPE_EN AS (x) ->
    CASE 
        WHEN x = 1  THEN 'Residential'
        WHEN x = 2  THEN 'Agricultural'
        WHEN x = 3  THEN 'Industrial'
        WHEN x = 4  THEN 'Commercial'
        WHEN x = 5  THEN 'Public Facilities'
        WHEN x = 6  THEN 'Government Authorities'
        WHEN x = 7  THEN 'Hospitality'
        WHEN x = 8  THEN 'Public Facilities'
        WHEN x = 9  THEN 'Educational'
        WHEN x = 10 THEN 'Facilities'
        WHEN x = 11 THEN 'Healthcare'
        WHEN x = 12 THEN 'Recreational'
        WHEN x = 13 THEN 'Open Space'
        WHEN x = 15 THEN 'Utility'
        WHEN x = 16 THEN 'Transportation'
        WHEN x = 18 THEN 'Future Development'
    END;

CREATE OR REPLACE FUNCTION MAP_LAND_TYPE_AR AS (x) ->
    CASE
        WHEN x = 1  THEN 'سكنى'
        WHEN x = 2  THEN 'زراعى'
        WHEN x = 3  THEN 'صناعى'
        WHEN x = 4  THEN 'تجارى'
        WHEN x = 5  THEN 'مرافق عامة'
        WHEN x = 6  THEN 'مؤسسات حكومية'
        WHEN x = 7  THEN 'ضيافة'
        WHEN x = 8  THEN 'مرافق عامة'
        WHEN x = 9  THEN 'التعليمية'
        WHEN x = 10 THEN 'مرافق'
        WHEN x = 11 THEN 'الرعاية الصحية'
        WHEN x = 12 THEN 'ترفيهية'
        WHEN x = 13 THEN 'الفضاء المفتوح'
        WHEN x = 15 THEN 'جدوى'
        WHEN x = 16 THEN 'مواصلات'
        WHEN x = 18 THEN 'التنمية المستقبلية'
    END;