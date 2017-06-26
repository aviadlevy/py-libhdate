import pytest
import hdate
import hdate.hdate_julian as hj

import datetime
import random


HEBREW_YEARS_INFO = {
    # year, dow rosh hashana, length, dow pesach
    5753: (2, 353, 3), 5773: (2, 353, 3), 5777: (2, 353, 3),
    5756: (2, 355, 5), 5759: (2, 355, 5), 5780: (2, 355, 5), 5783: (2, 355, 5),
    5762: (3, 354, 5), 5766: (3, 354, 5), 5769: (3, 354, 5),
    5748: (5, 354, 7), 5751: (5, 354, 7), 5758: (5, 354, 7), 5772: (5, 354, 7),
    5775: (5, 354, 7), 5778: (5, 354, 7),
    5754: (5, 355, 1), 5785: (5, 355, 1),
    5761: (7, 353, 1), 5781: (7, 353, 1),
    5750: (7, 355, 3), 5764: (7, 355, 3), 5767: (7, 355, 3), 5770: (7, 355, 3),
    5788: (7, 355, 3),
    5749: (2, 383, 5), 5790: (2, 383, 5),
    5752: (2, 385, 7), 5776: (2, 385, 7), 5779: (2, 385, 7),
    5755: (3, 384, 7), 5782: (3, 384, 7),
    5765: (5, 383, 1), 5768: (5, 383, 1), 5812: (5, 383, 1),
    5744: (5, 385, 3), 5771: (5, 385, 3), 5774: (5, 385, 3),
    5757: (7, 383, 3), 5784: (7, 383, 3),
    5760: (7, 385, 5), 5763: (7, 385, 5), 5787: (7, 385, 5)
    }


