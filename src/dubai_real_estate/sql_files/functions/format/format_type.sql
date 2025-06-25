CREATE OR REPLACE FUNCTION FORMAT_BOOL AS (x) ->
    CASE 
        WHEN LOWER(TRIM(x)) IN ('f', 'false', '0')
        THEN False
        WHEN LOWER(TRIM(x)) IN ('t', 'true', '1')
        THEN True
    END;

CREATE OR REPLACE FUNCTION FORMAT_DATE_0 AS (x) -> parseDateTimeOrNull(x, '%d-%m-%Y')::Nullable(Date);

CREATE OR REPLACE FUNCTION FORMAT_DATE_1 AS (x) -> CASE WHEN YEAR(x) > 1970 THEN x END;

CREATE OR REPLACE FUNCTION FORMAT_DATE AS (x) -> FORMAT_DATE_1(FORMAT_DATE_0(x));

CREATE OR REPLACE FUNCTION FORMAT_DATE_SLASH AS (x) -> parseDateTimeOrNull(x, '%m/%d/%Y %H:%i:%s')::Nullable(Date);

CREATE OR REPLACE FUNCTION FORMAT_PHONE_NUMBER_VARCHAR AS (x) ->
    CASE WHEN LENGTH(REGEXP_REPLACE(x, '[^0-9]', '')) BETWEEN 8 AND 14
        AND LENGTH(REGEXP_REPLACE(x, '[^0-9]', '')) <> LENGTH(REGEXP_REPLACE(x, '[^0]', ''))
    THEN CASE WHEN SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 1, 6) IN ('009710', '971971')
            THEN '971' || SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 7)
            WHEN SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 1, 5) IN ('00971', '09710')
            THEN '971' || SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 6)
            WHEN SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 1, 4) IN ('9710', '0971')
            THEN '971' || SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 5)
            WHEN LENGTH(REGEXP_REPLACE(x, '[^0-9]', '')) > 12 
                    AND SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 1, 6) IN ('971404')
            THEN '9714' || SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 7)
            WHEN SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 1, 4) IN ('4971')
            THEN '9714' || SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 5)
            WHEN SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 1, 1) IN ('0')
            THEN '971' || SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 2)
            WHEN SUBSTR(REGEXP_REPLACE(x, '[^0-9]', ''), 1, 3) NOT IN ('971')
            THEN '971' || REGEXP_REPLACE(x, '[^0-9]', '')
            ELSE REGEXP_REPLACE(x, '[^0-9]', '') 
        END END;

CREATE OR REPLACE FUNCTION FORMAT_PHONE_NUMBER AS (x) -> toUInt64OrNull(FORMAT_PHONE_NUMBER_VARCHAR(x));


CREATE OR REPLACE FUNCTION FORMAT_VARCHAR AS (x) ->
    CASE 
        WHEN LENGTH(REGEXP_REPLACE(x, '\s', '')) <> 0 AND LOWER(REGEXP_REPLACE(x, '\s', '')) NOT IN ('null', 'none')
        THEN TRIM(x)
    END;


CREATE OR REPLACE FUNCTION FORMAT_INT_0 AS (x) ->
    CASE
        WHEN LENGTH(REGEXP_REPLACE(x, '[^0-9+-]', '')) > 0
        THEN REGEXP_REPLACE(FORMAT_VARCHAR(x), '[^0-9+-]', '')
    END;

CREATE OR REPLACE FUNCTION FORMAT_INT_1 AS (x) ->
    CASE
        WHEN SUBSTR(x, 1, 1) NOT IN ('-', '+') OR LENGTH(x) > 1
        THEN x
    END;

CREATE OR REPLACE FUNCTION FORMAT_INT AS (x) -> FORMAT_INT_1(FORMAT_INT_0(x))::Nullable(Int128);


CREATE OR REPLACE FUNCTION FORMAT_LICENSE AS (x) ->
    CASE
        WHEN LENGTH(REGEXP_REPLACE(x, '[^0-9]', '')) > 1
        THEN REGEXP_REPLACE(FORMAT_VARCHAR(x), '[^0-9]', '')::Nullable(Int128)
    END;

