
CREATE OR REPLACE FUNCTION MAP_LICENSE_SOURCE_DEV_EN AS (x) ->
    CASE 
        WHEN x = 1  THEN 'DED'
        WHEN x = 2  THEN 'Jebel Ali Free-Zone Authority'
        WHEN x = 3  THEN 'DMCC'
        WHEN x = 4  THEN 'Dubai South'
        WHEN x = 5  THEN 'Dubai International Airport Free-Zone Authority'
        WHEN x = 6  THEN 'Dubai Healthcare City Authority'
        WHEN x = 7  THEN 'Dubai Creative Cluster Authority'
        WHEN x = 9  THEN 'RAK Free-Zone Authority'
        WHEN x = 10 THEN 'Sharjah International Airport Free-Zone Authority'
        WHEN x = 13 THEN 'Dubai Silicon Oasis Authority'
        WHEN x = 14 THEN 'Ports, Customs and Free Zone Corporation'
        WHEN x = 15 THEN 'Meydan Freezone'
        WHEN x = 16 THEN 'Dubai World Trade Center Authority'
        WHEN x = 17 THEN 'Dubai Internet City'
        WHEN x = 19 THEN 'Sharjah Media City'
        WHEN x = 20 THEN 'Hamriyah Free Zone Authority'
        WHEN x = 25 THEN 'Umm Alquwain Free-Zone Authority'
        WHEN x = 26 THEN 'Dubai Development Authority'
        WHEN x = 27 THEN 'Others'
    END;

CREATE OR REPLACE FUNCTION MAP_LICENSE_SOURCE_DEV_AR AS (x) ->
    CASE 
        WHEN x = 1  THEN 'دائرة التنمية الاقتصادية'
        WHEN x = 2  THEN 'سلطة المنطقة الحرة لجبل علي'
        WHEN x = 3  THEN 'مركز دبي للسلع المتعددة'
        WHEN x = 4  THEN 'دبي ساوث'
        WHEN x = 5  THEN 'سلطة المنطقة الحرة لمطار دبي'
        WHEN x = 6  THEN 'سلطة مدينة دبي الطبية'
        WHEN x = 7  THEN 'سلطة دبي للمجمعات الابداعية - سابقا تيكوم'
        WHEN x = 9  THEN 'هيئة المنطقة الحرة برأس الخيمة'
        WHEN x = 10 THEN 'المنطقة الحرة لمطار الشارقة الدولي'
        WHEN x = 13 THEN 'سلطة واحة دبي للسيليكون'
        WHEN x = 14 THEN 'تراخيص :: مؤسسة الجمارك والموانئ والمنطقة الحرة الرئيسية'
        WHEN x = 15 THEN 'ميدان منطقة حرة'
        WHEN x = 16 THEN 'سلطة مركز دبي التجاري العالمي'
        WHEN x = 17 THEN 'مدينة دبي للانترنت و التكنولوجيا و الإعلام'
        WHEN x = 19 THEN 'مدينة الشارقة للأعلام'
        WHEN x = 20 THEN 'هيئة المنطقة الحرة بالحمرية'
        WHEN x = 25 THEN 'سلطة منطقة التجارة الحرة بأم القيوين'
        WHEN x = 26 THEN 'سلطة دبي للتطوير'
        WHEN x = 27 THEN 'أخرى'
    END;