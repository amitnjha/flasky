import unittest
from app import create_app, db, fake
from app.models import User,Role
from selenium import webdriver
import threading
import re
import time

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        #start Chrome
        print('%%%%%%%%%%%% CHROME %%%%%%%%%%%%%%%%%%%')
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')

        try:
            cls.client = webdriver.Chrome()
        except:
            pass

        #skip thse tess if the browser could not be started
        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            #suppress logging to kee unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            admin_role = Role.query.filter_by(permissions = 0xff).first()
            admin = User(email = 'john@example.com', username = 'john', role = admin_role, password = 'cat')
            db.session.add(admin)
            db.session.commit()
            print(admin.id)
            
            #print('Added USer.............')
            #user = User.query.filter_by(email='john@example.com').first()
            #print(user)
            #allobjs = User.query.order_by(User.username).all()
            #for obj in allobjs:
            #    print(obj.email)
            #start the Flask Server in a thread

            cls.server_thread = threading.Thread(target = cls.app.run, kwargs =  {'debug': 'true', 'use_reloader' : False, 'use_debugger': True})
            cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_dummy(self):
        self.assertTrue(1==1)
    
    def test_admin_home_page(self):
        self.client.get('http://localhost:5000')
        #time.sleep(2)
        self.assertTrue(re.search('Stranger', self.client.page_source))

        self.client.find_element_by_link_text('Log In').click()
        #time.sleep(10)
        #self.assertIn('<h1>Login</h1>', self.client.page_source)
        
        #log in
        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        #time.sleep(20)
        self.assertTrue(re.search('Hello\s+john', self.client.page_source))

        self.client.find_element_by_link_text('Profile').click()
        self.assertIn('john', self.client.page_source)
        
