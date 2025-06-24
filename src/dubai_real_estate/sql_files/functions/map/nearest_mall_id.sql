CREATE OR REPLACE FUNCTION MAP_NEAREST_MALL_REVERSE AS (x) ->
    CASE 
        WHEN x = 'City Centre Mirdif'   THEN 0
        WHEN x = 'Dubai Mall'           THEN 1
        WHEN x = 'Ibn-e-Battuta Mall'   THEN 2
        WHEN x = 'Mall of the Emirates' THEN 3
        WHEN x = 'Marina Mall'          THEN 4
    END;

CREATE OR REPLACE FUNCTION MAP_NEAREST_MALL_EN AS (x) ->
    CASE 
        WHEN x = 0 THEN 'City Centre Mirdif'
        WHEN x = 1 THEN 'Dubai Mall'
        WHEN x = 2 THEN 'Ibn-e-Battuta Mall'
        WHEN x = 3 THEN 'Mall of the Emirates'
        WHEN x = 4 THEN 'Marina Mall'
    END;

CREATE OR REPLACE FUNCTION MAP_NEAREST_MALL_AR AS (x) ->
    CASE 
        WHEN x = 0 THEN 'سيتي سنتر مردف'
        WHEN x = 1 THEN 'مول دبي'
        WHEN x = 2 THEN 'ابن بطوطة مول'
        WHEN x = 3 THEN 'مول الإمارات'
        WHEN x = 4 THEN 'مارينا مول'
    END;