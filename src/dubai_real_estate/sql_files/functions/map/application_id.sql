CREATE OR REPLACE FUNCTION MAP_APPLICATION_EN AS (x) ->
    CASE 
        WHEN x = 2   THEN 'RT'
        WHEN x = 3   THEN 'Emart'
        WHEN x = 4   THEN 'TABU'
        WHEN x = 5   THEN 'DSR'
        WHEN x = 18  THEN 'Property Trustee'
        WHEN x = 25  THEN 'Taskeen'
        WHEN x = 26  THEN 'Property Survey'
        WHEN x = 40  THEN 'TABU Smart Services'
    END;

CREATE OR REPLACE FUNCTION MAP_APPLICATION_AR AS (x) ->
    CASE 
        WHEN x = 2   THEN 'أمين التسجيل'
        WHEN x = 3   THEN 'ايمارت'
        WHEN x = 4   THEN 'الطابو'
        WHEN x = 5   THEN 'التسجيل الذاتى للمطورين'
        WHEN x = 18  THEN 'الامين العقاري'
        WHEN x = 25  THEN 'تاسكين'
        WHEN x = 26  THEN 'مسح الممتلكات'
        WHEN x = 40  THEN 'الطابو'
    END;