CREATE OR REPLACE FUNCTION EXTRACT_LICENSE_TYPE AS (x) ->
    CASE
        WHEN FORMAT_LICENSE(x) IS NOT NULL
        THEN
            CASE
                WHEN UPPER(x) LIKE '%O%F%' OR UPPER(x) LIKE '%ا%' OR UPPER(x) LIKE '%ف%'
                THEN 'OF'
                WHEN UPPER(x) LIKE '%J%L%T%'
                THEN 'JLT'
                WHEN UPPER(x) LIKE '%D%M%C%C%'
                THEN 'DMCC'
                WHEN UPPER(x) LIKE '%C%N%'
                THEN 'CN'
                WHEN UPPER(x) LIKE '%L%C%'
                THEN 'LC'
                WHEN UPPER(x) LIKE 'F%'
                THEN 'F'
                WHEN UPPER(x) LIKE 'A%'
                THEN 'A'
            END
    END;


CREATE OR REPLACE FUNCTION FORMAT_FLOAT AS (x) ->
    CASE
        WHEN LENGTH(REGEXP_REPLACE(x, '[^0-9eE+-.]', '')) > 0
        THEN REGEXP_REPLACE(FORMAT_VARCHAR(x), '[^0-9eE+-.]', '')::Nullable(Float)
    END;


CREATE OR REPLACE FUNCTION FORMAT_WEBSITE_0 AS (x) ->
    CASE
        WHEN LENGTH(TRIM(x)) > 0 AND TRIM(x) NOT LIKE '%@%'
        THEN
            CASE
                WHEN LOWER(TRIM(x)) LIKE 'www.%.%'
                THEN LOWER(TRIM(x))
                WHEN LOWER(TRIM(x)) LIKE '%https://%' AND LOWER(TRIM(x)) NOT LIKE '%www.%'
                THEN REPLACE(LOWER(TRIM(x)), 'https://', 'www.')
                WHEN LOWER(TRIM(x)) LIKE '%http://%' AND LOWER(TRIM(x)) NOT LIKE '%www.%'
                THEN REPLACE(LOWER(TRIM(x)), 'http://', 'www.')
                WHEN LOWER(TRIM(x)) LIKE '%https://www.%'
                THEN REPLACE(LOWER(TRIM(x)), 'https://', '')
                WHEN LOWER(TRIM(x)) LIKE '%http://www.%'
                THEN REPLACE(LOWER(TRIM(x)), 'http://', '')
            END
    END;

CREATE OR REPLACE FUNCTION FORMAT_WEBSITE_1 AS (x) ->
    CASE
        WHEN x LIKE '%/'
        THEN SUBSTR(x, 1, LENGTH(x) - 1)
        ELSE x
    END;

CREATE OR REPLACE FUNCTION FORMAT_WEBSITE AS (x) -> FORMAT_WEBSITE_1(FORMAT_WEBSITE_0(x));


CREATE OR REPLACE FUNCTION FORMAT_EMAIL AS (x) ->
    CASE
        WHEN FORMAT_WEBSITE(x) IS NULL AND x LIKE '%@%'
        THEN LOWER(TRIM(REGEXP_REPLACE(x, '[^a-zA-Z0-9@.-]', '')))
    END;


CREATE OR REPLACE FUNCTION FORMAT_NAME_0 AS (x) ->
    CASE
        WHEN FORMAT_WEBSITE(x) IS NULL AND FORMAT_EMAIL(x) IS NULL AND FORMAT_PHONE_NUMBER(x) IS NULL
        THEN
            CASE 
                WHEN LOWER(x) LIKE '%l.l.c%'
                THEN REPLACE(INITCAP(TRIM(REPLACE(REPLACE(REPLACE(LOWER(x), '-', ''), 'l.l.c', 'LLC'), 'l l c', 'LLC'))), 'Llc', 'LLC')
                ELSE INITCAP(TRIM(x))
            END
    END;

CREATE OR REPLACE FUNCTION FORMAT_NAME_1 AS (x) ->
    CASE
        WHEN x LIKE '%.'
        THEN FORMAT_VARCHAR(SUBSTR(x, 1, LENGTH(x) - 1))
        ELSE FORMAT_VARCHAR(REPLACE(REPLACE(REPLACE(x, 'LLC.', 'LLC'), 'L L C', 'LLC'), 'Llc', 'LLC'))
    END;

CREATE OR REPLACE FUNCTION FORMAT_NAME AS (x) -> FORMAT_VARCHAR(REGEXP_REPLACE(FORMAT_NAME_1(FORMAT_NAME_0(x)), '[0-9-]', ''));


CREATE OR REPLACE FUNCTION FORMAT_CONTRACT_TYPE AS (x) -> FORMAT_VARCHAR(UPPER(TRIM(REGEXP_REPLACE(x, '[^a-zA-Z]', ''))));