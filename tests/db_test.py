#!/usr/bin/env python3
# -*- coding: ascii -*-

USERNAME = 'Joshua Stevens'
LOGIN = 'josh'
PASSWORD = 'Qw17M85s'
TITLE = 'BMW'
TYPE = 'M5'
PRICE = 120000


class TestDB(object):

    def test_get_user_by_id(self, db_steps):
        assert db_steps.get_user_by_id(47).name == 'Kelly Wilson'

    def test_get_users_by_name(self, db_steps):
        users = db_steps.get_users_by_name('Maria Sims')
        logins = []
        for user in users:
            logins.append(user.login)
        assert 'norma' in logins

    def test_get_user_login(self, db_steps):
        assert db_steps.get_user_by_id(10).login == 'annie'

    def test_get_user_password(self, db_steps):
        assert db_steps.get_user_by_id(77).password == 'y9wIFB3h'

    def test_get_user_vehicles(self, db_steps):
        vehicle_ids = [1, 3, 6, 7]
        vehicles = db_steps.get_user_vehicles(15)
        for vehicle in vehicles:
            assert vehicle.id in vehicle_ids

    def test_get_vehicle_by_id(self, db_steps):
        assert db_steps.get_vehicle_by_id(3).title == '1F435E'

    def test_get_vehicle_by_title(self, db_steps):
        assert db_steps.get_vehicle_by_title('78A6F2').id == 6

    def test_get_vehicle(self, db_steps):
        assert db_steps.get_vehicle(vehicle_id=3).title == '1F435E'
        assert db_steps.get_vehicle(title='78A6F2').id == 6

    def test_get_vehicle_type(self, db_steps):
        assert db_steps.get_vehicle_type(vehicle_id=5) == 'D41'
        assert db_steps.get_vehicle_type(title='304B79') == '9F8'

    def test_get_vehicles_by_type(self, db_steps):
        vehicles = db_steps.get_vehicles_by_type('AC6')
        vehicle_ids = []
        for vehicle in vehicles:
            vehicle_ids.append(vehicle.id)
        assert 4 in vehicle_ids

    def test_get_vehicle_price(self, db_steps):
        assert db_steps.get_vehicle_price(vehicle_id=10) == 444742
        assert db_steps.get_vehicle_price(title='9467AF') == 520959

    def test_get_owners(self, db_steps):
        user_ids = [8, 11, 15, 17, 18, 23, 29, 30, 32, 37, 42, 52, 55, 60, 61, 63, 64, 67, 70, 73, 76, 79, 80, 81, 83,
                    84, 92, 94, 95]
        users = db_steps.get_owners(vehicle_id=7)
        for user in users:
            assert user.id in user_ids
        users = db_steps.get_owners(title='304B79')
        for user in users:
            assert user.id in user_ids

    def test_get_user_vehicles_total_price(self, db_steps):
        assert db_steps.get_user_vehicles_total_price(99) == 566388

    def test_add_user(self, db_steps):
        vehicles_ids = (2, 5, 9, 2)
        vehicles = []
        for vehicle_id in vehicles_ids:
            vehicles.append(db_steps.get_vehicle_by_id(vehicle_id))
        db_steps.add_user(USERNAME, LOGIN, PASSWORD, vehicles=vehicles)
        db_steps.save_all()
        users = db_steps.get_users_by_name(USERNAME)
        for user in users:
            if user.login == LOGIN and user.password == PASSWORD:
                for vehicle in user.vehicles:
                    assert vehicle.id in vehicles_ids
                assert len(user.vehicles) == len(set(vehicles_ids))
                return
        raise UserWasNotAdded('User {} was not added to BD'.format(USERNAME))

    def test_delete_user(self, db_steps):
        users = db_steps.get_users_by_name(USERNAME)
        for user in users:
            if user.login == LOGIN and user.password == PASSWORD:
                db_steps.delete_user(user.id)
                db_steps.save_all()
                assert db_steps.get_user_by_id(user.id) is None
                return
        raise UserNotFound('User {} not found'.format(USERNAME))

    def test_add_vehicle(self, db_steps):
        user_ids = (15, 18, 24, 57, 82, 99, 15, 24)
        users = []
        for user_id in user_ids:
            users.append(db_steps.get_user_by_id(user_id))
        db_steps.add_vehicle(TITLE, TYPE, PRICE, users=users)
        db_steps.save_all()
        assert db_steps.get_vehicle_type(title=TITLE) == TYPE
        assert db_steps.get_vehicle_price(title=TITLE) == PRICE
        owners = db_steps.get_owners(title=TITLE)
        for owner in owners:
            assert owner.id in user_ids
        assert len(owners) == len(set(user_ids))

    def test_delete_vehicle(self, db_steps):
        db_steps.delete_vehicle(title=TITLE)
        db_steps.save_all()
        assert db_steps.get_vehicle_by_title(TITLE) is None


class DBTestError(Exception):
    pass


class UserWasNotAdded(DBTestError):
    pass


class UserNotFound(DBTestError):
    pass
