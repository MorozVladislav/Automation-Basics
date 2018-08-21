#!/usr/bin/env python3
# -*- coding: ascii -*-
from steps.db_steps import DBSteps

steps = DBSteps('test_db', 'root', '1Qaz2Wsx', host='192.168.56.101')
print(steps.get_user_login(user_id=10))
