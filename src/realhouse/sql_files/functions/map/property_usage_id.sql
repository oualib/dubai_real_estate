CREATE OR REPLACE FUNCTION MAP_PROPERTY_USAGE_REVERSE AS (x) ->
    CASE 
        WHEN x = 'Agricultural'                          THEN 0
        WHEN x = 'Agriculture'                           THEN 1
        WHEN x = 'Commercial'                            THEN 2
        WHEN x = 'Educational facility'                  THEN 3
        WHEN x = 'Health Facility'                       THEN 4
        WHEN x = 'Hospitality'                           THEN 5
        WHEN x = 'Industrial'                            THEN 6
        WHEN x = 'Industrial / Commercial'               THEN 7
        WHEN x = 'Industrial / Commercial / Residential' THEN 8
        WHEN x = 'Multi Usage'                           THEN 9
        WHEN x = 'Multi-Use'                             THEN 10
        WHEN x = 'Other'                                 THEN 11
        WHEN x = 'Residential'                           THEN 12
        WHEN x = 'Residential / Commercial'              THEN 13
        WHEN x = 'Storage'                               THEN 14
        WHEN x = 'Tourist origin'                        THEN 15
    END;

CREATE OR REPLACE FUNCTION MAP_PROPERTY_USAGE_EN AS (x) ->
    CASE 
        WHEN x = 0  THEN 'Agriculture'
        WHEN x = 1  THEN 'Agriculture'
        WHEN x = 2  THEN 'Commercial'
        WHEN x = 3  THEN 'Educational Facility'
        WHEN x = 4  THEN 'Health Facility'
        WHEN x = 5  THEN 'Hospitality'
        WHEN x = 6  THEN 'Industrial'
        WHEN x = 7  THEN 'Industrial | Commercial'
        WHEN x = 8  THEN 'Industrial | Commercial | Residential'
        WHEN x = 9  THEN 'Multi Usage'
        WHEN x = 10 THEN 'Multi Usage'
        WHEN x = 11 THEN 'Other'
        WHEN x = 12 THEN 'Residential'
        WHEN x = 13 THEN 'Residential | Commercial'
        WHEN x = 14 THEN 'Storage'
        WHEN x = 15 THEN 'Tourism'
    END;

CREATE OR REPLACE FUNCTION MAP_PROPERTY_USAGE_AR AS (x) ->
    CASE 
        WHEN x = 0  THEN 'زراعة'
        WHEN x = 1  THEN 'زراعة'
        WHEN x = 2  THEN 'تجاري'
        WHEN x = 3  THEN 'منشأه تعليميه'
        WHEN x = 4  THEN 'منشأه صحيه'
        WHEN x = 5  THEN 'ضيافة'
        WHEN x = 6  THEN 'صناعي'
        WHEN x = 7  THEN 'صناعي | تجاري'
        WHEN x = 8  THEN 'صناعي |  تجاري | سكني'
        WHEN x = 9  THEN 'متعدد الاستخدامات'
        WHEN x = 10 THEN 'متعدد الاستخدامات'
        WHEN x = 11 THEN 'أخرى'
        WHEN x = 12 THEN 'سكني'
        WHEN x = 13 THEN 'سكني | تجاري'
        WHEN x = 14 THEN 'تخزين'
        WHEN x = 15 THEN 'منشأه سياحيه'
    END;