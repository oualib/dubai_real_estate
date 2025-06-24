CREATE OR REPLACE FUNCTION MAP_PERMIT_STATUS_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'Pending'
        WHEN x = 2 THEN 'Pending For Payment'
        WHEN x = 3 THEN 'Rejected'
        WHEN x = 4 THEN 'Cancelled'
        WHEN x = 6 THEN 'Completed'
        WHEN x = 7 THEN 'Auto Approval'
    END;

CREATE OR REPLACE FUNCTION MAP_PERMIT_STATUS_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'في إنتظار الموافقه'
        WHEN x = 2 THEN 'في إنتظار الدفع'
        WHEN x = 3 THEN 'رفض'
        WHEN x = 4 THEN 'ملغي'
        WHEN x = 6 THEN 'مكتملة'
        WHEN x = 7 THEN 'موافقة الية'
    END;