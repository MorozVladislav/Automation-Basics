#!/usr/bin/env python3
# -*- coding: ascii -*-


class TestDB(object):

    def test_get_user_by_name(self, db_steps):
        assert db_steps.get_user_by_name('Diane Ford').login == 'susan'

    def test_get_user_by_id(self, db_steps):
        assert db_steps.get_user_by_id(47).name == 'Robin Scott'

    def test_get_user_login(self, db_steps):
        assert db_steps.get_user_login(user_id=10) == 'diane'
        assert db_steps.get_user_login(username='Robin Scott') == 'nancy'

    def test_get_user_password(self, db_steps):
        assert db_steps.get_user_password(user_id=77) == '7WPb4Mau'
        assert db_steps.get_user_password(username='Mary Watson') == 'FxYh8smZ'

    def test_get_user_vehicles(self, db_steps):
        vehicle_ids = [7, 8, 10]
        vehicles = db_steps.get_user_vehicles(user_id=15)
        for vehicle in vehicles:
            assert vehicle.id in vehicle_ids
        vehicles = db_steps.get_user_vehicles(username='Ann Campbell')
        for vehicle in vehicles:
            assert vehicle.id in vehicle_ids

    def test_get_vehicle_by_title(self, db_steps):
        assert db_steps.get_vehicle_by_title('A6DB09').id == 6

    def test_get_vehicle_by_id(self, db_steps):
        assert db_steps.get_vehicle_by_id(3).title == '1D75A9'

    def test_get_vehicle_type(self, db_steps):
        assert db_steps.get_vehicle_type(vehicle_id=5) == 'E64'
        assert db_steps.get_vehicle_type(title='A62D1B') == 'AE2'

    def test_get_vehicle_price(self, db_steps):
        assert db_steps.get_vehicle_price(vehicle_id=10) == 855743
        assert db_steps.get_vehicle_price(title='079465') == 741598

    def test_get_users_owing_vehicle(self, db_steps):
        user_ids = [1, 5, 8, 12, 15, 17, 22, 29, 36, 37, 38, 39, 40, 43, 47, 48, 49, 50, 58, 59, 64, 69, 70, 73, 75,
                    82, 86, 87, 90, 100]
        users = db_steps.get_users_owing_vehicle(vehicle_id=7)
        for user in users:
            assert user.id in user_ids
        users = db_steps.get_users_owing_vehicle(title='079465')
        for user in users:
            assert user.id in user_ids

    def test_get_user_vehicles_total_price(self, db_steps):
        assert db_steps.get_user_vehicles_total_price(user_id=100) == 1557608
        assert db_steps.get_user_vehicles_total_price(username='Margaret Fisher') == 1557608
