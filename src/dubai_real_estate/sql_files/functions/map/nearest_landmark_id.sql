CREATE OR REPLACE FUNCTION MAP_NEAREST_LANDMARK_REVERSE AS (x) ->
	CASE 
		WHEN x = 'Al Makhtoum International Airport' THEN 0
		WHEN x = 'Burj Al Arab'                      THEN 1
		WHEN x = 'Burj Khalifa'                      THEN 2
		WHEN x = 'Downtown Dubai'                    THEN 3
		WHEN x = 'Dubai Cycling Course'              THEN 4
		WHEN x = 'Dubai International Airport'       THEN 5
		WHEN x = 'Dubai Parks and Resorts'           THEN 6
		WHEN x = 'Expo 2020 Site'                    THEN 7
		WHEN x = 'Global Village'                    THEN 8
		WHEN x = 'Hamdan Sports Complex'             THEN 9
		WHEN x = 'IMG World Adventures'              THEN 10
		WHEN x = 'Jabel Ali'                         THEN 11
		WHEN x = 'Motor City'                        THEN 12
		WHEN x = 'Sports City Swimming Academy'      THEN 13
	END;

CREATE OR REPLACE FUNCTION MAP_NEAREST_LANDMARK_EN AS (x) ->
	CASE 
		WHEN x = 0  THEN 'Al Makhtoum International Airport'
		WHEN x = 1  THEN 'Burj Al Arab'
		WHEN x = 2  THEN 'Burj Khalifa'
		WHEN x = 3  THEN 'Downtown Dubai'
		WHEN x = 4  THEN 'Dubai Cycling Course'
		WHEN x = 5  THEN 'Dubai International Airport'
		WHEN x = 6  THEN 'Dubai Parks and Resorts'
		WHEN x = 7  THEN 'Expo 2020 Site'
		WHEN x = 8  THEN 'Global Village'
		WHEN x = 9  THEN 'Hamdan Sports Complex'
		WHEN x = 10 THEN 'IMG World Adventures'
		WHEN x = 11 THEN 'Jabel Ali'
		WHEN x = 12 THEN 'Motor City'
		WHEN x = 13 THEN 'Sports City Swimming Academy'
	END;

CREATE OR REPLACE FUNCTION MAP_NEAREST_LANDMARK_AR AS (x) ->
	CASE 
		WHEN x = 0  THEN 'مطار آل مكتوم الدولي'
		WHEN x = 1  THEN 'برج العرب'
		WHEN x = 2  THEN 'برج خليفة'
		WHEN x = 3  THEN 'وسط مدينة دبي'
		WHEN x = 4  THEN 'دورة دبي للدراجات'
		WHEN x = 5  THEN 'مطار دبي الدولي'
		WHEN x = 6  THEN 'دبي باركس اند ريزورتس'
		WHEN x = 7  THEN 'موقع إكسبو 2020'
		WHEN x = 8  THEN 'قرية عالمية'
		WHEN x = 9  THEN 'مجمع حمدان الرياضي'
		WHEN x = 10 THEN 'آي إم جي وورلد أدفينتشرز'
		WHEN x = 11 THEN 'جبل علي'
		WHEN x = 12 THEN 'موتور سيتي'
		WHEN x = 13 THEN 'أكاديمية المدينة الرياضية للسباحة'
	END;