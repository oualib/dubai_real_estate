CREATE OR REPLACE FUNCTION IS_EN AS (x) -> LENGTH(REGEXP_REPLACE(x, '[^A-Za-z]', '')) > 0;

CREATE OR REPLACE FUNCTION FIRST_EN AS (x, y, z) ->
    CASE
        WHEN IS_EN(x) THEN x
        WHEN IS_EN(y) THEN y
        WHEN IS_EN(z) THEN z
    END;

CREATE OR REPLACE FUNCTION FIRST_AR AS (x, y, z) ->
    CASE
        WHEN NOT(IS_EN(x)) THEN x
        WHEN NOT(IS_EN(y)) THEN y
        WHEN NOT(IS_EN(z)) THEN z
    END;