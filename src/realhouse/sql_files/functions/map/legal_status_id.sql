CREATE OR REPLACE FUNCTION MAP_LEGAL_STATUS_EN AS (x) ->
    CASE 
        WHEN x = 1       THEN 'Off Shore'
        WHEN x = 2       THEN 'Limited Responsibility'
        WHEN x = 3       THEN 'Personal'
        WHEN x = 3923325 THEN 'New Legal Status'
        WHEN x = 4082201 THEN 'Public Contribution'
    END;

CREATE OR REPLACE FUNCTION MAP_LEGAL_STATUS_AR AS (x) ->
    CASE 
        WHEN x = 1       THEN 'قبالة الشاطئ'
        WHEN x = 2       THEN 'مسؤولية محدودة'
        WHEN x = 3       THEN 'استخدام شخصي'
        WHEN x = 3923325 THEN 'وضع قانوني جديد'
        WHEN x = 4082201 THEN 'مساهمة عامة'
    END;