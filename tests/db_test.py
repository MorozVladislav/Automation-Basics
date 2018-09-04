#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class TestDB(object):

    def test_get_user_by_id(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_1
        assert db_steps.get_user_by_id(condition).name == expected_result

    def test_get_users_by_name(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_2
        logins = [user.login for user in db_steps.get_users_by_name(condition)]
        assert expected_result in logins

    def test_get_user_by_login(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_3
        assert db_steps.get_user_by_login(condition).name == expected_result

    def test_get_user_login(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_4
        assert db_steps.get_user_by_id(condition).login == expected_result

    def test_get_user_password(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_5
        assert db_steps.get_user_by_id(condition).password == expected_result

    def test_get_user_vehicles(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_6
        vehicles = db_steps.get_user_vehicles(condition)
        for vehicle in vehicles:
            assert vehicle.id in expected_result

    def test_get_vehicle_by_id(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_7
        assert db_steps.get_vehicle_by_id(condition).title == expected_result

    def test_get_vehicle_by_title(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_8
        assert db_steps.get_vehicle_by_title(condition).id == expected_result

    def test_get_vehicle(self, db_steps, samples):
        condition_1, expected_result_1 = samples.SAMPLE_9_1
        condition_2, expected_result_2 = samples.SAMPLE_9_2
        assert db_steps.get_vehicle(vehicle_id=condition_1).title == expected_result_1
        assert db_steps.get_vehicle(title=condition_2).id == expected_result_2

    def test_get_vehicle_type(self, db_steps, samples):
        condition_1, expected_result_1 = samples.SAMPLE_10_1
        condition_2, expected_result_2 = samples.SAMPLE_10_2
        assert db_steps.get_vehicle_type(vehicle_id=condition_1) == expected_result_1
        assert db_steps.get_vehicle_type(title=condition_2) == expected_result_2

    def test_get_vehicles_by_type(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_11
        vehicle_ids = [vehicle.id for vehicle in db_steps.get_vehicles_by_type(condition)]
        assert expected_result in vehicle_ids

    def test_get_vehicle_price(self, db_steps, samples):
        condition_1, expected_result_1 = samples.SAMPLE_12_1
        condition_2, expected_result_2 = samples.SAMPLE_12_2
        assert db_steps.get_vehicle_price(vehicle_id=condition_1) == expected_result_1
        assert db_steps.get_vehicle_price(title=condition_2) == expected_result_2

    def test_get_owners(self, db_steps, samples):
        condition_1, expected_result_1 = samples.SAMPLE_13_1
        condition_2, expected_result_2 = samples.SAMPLE_13_2
        users = db_steps.get_owners(vehicle_id=condition_1)
        for user in users:
            assert user.id in expected_result_1
        users = db_steps.get_owners(title=condition_2)
        for user in users:
            assert user.id in expected_result_2

    def test_get_user_vehicles_total_price(self, db_steps, samples):
        condition, expected_result = samples.SAMPLE_14
        assert db_steps.get_user_vehicles_total_price(condition) == expected_result

    def test_add_user(self, db_steps, samples):
        name, login, password, vehicle_ids = samples.SAMPLE_15
        vehicles = [db_steps.get_vehicle_by_id(vehicle_id) for vehicle_id in vehicle_ids]
        db_steps.add_user(name, login, password, vehicles=vehicles)
        db_steps.save_all()
        users = db_steps.get_users_by_name(name)
        for user in users:
            if user.login == login and user.password == password:
                for vehicle in user.vehicles:
                    assert vehicle.id in vehicle_ids
                assert len(user.vehicles) == len(set(vehicle_ids))
                return
        raise UserWasNotAdded('User {} was not added to BD'.format(name))

    def test_delete_user(self, db_steps, samples):
        name, login, password, vehicles_ids = samples.SAMPLE_15
        users = db_steps.get_users_by_name(name)
        for user in users:
            if user.login == login and user.password == password:
                db_steps.delete_user(user.id)
                db_steps.save_all()
                assert db_steps.get_user_by_id(user.id) is None
                return
        raise UserNotFound('User {} not found'.format(name))

    def test_add_vehicle(self, db_steps, samples):
        title, vehicle_type, price, user_ids = samples.SAMPLE_16
        users = [db_steps.get_user_by_id(user_id) for user_id in user_ids]
        db_steps.add_vehicle(title, vehicle_type, price, users=users)
        db_steps.save_all()
        assert db_steps.get_vehicle_type(title=title) == vehicle_type
        assert db_steps.get_vehicle_price(title=title) == price
        owners = db_steps.get_owners(title=title)
        for owner in owners:
            assert owner.id in user_ids
        assert len(owners) == len(set(user_ids))

    def test_delete_vehicle(self, db_steps, samples):
        title, vehicle_type, price, user_ids = samples.SAMPLE_16
        db_steps.delete_vehicle(title=title)
        db_steps.save_all()
        assert db_steps.get_vehicle_by_title(title) is None


class DBTestError(Exception):
    pass


class UserWasNotAdded(DBTestError):
    pass


class UserNotFound(DBTestError):
    pass
