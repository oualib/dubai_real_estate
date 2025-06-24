CREATE OR REPLACE FUNCTION MAP_PROJECT_STATUS_REVERSE AS (x) ->
    CASE 
        WHEN x = 'ACTIVE'                 THEN 2
        WHEN x = 'PENDING'                THEN 1
        WHEN x = 'FINISHED'               THEN 3
        WHEN x = 'NOT_STARTED'            THEN 0
        WHEN x = 'CONDITIONAL_ACTIVATING' THEN 0
        WHEN x = 'FRIEZED'                THEN 1
        WHEN x = 'STOPPED'                THEN 1
    END;

CREATE OR REPLACE FUNCTION MAP_PROJECT_STATUS_EN AS (x) ->
    CASE 
        WHEN x = 0 THEN 'NOT STARTED'
        WHEN x = 1 THEN 'PENDING'
        WHEN x = 2 THEN 'ACTIVE'
        WHEN x = 3 THEN 'FINISHED'
    END;

CREATE OR REPLACE FUNCTION MAP_PROJECT_STATUS_AR AS (x) ->
    CASE 
        WHEN x = 0 THEN 'تحت الانشاء'
        WHEN x = 1 THEN 'قيد التسجيل'
        WHEN x = 2 THEN 'فعال'
        WHEN x = 3 THEN 'منجز'
    END;