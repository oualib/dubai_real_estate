CREATE OR REPLACE FUNCTION MAP_PROCEDURE_EN AS (x) ->
    CASE
        WHEN x = 1   THEN 'Bestowal'
        WHEN x = 2   THEN 'Property Annexation'
        WHEN x = 3   THEN 'Property Cut Off'
        WHEN x = 4   THEN 'Adding Land By Sell'
        WHEN x = 5   THEN 'Property Cease'
        WHEN x = 6   THEN 'Compensate With Land'
        WHEN x = 7   THEN 'Compensate With Money'
        WHEN x = 8   THEN 'Proof of Ownership'
        WHEN x = 9   THEN 'Grant'
        WHEN x = 11  THEN 'Sell'
        WHEN x = 13  THEN 'Mortgage Registration'
        WHEN x = 14  THEN 'Modify Mortgage'
        WHEN x = 15  THEN 'Mortgage Release'
        WHEN x = 16  THEN 'Heirs Ownership'
        WHEN x = 17  THEN 'Convert Property to Partial Deed'
        WHEN x = 18  THEN 'Ownership Change'
        WHEN x = 19  THEN 'Issuing Losses | Damaged Recompense'
        WHEN x = 20  THEN 'Map Issuing'
        WHEN x = 22  THEN 'Area Name Change'
        WHEN x = 23  THEN 'Owners Cut Off'
        WHEN x = 24  THEN 'Property Evaluation'
        WHEN x = 26  THEN 'Owners Division'
        WHEN x = 27  THEN 'Ownership Transfer'
        WHEN x = 28  THEN 'Properties Exchange'
        WHEN x = 32  THEN 'Lease to Own Modify'
        WHEN x = 33  THEN 'Lease to Own Release'
        WHEN x = 36  THEN 'Development Release'
        WHEN x = 37  THEN 'Lease to Own Transfer'
        WHEN x = 39  THEN 'Development Mortgage'
        WHEN x = 41  THEN 'Delayed Sell'
        WHEN x = 43  THEN 'Portfolio Mortgage Registration'
        WHEN x = 44  THEN 'Mortgage Transfer'
        WHEN x = 45  THEN 'Sell Development'
        WHEN x = 49  THEN 'Portfolio Mortgage Modification'
        WHEN x = 56  THEN 'Modify Development Mortgage'
        WHEN x = 57  THEN 'Transfer Development Mortgage'
        WHEN x = 59  THEN 'Grant Development'
        WHEN x = 60  THEN 'Delayed Portfolio Mortgage'
        WHEN x = 93  THEN 'Delayed Sell Development'
        WHEN x = 94  THEN 'Issue Ownership Certificate'
        WHEN x = 95  THEN 'Delayed Development'
        WHEN x = 98  THEN 'Complete Delayed Development'
        WHEN x = 101 THEN 'Portfolio Mortgage Registration Pre-Registration'
        WHEN x = 102 THEN 'Sell Pre-Registration'
        WHEN x = 103 THEN 'Lease to Own Transfer Pre-Registration'
        WHEN x = 104 THEN 'Lease to Own Modify Pre-Registration'
        WHEN x = 105 THEN 'Mortgage Pre-Registration'
        WHEN x = 107 THEN 'Lease to Own Registration Pre-Registration'
        WHEN x = 108 THEN 'Modify Mortgage Pre-Registration'
        WHEN x = 110 THEN 'Lease to Own Registration'
        WHEN x = 111 THEN 'Portfolio Mortgage Transfer'
        WHEN x = 113 THEN 'Mortgage Transfer Pre-Registration'
        WHEN x = 115 THEN 'Complete Delayed Sell'
        WHEN x = 120 THEN 'Grant Pre-Registration'
        WHEN x = 130 THEN 'Modify Development'
        WHEN x = 133 THEN 'Development Registration'
        WHEN x = 135 THEN 'Portfolio Mortgage Modification Pre-Registration'
        WHEN x = 136 THEN 'Development Transfer'
        WHEN x = 137 THEN 'Portfolio Mortgage Transfer Pre-Registration'
        WHEN x = 140 THEN 'Transfeer From Development to Free OwenrShip'
        WHEN x = 150 THEN 'Portfolio Development Registration'
        WHEN x = 151 THEN 'Portfolio Mortgage Development Registration'
        WHEN x = 152 THEN 'Portfolio Mortgage Development Modification'
        WHEN x = 190 THEN 'Delayed Mortgage'
        WHEN x = 191 THEN 'Modify Delayed Mortgage'
        WHEN x = 192 THEN 'Transfer Delayed Mortgage'
        WHEN x = 207 THEN 'Complete Bestowal'
        WHEN x = 213 THEN 'Delayed Property Cut Off'
        WHEN x = 214 THEN 'Property Evaluation External'
        WHEN x = 216 THEN 'Delayed Property Annex'
        WHEN x = 219 THEN 'Grant on Delayed Sell'
        WHEN x = 361 THEN 'Delayed Lease to Own Registration'
        WHEN x = 362 THEN 'Delayed Lease to Own Modify'
        WHEN x = 363 THEN 'Delayed Lease to Own Transfer'
        WHEN x = 364 THEN 'Delayed Lease to Own Release'
        WHEN x = 365 THEN 'Delayed Lease to Own Continue'
        WHEN x = 371 THEN 'Lease Development Registration'
        WHEN x = 372 THEN 'Lease Development Modify'
        WHEN x = 373 THEN 'Lease Development Transfer'
        WHEN x = 374 THEN 'Lease Development Continue'
        WHEN x = 405 THEN 'Issue Real Estate Lost License'
        WHEN x = 451 THEN 'Register Real Estate Broker'
        WHEN x = 452 THEN 'Renew Real Estate Broker License'
        WHEN x = 458 THEN 'Bestowal Ownership'
        WHEN x = 460 THEN 'Sale On Payment Plan'
        WHEN x = 653 THEN 'Property Approval Procedure'
        WHEN x = 703 THEN 'Common Area Map Issue'
        WHEN x = 705 THEN 'Property Map Issue Volume'
        WHEN x = 706 THEN 'Common Part Map Issue'
        WHEN x = 715 THEN 'Delayed Sell Lease to Own Registration'
        WHEN x = 716 THEN 'Delayed Sell Lease To Own Modification'
        WHEN x = 717 THEN 'Delayed Sell Lease To Own Transfer'
        WHEN x = 718 THEN 'Delayed Sell Lease To Own Release'
        WHEN x = 810 THEN 'Lease Finance Registration'
        WHEN x = 811 THEN 'Lease Finance Modification'
        WHEN x = 812 THEN 'Lease Finance Release'
        WHEN x = 813 THEN 'Procedure Termination'
        WHEN x = 814 THEN 'Lease to Own on Development Registration'
        WHEN x = 815 THEN 'Lease to Own on Development Modification'
        WHEN x = 816 THEN 'Lease to Own on Development Transfer'
        WHEN x = 817 THEN 'Lease to Own on Development Release'
        WHEN x = 821 THEN 'Lease Finance Registration Leased Totally'
        WHEN x = 845 THEN 'Update Bulk Of Properties'
        WHEN x = 851 THEN 'Development Registration Pre-Registration'
        WHEN x = 852 THEN 'Sell Development Pre-Registration'
        WHEN x = 861 THEN 'Development Mortgage Pre-Registration'
        WHEN x = 900 THEN 'Tasken Application'
        WHEN x = 911 THEN 'Complete Lease To Own On Delayed Sell'
        WHEN x = 919 THEN 'Hold Share Sell'
        WHEN x = 928 THEN 'Companies Registration Investment Funds Procedure'
    END;

