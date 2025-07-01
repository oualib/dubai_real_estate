"""
Simple tests for MAP functions.
"""

import pytest
from dubai_real_estate.connection.clients import BaseConnection
from dubai_real_estate.sql import get_function_sql


@pytest.mark.integration
def test_area_id(clickhouse_connection: BaseConnection):
    """Test area_id mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "area_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (284, "Jabal Ali", "جبل على"),
            (390, "Burj Khalifa", "برج خليفة"),
            (526, "Business Bay", "الخليج التجارى"),
            (999, None, None),  # Unknown
        ]

        for area_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_AREA_NAME_EN({area_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_AREA_NAME_AR({area_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_activity_type(clickhouse_connection: BaseConnection):
    """Test activity_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "activity_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (
                1,
                "Real Estate Buying & Selling Brokerage",
                "شراء الأراضي و العقارات و بيعها",
            ),
            (9, "Real Estate Development", "التطوير العقاري"),
            (14, "Shopping Mall", "مركز تسوق"),
            (26, "Real Estate Valuation Services", "خدمات تثمين العقارات"),
            (34, "Real Estate Consultancy", "الاستشارات العقارية"),
            (999, None, None),  # Unknown
        ]

        for activity_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_ACTIVITY_TYPE_EN({activity_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_ACTIVITY_TYPE_AR({activity_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_service(clickhouse_connection: BaseConnection):
    """Test service mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "service_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (6, "Vehicles Advertisement", "إعلانات المركبات"),
            (8, "Inside Dubai", "داخل دبي"),
            (11, "Newspaper Advertisement", "اعلانات الصحف"),
            (16, "Real Estate Promotional Stand", "منصة ترويج عقاري"),
            (31, "Advertisement by SMS", "تصاريح رسائل نصيه"),
            (44, "Launching a real estate project", "حفل إطلاق مشروع"),
            (80, "Electronic Advertisement", "اعلانات الكترونية"),
            (130, "Open Day", "اليوم المفتوح"),
            (999, None, None),  # Unknown
        ]

        for service_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_SERVICE_EN({service_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_SERVICE_AR({service_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_rooms(clickhouse_connection: BaseConnection):
    """Test rooms mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "rooms_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases for MAP_ROOMS_EN and MAP_ROOMS_AR
        test_cases = [
            (0, "Studio", "أستوديو"),
            (1, "1 B/R", "غرفة و صالة"),
            (2, "2 B/R", "غرفتين و صالة"),
            (3, "3 B/R", "ثلاثة غرفة و صالة"),
            (17, "Shop | Store", "محل"),
            (23, "Bank | ATM", "مساحه صراف آلي"),
            (58, "Office", "مكتب"),
            (621, "Penthouse", "بينت هاوس"),
            (1003, "Open Land | Garden", "أرض فضاء"),
            (999, None, None),  # Unknown
        ]

        for room_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(f"SELECT MAP_ROOMS_EN({room_id})")
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(f"SELECT MAP_ROOMS_AR({room_id})")
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar

        # Test cases for MAP_ROOMS_REVERSE
        reverse_test_cases = [
            ("Studio", 0),
            ("1 B/R", 1),
            ("2 B/R", 2),
            ("3 B/R", 3),
            ("Warehouse", 13),
            ("Shop", 17),
            ("Office", 58),
            ("Penthouse", 621),
            ("Hotel", 68),
            ("Unknown Room Type", None),  # Unknown
        ]

        for room_name, expected_id in reverse_test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_ROOMS_REVERSE('{room_name}')"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_id


@pytest.mark.integration
def test_service_category(clickhouse_connection: BaseConnection):
    """Test service_category mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "service_category_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Services", "خدمات"),
            (2, "Maintenance", "صيانة"),
            (6, "Management Services", "خدمات الإدارة"),
            (7, "Insurance", "تأمين"),
            (9, "Income", "الإيرادات"),
            (12, "Reserved Fund", "الصندوق الاحتياطي"),
            (48540, "Unit A/C (Charges)", "وحدة A / C (الرسوم)"),
            (48570, "Parking", "موقف سيارات"),
            (999, None, None),  # Unknown
        ]

        for category_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_SERVICE_CATEGORY_EN({category_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_SERVICE_CATEGORY_AR({category_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_request_source(clickhouse_connection: BaseConnection):
    """Test request_source mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "request_source_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Dubai Land Department", "دائرة الاراضي والاملاك"),
            (
                3,
                "Real Estate Registration Trustees Offices",
                "مكاتب امين التسجيل العقاري",
            ),
            (4, "Real Estate Services Trustees Offices", "مكاتب امين الخدمات العقاري"),
            (5, "Real Estate Developers Offices", "مكاتب المطورين العقاريين"),
            (15, "Dubai REST Smart Application", "تطبيق دبي ريست"),
            (999, None, None),  # Unknown
        ]

        for source_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_REQUEST_SOURCE_EN({source_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_REQUEST_SOURCE_AR({source_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_property_usage(clickhouse_connection: BaseConnection):
    """Test property_usage mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "property_usage_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases for MAP_PROPERTY_USAGE_EN and MAP_PROPERTY_USAGE_AR
        test_cases = [
            (1, "Agriculture", "زراعة"),
            (2, "Commercial", "تجاري"),
            (5, "Hospitality", "ضيافة"),
            (6, "Industrial", "صناعي"),
            (8, "Industrial | Commercial | Residential", "صناعي |  تجاري | سكني"),
            (12, "Residential", "سكني"),
            (13, "Residential | Commercial", "سكني | تجاري"),
            (15, "Tourism", "منشأه سياحيه"),
            (999, None, None),  # Unknown
        ]

        for usage_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROPERTY_USAGE_EN({usage_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROPERTY_USAGE_AR({usage_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar

        # Test cases for MAP_PROPERTY_USAGE_REVERSE
        reverse_test_cases = [
            ("Agricultural", 0),
            ("Commercial", 2),
            ("Educational facility", 3),
            ("Hospitality", 5),
            ("Industrial", 6),
            ("Industrial / Commercial / Residential", 8),
            ("Multi Usage", 9),
            ("Residential", 12),
            ("Residential / Commercial", 13),
            ("Storage", 14),
            ("Unknown Usage", None),  # Unknown
        ]

        for usage_name, expected_id in reverse_test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROPERTY_USAGE_REVERSE('{usage_name}')"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_id


@pytest.mark.integration
def test_reg_type(clickhouse_connection: BaseConnection):
    """Test reg_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "reg_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (0, "Off-Plan Properties", "على الخارطة"),
            (1, "Existing Properties", "العقارات القائمة"),
            (999, None, None),  # Unknown
        ]

        for reg_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_REG_TYPE_EN({reg_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_REG_TYPE_AR({reg_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_property_type(clickhouse_connection: BaseConnection):
    """Test property_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "property_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Land", "ارض"),
            (2, "Building", "مبنى"),
            (3, "Unit", "وحدة"),
            (4, "Villa", "فيلا"),
            (999, None, None),  # Unknown
        ]

        for property_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROPERTY_TYPE_EN({property_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROPERTY_TYPE_AR({property_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_property_sub_type(clickhouse_connection: BaseConnection):
    """Test property_sub_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "property_sub_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Land", "أرض"),
            (4, "Villa", "فيلا"),
            (17, "Shopping Mall", "مركز تسوق"),
            (31, "Hotel", "فندق"),
            (60, "Flat", "شقه سكنيه"),
            (101, "Hotel Apartment", "شقة فندقية"),
            (454, "Residential | Residential Villa", "سكني | فيلا سكنية"),
            (589, "Commercial | Offices | Residential", "تجاري | مكاتب | سكني"),
            (999, None, None),  # Unknown
        ]

        for sub_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROPERTY_SUB_TYPE_EN({sub_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROPERTY_SUB_TYPE_AR({sub_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_project_status(clickhouse_connection: BaseConnection):
    """Test project_status mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "project_status_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases for MAP_PROJECT_STATUS_EN and MAP_PROJECT_STATUS_AR
        test_cases = [
            (0, "NOT STARTED", "تحت الانشاء"),
            (1, "PENDING", "قيد التسجيل"),
            (2, "ACTIVE", "فعال"),
            (3, "FINISHED", "منجز"),
            (999, None, None),  # Unknown
        ]

        for status_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROJECT_STATUS_EN({status_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROJECT_STATUS_AR({status_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar

        # Test cases for MAP_PROJECT_STATUS_REVERSE
        reverse_test_cases = [
            ("ACTIVE", 2),
            ("PENDING", 1),
            ("FINISHED", 3),
            ("NOT_STARTED", 0),
            ("CONDITIONAL_ACTIVATING", 0),
            ("FRIEZED", 1),
            ("STOPPED", 1),
            ("UNKNOWN_STATUS", None),  # Unknown
        ]

        for status_name, expected_id in reverse_test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROJECT_STATUS_REVERSE('{status_name}')"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_id


@pytest.mark.integration
def test_project_type(clickhouse_connection: BaseConnection):
    """Test project_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "project_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Normal", "عادي"),
            (2, "Infrastructure", "بنية تحتية"),
            (3, "Multiple", "متعدد"),
            (999, None, None),  # Unknown
        ]

        for project_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROJECT_TYPE_EN({project_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROJECT_TYPE_AR({project_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_project_classification(clickhouse_connection: BaseConnection):
    """Test project_classification mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "project_classification_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Buildings", "مباني"),
            (2, "Villas", "فلل"),
            (3, "Villa Complex", "مجمع فلل"),
            (999, None, None),  # Unknown
        ]

        for classification_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROJECT_CLASSIFICATION_EN({classification_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROJECT_CLASSIFICATION_AR({classification_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_procedure(clickhouse_connection: BaseConnection):
    """Test procedure mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "procedure_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Bestowal", "تسجيل منحة"),
            (11, "Sell", "بيع"),
            (13, "Mortgage Registration", "تسجيل رهن"),
            (27, "Ownership Transfer", "إنتقال ملكية"),
            (94, "Issue Ownership Certificate", "إصدار ملكية عقار"),
            (102, "Sell Pre-Registration", "بيع - تسجيل مبدئى"),
            (451, "Register Real Estate Broker", "تسجيل وسيط عقارى"),
            (900, "Tasken Application", "طــلب تسكين"),
            (999, None, None),  # Unknown
        ]

        for procedure_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROCEDURE_EN({procedure_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PROCEDURE_AR({procedure_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_permit_status(clickhouse_connection: BaseConnection):
    """Test permit_status mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "permit_status_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Pending", "في إنتظار الموافقه"),
            (2, "Pending For Payment", "في إنتظار الدفع"),
            (3, "Rejected", "رفض"),
            (4, "Cancelled", "ملغي"),
            (6, "Completed", "مكتملة"),
            (7, "Auto Approval", "موافقة الية"),
            (999, None, None),  # Unknown
        ]

        for status_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PERMIT_STATUS_EN({status_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PERMIT_STATUS_AR({status_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_nearest_landmark(clickhouse_connection: BaseConnection):
    """Test nearest_landmark mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "nearest_landmark_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases for MAP_NEAREST_LANDMARK_EN and MAP_NEAREST_LANDMARK_AR
        test_cases = [
            (0, "Al Makhtoum International Airport", "مطار آل مكتوم الدولي"),
            (1, "Burj Al Arab", "برج العرب"),
            (2, "Burj Khalifa", "برج خليفة"),
            (5, "Dubai International Airport", "مطار دبي الدولي"),
            (7, "Expo 2020 Site", "موقع إكسبو 2020"),
            (11, "Jabel Ali", "جبل علي"),
            (999, None, None),  # Unknown
        ]

        for landmark_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_LANDMARK_EN({landmark_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_LANDMARK_AR({landmark_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar

        # Test cases for MAP_NEAREST_LANDMARK_REVERSE
        reverse_test_cases = [
            ("Burj Al Arab", 1),
            ("Burj Khalifa", 2),
            ("Downtown Dubai", 3),
            ("Dubai International Airport", 5),
            ("Expo 2020 Site", 7),
            ("Global Village", 8),
            ("Unknown Landmark", None),  # Unknown
        ]

        for landmark_name, expected_id in reverse_test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_LANDMARK_REVERSE('{landmark_name}')"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_id


@pytest.mark.integration
def test_parking_allocation_type(clickhouse_connection: BaseConnection):
    """Test parking_allocation_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "parking_allocation_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Title", "عنوان"),
            (2, "EU", "هش"),
            (999, None, None),  # Unknown
        ]

        for allocation_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PARKING_ALLOCATION_TYPE_EN({allocation_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_PARKING_ALLOCATION_TYPE_AR({allocation_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_nearest_metro(clickhouse_connection: BaseConnection):
    """Test nearest_metro mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "nearest_metro_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases for MAP_NEAREST_METRO_EN and MAP_NEAREST_METRO_AR
        test_cases = [
            (0, "ADCB Metro Station", "محطة مترو بنك أبوظبي التجاري"),
            (16, "Buj Khalifa Dubai Mall Metro Station", "محطة مترو بوج خليفة دبي مول"),
            (18, "Business Bay Metro Station", "محطة مترو الخليج التجاري"),
            (24, "Dubai Marina", "مرسى دبي"),
            (27, "Emirates Towers Metro Station", "محطة مترو أبراج الإمارات"),
            (34, "Ibn Battuta Metro Station", "محطة مترو ابن بطوطة"),
            (47, "Palm Jumeirah", "نخلة جميرا"),
            (53, "Trade Centre Metro Station", "محطة مترو المركز التجاري"),
            (999, None, None),  # Unknown
        ]

        for metro_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_METRO_EN({metro_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_METRO_AR({metro_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar

        # Test cases for MAP_NEAREST_METRO_REVERSE
        reverse_test_cases = [
            ("ADCB Metro Station", 0),
            ("Business Bay Metro Station", 18),
            ("Dubai Marina", 24),
            ("Emirates Towers Metro Station", 27),
            ("Ibn Battuta Metro Station", 34),
            ("Palm Jumeirah", 47),
            ("Trade Centre Metro Station", 53),
            ("Unknown Metro", None),  # Unknown
        ]

        for metro_name, expected_id in reverse_test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_METRO_REVERSE('{metro_name}')"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_id


@pytest.mark.integration
def test_nearest_mall(clickhouse_connection: BaseConnection):
    """Test nearest_mall mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "nearest_mall_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases for MAP_NEAREST_MALL_EN and MAP_NEAREST_MALL_AR
        test_cases = [
            (0, "City Centre Mirdif", "سيتي سنتر مردف"),
            (1, "Dubai Mall", "مول دبي"),
            (2, "Ibn-e-Battuta Mall", "ابن بطوطة مول"),
            (3, "Mall of the Emirates", "مول الإمارات"),
            (4, "Marina Mall", "مارينا مول"),
            (999, None, None),  # Unknown
        ]

        for mall_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_MALL_EN({mall_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_MALL_AR({mall_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar

        # Test cases for MAP_NEAREST_MALL_REVERSE
        reverse_test_cases = [
            ("City Centre Mirdif", 0),
            ("Dubai Mall", 1),
            ("Ibn-e-Battuta Mall", 2),
            ("Mall of the Emirates", 3),
            ("Marina Mall", 4),
            ("Unknown Mall", None),  # Unknown
        ]

        for mall_name, expected_id in reverse_test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NEAREST_MALL_REVERSE('{mall_name}')"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_id


@pytest.mark.integration
def test_nationality(clickhouse_connection: BaseConnection):
    """Test nationality mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "nationality_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "United Arab Emirates", "الإمارات العربية المتحدة"),
            (6, "Saudi Arabia", "المملكة العربية السعودية"),
            (13, "Egypt", "مصر"),
            (21, "India", "الهند"),
            (22, "Pakistan", "باكستان"),
            (26, "United Kingdom", "المملكة المتحدة"),
            (31, "Canada", "كندا"),
            (64, "Philippines", "الفلبين"),
            (999, None, None),  # Unknown
        ]

        for nationality_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NATIONALITY_EN({nationality_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_NATIONALITY_AR({nationality_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_master_community(clickhouse_connection: BaseConnection):
    """Test master_community mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "master_community_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Palm Jumeirah", "نخلة الجميرا"),
            (34, "Dubai Marina", "مرسى دبي"),
            (35, "Burj Khalifa District", "منطقة برج خليفة"),
            (112, "Business Bay", "بزنس باي"),
            (
                124,
                "Jumeriah Beach Residence  - JBR",
                "جميرا بيتش ريزيدنس  - الجيه بي آر",
            ),
            (519, "Dubai Silicon Oasis", "واحة دبي للسيليكون"),
            (541, "DownTown Dubai", "داون تاون دبي"),
            (545, "Dubai Hills Estate", "دبي هيلز استيت,"),
            (999, None, None),  # Unknown
        ]

        for community_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_MASTER_COMMUNITY_EN({community_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_MASTER_COMMUNITY_AR({community_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_license_type(clickhouse_connection: BaseConnection):
    """Test license_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "license_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Commercial", "تجارية"),
            (2, "Industrial", "صناعية"),
            (3, "Professional", "مهنية"),
            (6, "Commercial Sole Proprietorship", "تجارية مؤسسة فردية"),
            (8, "Commercial Public Shareholding", "تجارية مساهمة عامة"),
            (9, "External License", "رخصة خارجية"),
            (5324699, "Services", "خدمات"),
            (999, None, None),  # Unknown
        ]

        for license_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LICENSE_TYPE_EN({license_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LICENSE_TYPE_AR({license_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_license_source(clickhouse_connection: BaseConnection):
    """Test license_source mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "license_source_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (-10, "Dubai Economic Department", "دائرة التنمية الاقتصادية"),
            (-40, "Real Estate Regulatory Authority", "مؤسسة التنظيم العقاري"),
            (70, "Dubai Government", "حكومه دبى"),
            (
                4341,
                "TECOM Investments Free Zone (LLC)",
                "تيكوم للإستثمارات منطقة حرة- ذ.م.م",
            ),
            (5073, "Jebel Ali Free Zone Authority", "سلطه المنطقه الحره لجبل على"),
            (4249418, "Trakheesi", "تراخيص"),
            (10686091, "Dubai World Central", "دبي ورلد سنترال"),
            (999, None, None),  # Unknown
        ]

        for source_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LICENSE_SOURCE_EN({source_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LICENSE_SOURCE_AR({source_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_license_source_dev(clickhouse_connection: BaseConnection):
    """Test license_source mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "license_source_dev_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "DED", "دائرة التنمية الاقتصادية"),
            (4, "Dubai South", "دبي ساوث"),
            (
                5,
                "Dubai International Airport Free-Zone Authority",
                "سلطة المنطقة الحرة لمطار دبي",
            ),
            (999, None, None),  # Unknown
        ]

        for source_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LICENSE_SOURCE_DEV_EN({source_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LICENSE_SOURCE_DEV_AR({source_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_legal_type(clickhouse_connection: BaseConnection):
    """Test legal_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "legal_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Business", "تجارية"),
            (3, "Professional", "مهنية"),
            (5, "Commercial", "تجارية انطلاق"),
            (6, "Commercial Sole Proprietorship", "تجارية مؤسسة فردية"),
            (8, "Public Company", "تجارية مساهمة عامة"),
            (5324699, "Services", "خدمات"),
            (999, None, None),  # Unknown
        ]

        for legal_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LEGAL_TYPE_EN({legal_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LEGAL_TYPE_AR({legal_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_legal_status(clickhouse_connection: BaseConnection):
    """Test legal_status mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "legal_status_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Off Shore", "قبالة الشاطئ"),
            (2, "Limited Responsibility", "مسؤولية محدودة"),
            (3, "Personal", "استخدام شخصي"),
            (3923325, "New Legal Status", "وضع قانوني جديد"),
            (4082201, "Public Contribution", "مساهمة عامة"),
            (999, None, None),  # Unknown
        ]

        for status_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LEGAL_STATUS_EN({status_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LEGAL_STATUS_AR({status_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_land_type(clickhouse_connection: BaseConnection):
    """Test land_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "land_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Residential", "سكنى"),
            (3, "Industrial", "صناعى"),
            (4, "Commercial", "تجارى"),
            (7, "Hospitality", "ضيافة"),
            (11, "Healthcare", "الرعاية الصحية"),
            (16, "Transportation", "مواصلات"),
            (18, "Future Development", "التنمية المستقبلية"),
            (999, None, None),  # Unknown
        ]

        for land_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LAND_TYPE_EN({land_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_LAND_TYPE_AR({land_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_escrow_agent(clickhouse_connection: BaseConnection):
    """Test escrow_agent mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "escrow_agent_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "DUBAI ISLAMIC BANK (PJSC)", "بنك دبي الاسلامي (شركة مساهمة عامة)"),
            (7, "EMIRATES NBD BANK (PJSC)", "بنك الإمارات دبي الوطني (ش.م.ع)"),
            (19, "FIRST ABU DHABI BANK (PJSC)", "بنك أبوظبي الأول ش.م.ع."),
            (33, "MASHREQ BANK (PJSC)", "بنك المشرق (شركة مساهمة عامة)"),
            (41, "AJMAN BANK (PJSC)", "مصرف عجمان/ ش.م.ع"),
            (12763214, "INVESTMENT BANK (PJSC)", "بنك الاستثمار - ش.م.ع"),
            (999, None, None),  # Unknown
        ]

        for agent_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_ESCROW_AGENT_EN({agent_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_ESCROW_AGENT_AR({agent_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_ejari_bus_property_type(clickhouse_connection: BaseConnection):
    """Test ejari_bus_property_type mapping function."""
    # Read and format SQL
    sql = get_function_sql("MAP", "ejari_bus_property_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            (0, 1),
            (1, 2),
            (2, 3),
            (5, 5),  # Unchanged value
            (999, 999),  # Unchanged value
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_EJARI_BUS_PROPERTY_TYPE({input_val})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_ejari_property_type(clickhouse_connection: BaseConnection):
    """Test ejari_property_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "ejari_property_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Shop", "محل"),
            (2, "Office", "مكتب"),
            (841, "Villa", "فيلا"),
            (842, "Flat", "شقه"),
            (24, "Hotel", "فندق"),
            (28, "Petrol Station", "محطه وقود"),
            (280946546, "Supermarket", "سوبر ماركت"),
            (999, None, None),  # Unknown
        ]

        for property_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_EJARI_PROPERTY_TYPE_EN({property_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_EJARI_PROPERTY_TYPE_AR({property_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_contract_reg_type(clickhouse_connection: BaseConnection):
    """Test contract_reg_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "contract_reg_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "New", "جديد"),
            (2, "Renew", "تجديد"),
            (999, None, None),  # Unknown
        ]

        for contract_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_CONTRACT_REG_TYPE_EN({contract_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_CONTRACT_REG_TYPE_AR({contract_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_application(clickhouse_connection: BaseConnection):
    """Test application mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "application_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (2, "RT", "أمين التسجيل"),
            (4, "TABU", "الطابو"),
            (5, "DSR", "التسجيل الذاتى للمطورين"),
            (25, "Taskeen", "تاسكين"),
            (40, "TABU Smart Services", "الطابو"),
            (999, None, None),  # Unknown
        ]

        for app_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_APPLICATION_EN({app_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_APPLICATION_AR({app_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_status(clickhouse_connection: BaseConnection):
    """Test status mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "status_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (0, "Active", "سارية"),
            (2, "Under Transaction", "قيد الإجراء"),
            (3, "Frozen", "موقوفة"),
            (7, "Under Admin Cancellation", "قيد الالغاء الاداري"),
            (8, "Liquidated", "تصفية"),
            (9, "Cancelled", "ملغاة"),
            (999, None, None),  # Unknown
        ]

        for status_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(f"SELECT MAP_STATUS_EN({status_id})")
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(f"SELECT MAP_STATUS_AR({status_id})")
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_zoning_authority(clickhouse_connection: BaseConnection):
    """Test zoning_authority mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "zoning_authority_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Dubai Municipality", "بلدية دبي"),
            (2, "Dubai Development Authority (DDA)", "سلطة دبي للتطوير"),
            (3, "Dubai Silicon Oasis Authority", "سلطة واحة دبي للسيليكون"),
            (4, "Trakheesi", "تراخيص"),
            (5, "Dubai South", "دبي للجنوب"),
            (999, None, None),  # Unknown
        ]

        for authority_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_ZONING_AUTHORITY_EN({authority_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_ZONING_AUTHORITY_AR({authority_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_usage(clickhouse_connection: BaseConnection):
    """Test usage mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "usage_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Residential", "سكني"),
            (2, "Offices", "تجاري"),
            (3, "Mixed", "مختلط"),
            (5, "Parking", "وقوف السيارات"),
            (9, "Education", "تعليم"),
            (13, "Hospitality", "ضيافة"),
            (17, "Healthcare", "الرعاية الصحية"),
            (24, "Future Development", "التنمية المستقبلية"),
            (999, None, None),  # Unknown
        ]

        for usage_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(f"SELECT MAP_USAGE_EN({usage_id})")
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(f"SELECT MAP_USAGE_AR({usage_id})")
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_trans_group(clickhouse_connection: BaseConnection):
    """Test trans_group mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "trans_group_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (1, "Sales", "مبايعات"),
            (2, "Mortgages", "رهون"),
            (3, "Gifts", "هبات"),
            (999, None, None),  # Unknown
        ]

        for trans_group_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_TRANS_GROUP_EN({trans_group_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_TRANS_GROUP_AR({trans_group_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar


@pytest.mark.integration
def test_tenant_type(clickhouse_connection: BaseConnection):
    """Test tenant_type mapping functions."""
    # Read and format SQL
    sql = get_function_sql("MAP", "tenant_type_id")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_en, expected_ar)
        test_cases = [
            (0, "Person", "شخص"),
            (1, "Authority", "جهة"),
            (999, None, None),  # Unknown
        ]

        for tenant_type_id, expected_en, expected_ar in test_cases:
            # Test English function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_TENANT_TYPE_EN({tenant_type_id})"
            )
            en_result = cursor.fetchone()[0]
            cursor.close()

            # Test Arabic function
            cursor = clickhouse_connection.execute(
                f"SELECT MAP_TENANT_TYPE_AR({tenant_type_id})"
            )
            ar_result = cursor.fetchone()[0]
            cursor.close()

            assert en_result == expected_en
            assert ar_result == expected_ar
