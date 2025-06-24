CREATE OR REPLACE FUNCTION MAP_LICENSE_TYPE_EN AS (x) ->
    CASE 
        WHEN x = 1       THEN 'Commercial'
        WHEN x = 2       THEN 'Industrial'
        WHEN x = 3       THEN 'Professional'
        WHEN x = 5       THEN 'Commercial Launch'
        WHEN x = 6       THEN 'Commercial Sole Proprietorship'
        WHEN x = 7       THEN 'Private Joint Stock Business'
        WHEN x = 8       THEN 'Commercial Public Shareholding'
        WHEN x = 9       THEN 'External License'
        WHEN x = 5324699 THEN 'Services'
    END;

CREATE OR REPLACE FUNCTION MAP_LICENSE_TYPE_AR AS (x) ->
    CASE 
        WHEN x = 1       THEN 'تجارية'
        WHEN x = 2       THEN 'صناعية'
        WHEN x = 3       THEN 'مهنية'
        WHEN x = 5       THEN 'تجارية انطلاق'
        WHEN x = 6       THEN 'تجارية مؤسسة فردية'
        WHEN x = 7       THEN 'تجارية مساهمة خاصة'
        WHEN x = 8       THEN 'تجارية مساهمة عامة'
        WHEN x = 9       THEN 'رخصة خارجية'
        WHEN x = 5324699 THEN 'خدمات'
    END;