CREATE OR REPLACE FUNCTION MAP_PROCEDURE_AR AS (x) ->
    CASE
        WHEN x = 1   THEN 'تسجيل منحة'
        WHEN x = 2   THEN 'ضم عقار'
        WHEN x = 3   THEN 'فصل عقار'
        WHEN x = 4   THEN 'إضافة أرض بالبيع'
        WHEN x = 5   THEN 'الوقف'
        WHEN x = 6   THEN 'تعويض بأرض'
        WHEN x = 7   THEN 'تعويض مالى'
        WHEN x = 8   THEN 'إثبات تملك'
        WHEN x = 9   THEN 'هبه'
        WHEN x = 11  THEN 'بيع'
        WHEN x = 13  THEN 'تسجيل رهن'
        WHEN x = 14  THEN 'تعديل رهن'
        WHEN x = 15  THEN 'فك رهن'
        WHEN x = 16  THEN 'تسجيل ملكية الورثة'
        WHEN x = 17  THEN 'تحويل عقار إلي ملكية جزئية'
        WHEN x = 18  THEN 'تعديل بيانات ملكية'
        WHEN x = 19  THEN 'إصدار بدل فاقد/ تالف'
        WHEN x = 20  THEN 'إصدار خارطة'
        WHEN x = 22  THEN 'تغيير مسمى منطقه'
        WHEN x = 23  THEN 'فصل ملاك'
        WHEN x = 24  THEN 'تقييم عقار'
        WHEN x = 26  THEN 'قسمة شركاء'
        WHEN x = 27  THEN 'إنتقال ملكية'
        WHEN x = 28  THEN 'تبادل عقارين'
        WHEN x = 32  THEN 'تعديل إيجارة تنتهى بالتملك'
        WHEN x = 33  THEN 'فك إيجارة تنتهى بالتملك'
        WHEN x = 36  THEN 'انهاء حق منفعة'
        WHEN x = 37  THEN 'تحويل إيجارة تنتهى بالتملك'
        WHEN x = 39  THEN 'رهن حق منفعة'
        WHEN x = 41  THEN 'بيع مبدئى'
        WHEN x = 43  THEN 'تسجيل رهن محافظ'
        WHEN x = 44  THEN 'تحويل رهن'
        WHEN x = 45  THEN 'بيع حق منفعة'
        WHEN x = 49  THEN 'تعديل رهن محافظ'
        WHEN x = 56  THEN 'تعديل رهن حق منفعة'
        WHEN x = 57  THEN 'تحويل رهن حق منفعة'
        WHEN x = 59  THEN 'هبة حق المنفعة'
        WHEN x = 60  THEN 'رهن محافظ بيع مؤجل'
        WHEN x = 93  THEN 'بيع حق منفعة مؤجل'
        WHEN x = 94  THEN 'إصدار ملكية عقار'
        WHEN x = 95  THEN 'تسجيل حق منفعة مؤجل'
        WHEN x = 98  THEN 'استكمال حق منفعة مؤجل'
        WHEN x = 101 THEN 'تسجيل رهن محافظ - تسجيل مبدئى'
        WHEN x = 102 THEN 'بيع - تسجيل مبدئى'
        WHEN x = 103 THEN 'تحويل إيجارة تنتهى بالتملك - تسجيل مبدئى'
        WHEN x = 104 THEN 'تعديل إيجارة تنتهى بالتملك - تسجيل مبدئى'
        WHEN x = 105 THEN 'تسجيل رهن - تسجيل مبدئى'
        WHEN x = 107 THEN 'تسجيل إيجارة تنتهى بالتملك - تسجيل مبدئى'
        WHEN x = 108 THEN 'تعديل رهن - تسجيل مبدئي'
        WHEN x = 110 THEN 'تسجيل إيجارة تنتهى بالتملك'
        WHEN x = 111 THEN 'تحويل رهن محافظ'
        WHEN x = 113 THEN 'تحويل رهن- تسجيل مبدئي'
        WHEN x = 115 THEN 'إستكمال بيع مبدئى'
        WHEN x = 120 THEN 'هبه - تسجيل مبدئى'
        WHEN x = 130 THEN 'تعديل حق منفعة'
        WHEN x = 133 THEN 'تسجيل حق منفعة'
        WHEN x = 135 THEN 'تعديل رهن محافظ - تسجيل مبدئى'
        WHEN x = 136 THEN 'تحويل حق منفعة'
        WHEN x = 137 THEN 'تحويل رهن محافظ - تسجيل مبدئى'
        WHEN x = 140 THEN 'تحويل من حق منفعة إلي ملكية حره'
        WHEN x = 150 THEN 'تسجيل حق منفعة محافظ'
        WHEN x = 151 THEN 'تسجيل رهن حق منفعة محافظ'
        WHEN x = 152 THEN 'تعديل رهن حق منفعة محافظ'
        WHEN x = 190 THEN 'رهن بيع مبدئى'
        WHEN x = 191 THEN 'تعديل رهن بيع مبدئى'
        WHEN x = 192 THEN 'تحويل رهن بيع مبدئى'
        WHEN x = 207 THEN 'إستكمال تسجيل منحة'
        WHEN x = 213 THEN 'فصل عقار مؤجل'
        WHEN x = 214 THEN 'تقييم عقار غير مسجل'
        WHEN x = 216 THEN 'ضم عقار مؤجل'
        WHEN x = 219 THEN 'هبة على بيع مبدئى'
        WHEN x = 361 THEN 'تسجيل إيجارة تنتهى بالتملك المؤجل'
        WHEN x = 362 THEN 'تعديل إيجارة تنتهى بالتملك المؤجل'
        WHEN x = 363 THEN 'تحويل إيجارة تنتهى بالتملك المؤجل'
        WHEN x = 364 THEN 'فك إيجارة تنتهى بالتملك المؤجل'
        WHEN x = 365 THEN 'إستكمال إيجارة تنتهى بالتملك المؤجل'
        WHEN x = 371 THEN 'تسجيل حق منفعة بالاجارة'
        WHEN x = 372 THEN 'تعديل حق منفعة بالاجارة'
        WHEN x = 373 THEN 'تحويل حق منفعة بالاجارة'
        WHEN x = 374 THEN 'إستكمال حق منفعة بالاجارة'
        WHEN x = 405 THEN 'إصدار شهادة بدل فاقد لمكتب عقارى'
        WHEN x = 451 THEN 'تسجيل وسيط عقارى'
        WHEN x = 452 THEN 'تجديد وسيط عقارى'
        WHEN x = 458 THEN 'تمليك أرض منحة'
        WHEN x = 460 THEN 'بيع مقيد بسنوات الدفع'
        WHEN x = 653 THEN 'تصديق إجراء'
        WHEN x = 703 THEN 'إصدار خارطة المساحات المشتركه'
        WHEN x = 705 THEN 'إصدار خارطه حجميه'
        WHEN x = 706 THEN 'إصدار خارطه الأجزاء المشتركه'
        WHEN x = 715 THEN 'تسجيل إيجاره تنتهى بالتملك على بيع مبدئى'
        WHEN x = 716 THEN 'تعديل إيجاره تنتهى بالتملك على بيع مبدئى'
        WHEN x = 717 THEN 'تحويل إيجارة تنتهى بالتملك على بيع مبدئى'
        WHEN x = 718 THEN 'فك إيجاره تنتهى بالتملك على بيع مبدئى'
        WHEN x = 810 THEN 'تسجيل اجارة تمويلية'
        WHEN x = 811 THEN 'تعديل اجارة تمويلية'
        WHEN x = 812 THEN 'فك إيجارة تمويلية'
        WHEN x = 813 THEN 'إلغاء عقد'
        WHEN x = 814 THEN 'تسجيل إيجارة تنتهي بالتملك على حق منفعة'
        WHEN x = 815 THEN 'تعديل إيجارة تنتهي بالتملك على حق منفعة'
        WHEN x = 816 THEN 'تحويل إيجارة تنتهي بالتملك على حق منفعة'
        WHEN x = 817 THEN 'فك إيجارة تنتهي بالتملك على حق منفعة'
        WHEN x = 821 THEN 'تسجيل ايجارة تمويلية على حق منفعة'
        WHEN x = 845 THEN 'تعديل مجموعة عقارات'
        WHEN x = 851 THEN 'تسجيل حق منفعة - تسجيل مبدئي'
        WHEN x = 852 THEN 'بيع حق منفعة - تسجيل مبدئي'
        WHEN x = 861 THEN 'رهن حق منفعة تسجيل مبدئى'
        WHEN x = 900 THEN 'طــلب تسكين'
        WHEN x = 911 THEN 'استكمال بيع مبدئي مع إجارة تنتهي بالتملك'
        WHEN x = 919 THEN 'بيع حصص ملاك'
        WHEN x = 928 THEN 'إجراء تسجيل الشركات /الصناديق الإستثماريه'
    END;