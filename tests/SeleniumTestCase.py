from selenium import webdriver

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        #start Chrome
        print('!!!!!!!!!!!!!!!!!saddsad!!!!!!')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        try:
            cls.client = webdriver.Chrome(chrome_options = options)
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
            admin = User(email = 'john@exmaple.com', username = 'john', role = admin_role, password = 'cat')
            db.session.add(admin)
            db.session.commit()

            #start the Flask Server in a thread

            cls.server_thread = threading.Thread(target = cls.app.run, kwargs =  {'debug': 'false', 'user_reloader' : False, 'use_debugger': False})
            cls.server_trhead.start()

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
    
    
