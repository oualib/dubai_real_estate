CREATE OR REPLACE FUNCTION MAP_ZONING_AUTHORITY_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'Dubai Municipality'
        WHEN x = 2 THEN 'Dubai Development Authority (DDA)'
        WHEN x = 3 THEN 'Dubai Silicon Oasis Authority'
        WHEN x = 4 THEN 'Trakheesi'
        WHEN x = 5 THEN 'Dubai South'
    END;

CREATE OR REPLACE FUNCTION MAP_ZONING_AUTHORITY_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'بلدية دبي'
        WHEN x = 2 THEN 'سلطة دبي للتطوير'
        WHEN x = 3 THEN 'سلطة واحة دبي للسيليكون'
        WHEN x = 4 THEN 'تراخيص'
        WHEN x = 5 THEN 'دبي للجنوب'
    END;