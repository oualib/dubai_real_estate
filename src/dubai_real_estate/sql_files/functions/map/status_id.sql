CREATE OR REPLACE FUNCTION MAP_STATUS_EN AS (x) ->
    CASE 
        WHEN x = 0    THEN 'Active'
        WHEN x = 2    THEN 'Under Transaction'
        WHEN x = 3    THEN 'Frozen'
        WHEN x = 7    THEN 'Under Admin Cancellation'
        WHEN x = 8    THEN 'Liquidated'
        WHEN x = 9    THEN 'Cancelled'
    END;

CREATE OR REPLACE FUNCTION MAP_STATUS_AR AS (x) ->
    CASE
        WHEN x = 0    THEN 'سارية'
        WHEN x = 2    THEN 'قيد الإجراء'
        WHEN x = 3    THEN 'موقوفة'
        WHEN x = 7    THEN 'قيد الالغاء الاداري'
        WHEN x = 8    THEN 'تصفية'
        WHEN x = 9    THEN 'ملغاة'
    END;