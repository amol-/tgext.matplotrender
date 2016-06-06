# -*- coding: utf-8 -*-
from unittest import TestCase
from tg import AppConfig
from tg.util import Bunch
from webtest import TestApp


class AppGlobals(object):
    pass


def make_appcfg_for_controller(root_controller):
    config = AppConfig(minimal=True, root_controller=root_controller)
    config['helpers'] = Bunch()
    config['app_globals'] = AppGlobals
    return config


class BaseTestClass(TestCase):
    RootController = None

    @classmethod
    def setup_app(cls, config):
        pass

    @classmethod
    def setUpClass(cls):
        config = make_appcfg_for_controller(cls.RootController())
        cls.setup_app(config)
        cls.wsgi_app = config.make_wsgi_app()

    def setUp(self):
        self.app = TestApp(self.wsgi_app)