class TestSetDate(object):

    def test_default_today(self):
        assert hdate.set_date(None) == datetime.date.today()

    def test_random_date(self, random_date):
        randomday = datetime.date(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    @pytest.mark.parametrize('execution_number', range(5))
    def test_random_datetime(self, execution_number, random_date):
        randomday = datetime.datetime(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    def test_illegal_value(self):
        with pytest.raises(TypeError):
            hdate.set_date(100)


class TestHDate(object):

    NON_MOVING_HOLIDAYS = [
        ((1, 1), 1, "Rosh Hashana"),
        ((2, 1), 2, "Rosh Hashana II"),
        ((9, 1), 37, "Erev Yom Kippur"),
        ((10, 1), 4, "Yom Kippur"),
        ((15, 1), 5, "Sukkot"),
        ((17, 1), 6, "Chol Hamoed Sukkot"),
        ((18, 1), 6, "Chol Hamoed Sukkot"),
        ((19, 1), 6, "Chol Hamoed Sukkot"),
        ((20, 1), 6, "Chol Hamoed Sukkot"),
        ((21, 1), 7, "Hoshana Raba"),
        ((22, 1), 27, "Shmini Atseret"),
        ((15, 7), 15, "Pesach"),
        ((17, 7), 16, "Chol Hamoed Pesach"),
        ((18, 7), 16, "Chol Hamoed Pesach"),
        ((19, 7), 16, "Chol Hamoed Pesach"),
        ((20, 7), 16, "Chol Hamoed Pesach"),
        ((21, 7), 28, "Shvi'i shel Pesach"),
        ((5, 9), 19, "Erev Shavuot"),
        ((6, 9), 20, "Shavuot"),

        ((25, 3), 9, "Chanuka"),
        ((26, 3), 9, "Chanuka"),
        ((27, 3), 9, "Chanuka"),
        ((28, 3), 9, "Chanuka"),
        ((29, 3), 9, "Chanuka"),
        ((1, 4), 9, "Chanuka"),
        ((2, 4), 9, "Chanuka"),
        ((10, 4), 10, "Asara b'Tevet"),
        ((15, 5), 11, "Tu b'Shvat"),
        ((18, 8), 18, "Lag BaOmer"),
        ((15, 11), 23, "Tu b'Av")
    ]

    DIASPORA_ISRAEL_HOLIDAYS = [
        # Date, holiday in Diaspora, holiday in Israel
        ((16, 1), 31, 6, "Sukkot II"),
        ((23, 1), 8, 0, "Simchat Torah"),
        ((16, 7), 32, 16, "Pesach II"),
        ((22, 7), 29, 0, "Acharon Shel Pesach"),
        ((7, 9), 30, 0, "Shavuot II")
    ]

    MOVING_HOLIDAYS = [
        # Possible dates, test year range, holiday result, name
        ([(3, 1), (4, 1)], (5000, 6500), 3, "Tsom Gedalya"),
        ([(17, 10), (18, 10)], (5000, 6500), 21, "Shiva Asar b'Tamuz"),
        ([(9, 11), (10, 11)], (5000, 6500), 22, "Tisha b'Av"),
        ([(26, 7), (27, 7), (28, 7)], (5718, 6500), 24, "Yom Hasho'a"),
        ([(3, 8), (4, 8), (5, 8)], (5709, 5763), 17, "Yom Ha'atsmaut"),
        ([(3, 8), (4, 8), (5, 8), (6, 8)], (5764, 6500), 17, "Yom Ha'atsmaut"),
        ([(2, 8), (3, 8), (4, 8)], (5709, 5763), 25, "Yom Hazikaron"),
        ([(2, 8), (3, 8), (4, 8), (5, 8)], (5764, 6500), 25, "Yom Hazikaron"),
        ([(28, 8)], (5728, 6500), 26, "Yom Yerushalayim"),
        ([(11, 2), (12, 2)], (5758, 6500), 35, "Rabin Memorial day"),
        ([(29, 10), (1, 11)], (5765, 6500), 36, "Zhabotinsky day"),
        ([(30, 5)], (5000, 6500), 33, "Family day")
    ]

    # Missing tests:
    # - chanuka: 3 tevet or 30 kislev
    # - Mukdam: Ta'anit Esther
    # - Ta'anit Esther, Purim, Shushan Purim: Adar vs Adar II
    # - Israli holidays (have a starting year):
    #   * Memorial day for fallen whose place of burial is unknown

    @pytest.fixture
    def default_values(self):
        return hdate.HDate()

    @pytest.fixture
    def random_hdate(self, random_date):
        date = datetime.date(*random_date)
        return hdate.HDate(date)

    def test_default_weekday(self, default_values):
        expected_weekday = datetime.datetime.today().weekday() + 2
        expected_weekday = expected_weekday if expected_weekday < 8 else 1
        assert default_values._weekday == expected_weekday

    @pytest.mark.parametrize('execution_number', range(10))
    def test_random_weekday(self, execution_number, random_hdate):
        expected_weekday = random_hdate._gdate.weekday() + 2
        expected_weekday = expected_weekday if expected_weekday < 8 else 1
        assert random_hdate._weekday == expected_weekday

    @pytest.mark.parametrize('execution_number', range(10))
    def test_random_hdate(self, execution_number, random_hdate):
        _hdate = hdate.HDate()
        _hdate.hdate_set_hdate(random_hdate._h_day, random_hdate._h_month,
                               random_hdate._h_year)
        assert _hdate._h_day == random_hdate._h_day
        assert _hdate._h_month == random_hdate._h_month
        assert _hdate._h_year == random_hdate._h_year
        assert _hdate.jdn == random_hdate.jdn
        assert _hdate._weekday == random_hdate._weekday
        assert _hdate._h_size_of_year == random_hdate._h_size_of_year
        assert _hdate._h_year_type == random_hdate._h_year_type
        assert _hdate._h_weeks == random_hdate._h_weeks
        assert _hdate._gdate == random_hdate._gdate
        assert _hdate._h_new_year_weekday == random_hdate._h_new_year_weekday

    def test_hj_get_size_of_hebrew_year(self):
        for year, info in HEBREW_YEARS_INFO.items():
            assert hj.get_size_of_hebrew_year(year) == info[1]

    @pytest.mark.parametrize('execution_number', range(10))
    def test_hdate_get_size_of_hebrew_years(self, execution_number,
                                            random_hdate):
        assert (random_hdate._h_size_of_year ==
                hj.get_size_of_hebrew_year(random_hdate._h_year))

    def test_rosh_hashana_day_of_week(self, random_hdate):
        for year, info in HEBREW_YEARS_INFO.items():
            random_hdate.hdate_set_hdate(random_hdate._h_day,
                                         random_hdate._h_month, year)
            assert random_hdate._h_new_year_weekday == info[0]

    def test_pesach_day_of_week(self, random_hdate):
        for year, info in HEBREW_YEARS_INFO.items():
            random_hdate.hdate_set_hdate(15, 7, year)
            assert random_hdate._weekday == info[2]
            assert random_hdate.get_holyday() == 15

    @pytest.mark.parametrize('date, holiday, name', NON_MOVING_HOLIDAYS)
    def test_get_holidays_non_moving(self, random_hdate, date, holiday, name):
        random_hdate.hdate_set_hdate(*date, year=random_hdate._h_year)
        assert random_hdate.get_holyday() == holiday

    @pytest.mark.parametrize('date, diaspora_holiday, israel_holiday, name',
                             DIASPORA_ISRAEL_HOLIDAYS)
    def test_get_diaspora_israel_holidays(self, random_hdate, date,
                                          diaspora_holiday, israel_holiday,
                                          name):
        random_hdate.hdate_set_hdate(*date, year=random_hdate._h_year)
        assert random_hdate.get_holyday() == israel_holiday
        random_hdate._diaspora = True
        assert random_hdate.get_holyday() == diaspora_holiday

    @pytest.mark.parametrize('possible_dates, years, holiday, name',
                             MOVING_HOLIDAYS)
    def test_get_holidays_moving(self, possible_dates, years, holiday, name):
        found_matching_holiday = False
        year = random.randint(*years)

        print "Testing " + name + " for " + str(year)

        for date in possible_dates:
            date_under_test = hdate.HDate()
            date_under_test.hdate_set_hdate(*date, year=year)
            if date_under_test.get_holyday() == holiday:
                for other in possible_dates:
                    if other != date:
                        other_date = hdate.HDate()
                        other_date.hdate_set_hdate(*other, year=year)
                        assert other_date.get_holyday() != holiday
                found_matching_holiday = True

        assert found_matching_holiday

        # Test holiday == 0 before 'since'
        # In case of yom hazikaron and yom ha'atsmaut don't test for the
        # case of 0 between 5708 and 5764
        if years[0] != 5000:
            if years[0] == 5764 and holiday in [17, 25]:
                return
            year = random.randint(5000, years[0]-1)
            print "Testing " + name + " for " + str(year)
            for date in possible_dates:
                date_under_test = hdate.HDate()
                date_under_test.hdate_set_hdate(*date, year=year)
                assert date_under_test.get_holyday() == 0

    @pytest.mark.parametrize('execution_number', range(10))
    def test_get_omer_day(self, execution_number, random_hdate):
        if (random_hdate._h_month not in [7, 8, 9] or
            random_hdate._h_month == 7 and random_hdate._h_day < 16 or
                random_hdate._h_month == 9 and random_hdate._h_day > 5):
            assert random_hdate.get_omer_day() == 0

        nissan = range(16, 30)
        iyyar = range(1, 29)
        sivan = range(1, 5)

        for day in nissan:
            random_hdate.hdate_set_hdate(day, 7, random_hdate._h_year)
            assert random_hdate.get_omer_day() == day - 15
        for day in iyyar:
            random_hdate.hdate_set_hdate(day, 8, random_hdate._h_year)
            assert random_hdate.get_omer_day() == day + 15
        for day in sivan:
            random_hdate.hdate_set_hdate(day, 9, random_hdate._h_year)
            assert random_hdate.get_omer_day() == day + 44

    @pytest.mark.parametrize('execution_number', range(40))
    def test_get_holyday_type(self, execution_number):
        holyday = execution_number
        # regular day
        if holyday == 0:
            assert hdate.get_holyday_type(holyday) == 0
        # Yom tov
        if holyday in [1, 2, 4, 5, 8, 15, 20, 27, 28, 29, 30, 31, 32]:
            assert hdate.get_holyday_type(holyday) == 1
        # Erev yom kippur
        if holyday == 37:
            assert hdate.get_holyday_type(holyday) == 2
        # Hol hamoed
        if holyday in [6, 7, 16]:
            assert hdate.get_holyday_type(holyday) == 3
        # Hanuka and purim
        if holyday in [9, 13, 14]:
            assert hdate.get_holyday_type(holyday) == 4
        # Tzom
        if holyday in [3, 10, 12, 21, 22]:
            assert hdate.get_holyday_type(holyday) == 5
        # Independance day and Yom yerushalaim
        if holyday in [17, 26]:
            assert hdate.get_holyday_type(holyday) == 6
        # Lag baomer ,Tu beav, Tu beshvat
        if holyday in [18, 23, 11]:
            assert hdate.get_holyday_type(holyday) == 7
        # Tzahal and Holocaust memorial days
        if holyday in [24, 25]:
            assert hdate.get_holyday_type(holyday) == 8
        # Not a holy day (yom hamishpacha, zhabotinsky, rabin, fallen soldiers
        # whose burial place is unknown)
        if holyday in [33, 34, 35, 36]:
            assert hdate.get_holyday_type(holyday) == 9
