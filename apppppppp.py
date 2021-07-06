import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
class MyApp(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("TITANS REPORT")
        self.setMaximumSize(828, 501)
        self.setMinimumSize(828, 501)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        self.subid.setReadOnly(True)

        self.uid = str(uuid.uuid4())
        self.r = requests.Session()
        self.cookies = []
        self.reels_id = []
        self.targets = []
        self.ids = []
        self.done = 0
        self.error = 0
        self.loadedstr = 0
        self.bndstr = 0

        self.added = 0

        self.headers = {
            'X-Pigeon-Session-Id': self.uid,
            'X-IG-Device-ID': self.uid,
            'X-IG-App-Locale': 'en_US',
            'X-IG-Device-Locale': 'en_US',
            'X-IG-Mapped-Locale': 'en_US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTvw8=',
            'User-Agent': 'Instagram 151.0.0.23.120 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com'
        }

        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)

        x = subprocess.check_output(
            'wmic csproduct get uuid').decode().split('\n')[1].strip()
        self.subid.setText(x)

        self.loginprf_2.clicked.connect(self.checksub)

        self.loginprf.clicked.connect(self.openaccs)
        self.loginstr.clicked.connect(self.openaccs)
        self.loginhi.clicked.connect(self.openaccs)

        self.startprf.clicked.connect(self.startThread)
        self.startstr.clicked.connect(self.startThread)
        self.starthi.clicked.connect(self.startThread)

        self.addprf.clicked.connect(self.addTarget)
        self.addstr.clicked.connect(self.addTarget)
        self.addhi.clicked.connect(self.addTarget)

    def checksub(self):
        tkn = self.subid.text()
        if tkn != "":
            if tkn in requests.get('https://pastebin.com/raw/iLYei3Kd').text:
                self.tabWidget.setTabEnabled(1, True)
                self.tabWidget.setTabEnabled(2, True)
                self.tabWidget.setTabEnabled(3, True)
                self.tabWidget.setCurrentIndex(1)
                self.tabWidget.setTabEnabled(0, False)

            else:
                autopy.alert.alert("Not Subscribed", "CHECK SUB")

    def openaccs(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(
            self, "Accounts file", "", "All Files (*.txt);;Python Files (*.py)", options=options)
        threading.Thread(target=self.login).start()

    def login(self):
        if self.tabWidget.currentIndex() == 1:
            label = self.talgn
        elif self.tabWidget.currentIndex() == 2:
            label = self.stlgn
        elif self.tabWidget.currentIndex() == 3:
            label = self.hilgn
        done = 0
        accs = open(self.fileName, 'r').read().splitlines()
        for acc in accs:

            user = acc.split(':')[0]
            pasw = acc.split(':')[1]

            url_login = 'https://i.instagram.com/api/v1/accounts/login/'

            self.headers = {
                'X-Pigeon-Session-Id': self.uid,
                'X-IG-Device-ID': self.uid,
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw8=',
                'User-Agent': 'Instagram 165.1.0.29.119 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com'
            }

            data = {
                '_uuid': self.uid,
                'username': user,
                'enc_password': '#PWD_INSTAGRAM_BROWSER:0:1589682409:{}'.format(pasw),
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'device_id': self.uid,
                'from_reg': 'false',
                '_csrftoken': 'missing',
                'login_attempt_count': '0'
            }
            self.req1 = self.r.post(url_login, headers=self.headers, data=data)

            if ('logged_in_user') in self.req1.text:
                self.cookies.append(self.req1.cookies)
                done += 1
                label.setText(f"LOGINS : {done}")
            else:
                pass

    def addTarget(self):
        if self.tabWidget.currentIndex() == 1:
            target = self.tarprf.text()
            try:
                get = self.r.get(
                    f'https://www.instagram.com/{target}/?__a=1', cookies=random.choice(self.cookies)).json()
                idd = str(get["logging_page_id"]).split('_')[1]
                self.targets.append(idd)
                self.added += 1
            except:
                autopy.alert.alert("No Target Found", "Error")
            self.taprf.setText(f"TARGETS : {self.added}")
        elif self.tabWidget.currentIndex() == 2:
            target = self.tarstr.text()
            try:
                get = self.r.get(
                    f'https://www.instagram.com/{target}/?__a=1', cookies=random.choice(self.cookies)).json()
                idd = str(get["logging_page_id"]).split('_')[1]
                self.targets.append(idd)
                self.added += 1
            except:
                autopy.alert.alert("No Target Found", "Error")
            self.tastr.setText(f"TARGETS : {self.added}")

        elif self.tabWidget.currentIndex() == 3:
            target = self.tarhi.text()
            try:
                get = self.r.get(
                    f'https://www.instagram.com/{target}/?__a=1', cookies=random.choice(self.cookies)).json()
                idd = str(get["logging_page_id"]).split('_')[1]
                self.targets.append(idd)
                self.added += 1
            except:
                autopy.alert.alert("No Target Found", "Error")
            self.tahi.setText(f"TARGETS : {self.added}")

    def startThread(self):
        if self.tabWidget.currentIndex() == 1:
            self.dnlab = self.dnprf
            self.erlab = self.erprf

            if self.spam.isChecked():
                self.reptp = 'ig_spam_v3'

            elif self.self.isChecked():
                self.reptp = 'ig_self_injury_v3'

            elif self.hate.isChecked():
                self.reptp = 'ig_hate_speech_v3'

            elif self.scam.isChecked():
                self.reptp = 'ig_product_scam_fraud_v2'

            elif self.falseinfo.isChecked():
                self.reptp = 'ig_false_news'

            elif self.vio.isChecked():
                self.reptp = 'ig_violence_threat'
                self.maintp = "ig_violence_parent"

            elif self.drugs.isChecked():
                self.reptp = 'ig_drugs_v3'
                self.maintp = "ig_sale_of_illegal_or_regulated_goods_v3"

            elif self.bully.isChecked():
                self.reptp = 'ig_bullying_or_harassment_comment_v3'
                self.maintp = "ig_bullying_or_harassment_me_v3"

            elif self.nudity.isChecked():
                self.reptp = 'ig_nudity_or_pornography_v3'
                self.maintp = "ig_nudity_v2"

            elif self.imper.isChecked():
                self.reptp = 'ig_user_impersonation_me'
                self.maintp = "ig_user_impersonation"

            elif self.radioButton.isChecked():
                self.reptp = 'ig_firearms_v3'
                self.maintp = "ig_sale_of_illegal_or_regulated_goods_v3"

            elif self.animal.isChecked():
                self.reptp = 'ig_animal_abuse'
                self.maintp = "ig_violence_parent"

            elif self.posting.isChecked():
                self.reptp = '1'

            threading.Thread(target=self.report_profile).start()

        elif self.tabWidget.currentIndex() == 2:
            self.dnlab = self.dnstr
            self.erlab = self.erstr
            self.cntstr = self.cntstrids
            self.cntbnd = self.cntstrbnd
            threading.Thread(target=self.story_get).start()
        elif self.tabWidget.currentIndex() == 3:
            self.dnlab = self.dnhi
            self.erlab = self.erhi
            if self.spam_2.isChecked():
                self.reptp = 'ig_spam_v3'

            elif self.self_2.isChecked():
                self.reptp = 'ig_self_injury_v3'

            elif self.hate_2.isChecked():
                self.reptp = 'ig_hate_speech_v3'

            elif self.scam_4.isChecked():
                self.reptp = 'ig_product_scam_fraud_v2'

            elif self.falseinfo_4.isChecked():
                self.reptp = 'ig_false_news'

            elif self.vio_2.isChecked():
                self.reptp = 'ig_violence_threat'
                self.maintp = "ig_violence_parent"

            elif self.drugs_3.isChecked():
                self.reptp = 'ig_drugs_v3'
                self.maintp = "ig_sale_of_illegal_or_regulated_goods_v3"

            elif self.bully_3.isChecked():
                self.reptp = 'ig_bullying_or_harassment_comment_v3'
                self.maintp = "ig_bullying_or_harassment_me_v3"

            elif self.nudity_3.isChecked():
                self.reptp = 'ig_nudity_or_pornography_v3'
                self.maintp = "ig_nudity_v2"

            elif self.radioButton_4.isChecked():
                self.reptp = 'ig_firearms_v3'
                self.maintp = "ig_sale_of_illegal_or_regulated_goods_v3"

            elif self.animal_4.isChecked():
                self.reptp = 'ig_animal_abuse'
                self.maintp = "ig_violence_parent"
            threading.Thread(target=self.get_highligts).start()

    def report_profile(self):
        try:
            while True:
                for cki in self.cookies:
                    for i in range(0, 10):
                        target_id = str(random.choice(self.targets))
                        data1 = f'object_id='+target_id+'&object_type=5&entry_point=1&_csrftoken=missing&_uuid=' + \
                            self.uid+'&is_dark_mode=true&frx_prompt_request_type=1&container_module=profile&location=2'

                        response = requests.post(
                            'https://i.instagram.com/api/v1/reports/get_frx_prompt/', headers=self.headers, cookies=cki, data=data1)

                        if response.status_code != 200:
                            continue
                        reporter_id = response.json(
                        )['response']['report_info']['reporter_id']

                        responsible_id = response.json(
                        )['response']['report_info']['responsible_id']
                        aaaaa = json.loads(response.json()['response']['context'])
                        jj = json.loads(aaaaa['ixt_context_from_www'])
                        cc = json.loads(jj['session'])
                        mapp = cc['extra_data']['sentry_feature_map']

                        if self.reptp == "ig_spam_v3":

                            data2 = '_csrftoken=missing&_uuid='+self.uid+'&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.reptp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%220ac6368e-b4d9-4ecf-bf12-476c813d3ea1%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22'+self.reptp+'%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                'JvT3t'+'%5C%5C%5C%5C%5C%5C%5C%2F'+mapp+'%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFhwWlprViAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%228d1ef464-4092-48e4-a7c4-51ed16f75f5d%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif self.reptp == "ig_self_injury_v3":

                            data2 = '_csrftoken=missing&_uuid='+self.uid+'&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.reptp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%220ac6368e-b4d9-4ecf-bf12-476c813d3ea1%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22'+self.reptp+'%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                'JvT3t'+'%5C%5C%5C%5C%5C%5C%5C%2F'+mapp+'%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFhwWlprViAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%228d1ef464-4092-48e4-a7c4-51ed16f75f5d%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif self.reptp == "ig_hate_speech_v3":

                            data2 = '_csrftoken=missing&_uuid='+self.uid+'&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.reptp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%220ac6368e-b4d9-4ecf-bf12-476c813d3ea1%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22'+self.reptp+'%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                'JvT3t'+'%5C%5C%5C%5C%5C%5C%5C%2F'+mapp+'%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFhwWlprViAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%228d1ef464-4092-48e4-a7c4-51ed16f75f5d%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'
                        elif self.reptp == "ig_product_scam_fraud_v2":
                            data2 = '_csrftoken=missing&_uuid='+self.uid+'&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.reptp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%220ac6368e-b4d9-4ecf-bf12-476c813d3ea1%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22'+self.reptp+'%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                'JvT3t'+'%5C%5C%5C%5C%5C%5C%5C%2F'+mapp+'%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFhwWlprViAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%228d1ef464-4092-48e4-a7c4-51ed16f75f5d%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif self.reptp == "ig_false_news":
                            data2 = '_csrftoken=missing&_uuid='+self.uid+'&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.reptp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%220ac6368e-b4d9-4ecf-bf12-476c813d3ea1%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22'+self.reptp+'%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                'JvT3t'+'%5C%5C%5C%5C%5C%5C%5C%2F'+mapp+'%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeFy9wcm9tcHQvFhwWlprViAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%228d1ef464-4092-48e4-a7c4-51ed16f75f5d%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif self.reptp == "ig_violence_threat":
                            data2 = 'selected_tag_types=%5B%22ig_violence_threat%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_violence_parent%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22733f16ef-b9df-4668-8ceb-9073a9c2bcaf%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2272f87812-900c-4bec-a5b1-a559712f5bca%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif self.reptp == "ig_drugs_v3":
                            data2 = 'selected_tag_types=%5B%22'+self.reptp+'%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.maintp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22733f16ef-b9df-4668-8ceb-9073a9c2bcaf%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2272f87812-900c-4bec-a5b1-a559712f5bca%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif self.reptp == 'ig_bullying_or_harassment_comment_v3':
                            data2 = '_csrftoken=missing&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_bullying_or_harassment_comment_v3%22%2C%22ig_bullying_or_harassment_me_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%229ca7699f-2763-4a4e-92cc-61035dd2efba%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_bullying_or_harassment_comment_v3%5C%5C%5C%22%2C%5C%5C%5C%22ig_bullying_or_harassment_me_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22b247c39d-0c46-479a-ab9b-3416f22708cd%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif self.reptp == 'ig_nudity_or_pornography_v3':

                            data2 = 'selected_tag_types=%5B%22'+self.reptp+'%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.maintp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22733f16ef-b9df-4668-8ceb-9073a9c2bcaf%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2272f87812-900c-4bec-a5b1-a559712f5bca%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif self.reptp == 'ig_user_impersonation_me':

                            data2 = 'selected_tag_types=%5B%22'+self.reptp+'%22%5D&_csrftoken=missing&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.maintp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22733f16ef-b9df-4668-8ceb-9073a9c2bcaf%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2272f87812-900c-4bec-a5b1-a559712f5bca%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif self.reptp == 'ig_firearms_v3':

                            data2 = 'selected_tag_types=%5B%22'+self.reptp+'%22%5D&_csrftoken=missing&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22'+self.maintp+'%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22733f16ef-b9df-4668-8ceb-9073a9c2bcaf%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2272f87812-900c-4bec-a5b1-a559712f5bca%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif self.reptp == 'ig_animal_abuse':
                            data2 = 'selected_tag_types=%5B%22ig_animal_abuse%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_violence_parent%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_profile%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22733f16ef-b9df-4668-8ceb-9073a9c2bcaf%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22user_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+target_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2272f87812-900c-4bec-a5b1-a559712f5bca%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        req2 = self.r.post('https://i.instagram.com/api/v1/reports/get_frx_prompt/',
                                           headers=self.headers, cookies=cki, data=data2)

                        if '"status":"ok"' in req2.text:
                            self.done += 1
                        else:
                            self.error += 1

                        self.dnlab.setText(f'DONE : {self.done}')
                        self.erlab.setText(f"ERROR : {self.error}")
                        time.sleep(5)
        except:
            autopy.alert.alert("Action Blocked","Error")
    def story_get(self):
        for idd in self.targets:
            urlstrinfo = f"https://i.instagram.com/api/v1/feed/user/{idd}/story/"
            try:
                reqstr = self.r.get(
                    urlstrinfo, headers=self.headers, cookies=random.choice(self.cookies)).json()
                for item in reqstr['reel']['items']:
                    strid = item['id']
                    self.ids.append(strid)
                idcnt = len(self.ids)
                self.cntstr.setText(f"STORIES LOADED : {idcnt}")
            except Exception as e:
                autopy.alert.alert(f"No Stories Found", "error")
            threading.Thread(target=self.report_story).start()

    def report_story(self):
        listrep = ['spam', 'self', 'hate', 'sex', 'drugs', 'bully', 'violence']
        try:
            while True:
                for cki in self.cookies:
                    for ides in self.ids:
                        data1 = {
                            'object_id': ides,
                            'object_type': '1',
                            'entry_point': 1,
                            '_csrftoken': 'missing',
                            '_uuid': self.uid,
                            'is_dark_mode': 'true',
                            'frx_prompt_request_type': 1,
                            'container_module': 'reel_feed_timeline',
                            'location': 4,
                        }
                        response = requests.post(
                            'https://i.instagram.com/api/v1/reports/get_frx_prompt/', headers=self.headers, cookies=cki, data=data1)
                        if response.status_code != 200:
                            continue
                        reporter_id = response.json(
                        )['response']['report_info']['reporter_id']

                        responsible_id = response.json(
                        )['response']['report_info']['responsible_id']
                        aaaaa = json.loads(response.json()['response']['context'])
                        jj = json.loads(aaaaa['ixt_context_from_www'])
                        cc = json.loads(jj['session'])
                        mapp = cc['extra_data']['sentry_feature_map']
                        for reptp in listrep:
                            if reptp == 'spam':
                                data = 'selected_tag_types=%5B%22ig_spam_v3%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22be323b89-da93-47d9-b282-9bddb8e8b744%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                    mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22824a4969-e246-4bb5-b73d-ec30c48d9d07%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2'

                            elif reptp == 'self':
                                data = '_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_self_injury_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%229ee46817-c0a4-412b-96de-1a32238bcd96%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_self_injury_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                    mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2269a3c637-3108-40a5-bc1c-b58cb600cf05%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                            elif reptp == 'hate':
                                data = '_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_hate_speech_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22f20c6f72-d723-47da-a81d-b4d42b07fd64%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_hate_speech_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                    mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22355a7461-2301-4aea-a61e-b45cb73a3a6f%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                            elif reptp == 'sex':

                                data = 'selected_tag_types=%5B%22ig_nudity_or_pornography_v3%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_nudity_v2%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22bc39e59d-33a4-415c-842f-0599d0aa5f7c%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_nudity_v2%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                    mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22a1c1849b-7655-4e81-be3f-7b3cefec8fb5%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                            elif reptp == 'drugs':

                                data = 'selected_tag_types=%5B%22ig_drugs_alcohol_tobacco%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_sale_of_illegal_or_regulated_goods_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22c85d2333-1696-4829-b934-fa56db7f1d1c%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_sale_of_illegal_or_regulated_goods_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides + \
                                    '%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                    '%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2239e1c844-c6b7-4ff1-90d8-4a881a12be34%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                            elif reptp == 'bully':

                                data = '_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_bullying_or_harassment_comment_v3%22%2C%22ig_bullying_or_harassment_me_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2233268cbf-02ab-4bf0-b1f8-08ff80c4c701%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_bullying_or_harassment_comment_v3%5C%5C%5C%22%2C%5C%5C%5C%22ig_bullying_or_harassment_me_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                    mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22b81ee6e8-9612-43de-8150-329f015a0e48%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                            elif reptp == 'violence':

                                data = 'selected_tag_types=%5B%22ig_violence_threat%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_violence_parent%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%226e184ac5-b80e-416a-b34b-91577453d94c%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                    mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2274dd68bc-3cfd-42d2-8268-4b2a6e808958%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                            response = self.r.post(
                                'https://i.instagram.com/api/v1/reports/get_frx_prompt/', data=data, headers=self.headers, cookies=cki)

                            if '"status":"ok"' in response.text:
                                self.done += 1

                            elif '"status":"fail"' in response.text:
                                self.bndstr += 1
                                self.cntbnd.setText(
                                    f"STORIES BANNED : {self.bndstr}")
                            else:
                                self.error += 1
                            self.dnlab.setText(f'DONE : {self.done}')
                            self.erlab.setText(f"ERROR : {self.error}")
                            time.sleep(1)
        except:
            autopy.alert.alert("Action Blocked","Error")

    def get_highligts(self):
        for target in self.targets:

            url_1 = f'https://i.instagram.com/api/v1/highlights/{target}/highlights_tray/?supported_capabilities_new=%5B%7B%22name%22%3A%22SUPPORTED_SDK_VERSIONS%22%2C%22value%22%3A%2266.0%2C67.0%2C68.0%2C69.0%2C70.0%2C71.0%2C72.0%2C73.0%2C74.0%2C75.0%2C76.0%2C77.0%2C78.0%2C79.0%2C80.0%2C81.0%2C82.0%2C83.0%2C84.0%2C85.0%2C86.0%2C87.0%2C88.0%2C89.0%2C90.0%2C91.0%2C92.0%2C93.0%22%7D%2C%7B%22name%22%3A%22FACE_TRACKER_VERSION%22%2C%22value%22%3A%2214%22%7D%2C%7B%22name%22%3A%22segmentation%22%2C%22value%22%3A%22segmentation_enabled%22%7D%2C%7B%22name%22%3A%22COMPRESSION%22%2C%22value%22%3A%22ETC2_COMPRESSION%22%7D%2C%7B%22name%22%3A%22world_tracker%22%2C%22value%22%3A%22world_tracker_enabled%22%7D%2C%7B%22name%22%3A%22gyroscope%22%2C%22value%22%3A%22gyroscope_enabled%22%7D%5D&phone_id=d3955bef-f143-4ebd-854b-9cbda044b0b1&battery_level=65&is_charging=1&is_dark_mode=1&will_sound_on=0'
            req_get = self.r.get(
                url_1, headers=self.headers, cookies=random.choice(self.cookies))
            for i in req_get.json()['tray']:
                reel_id = (i['id'])
                url_get_str = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={reel_id}'
                req_get_str = self.r.get(
                    url=url_get_str, cookies=random.choice(self.cookies), headers=self.headers)
                for s in req_get_str.json()['reels'][reel_id]['items']:
                    idd = (s['id'])
                    self.reels_id.append(idd)

        threading.Thread(target=self.report_highlights).start()

    def report_highlights(self):
        try:
            while True:
                for cki in self.cookies:
                    for idd in self.reels_id:
                        data1 = {
                            'object_id': idd,
                            'object_type': '1',
                            'entry_point': 1,
                            '_csrftoken': 'missing',
                            '_uuid': self.uid,
                            'is_dark_mode': 'true',
                            'frx_prompt_request_type': 1,
                            'container_module': 'reel_highlight_profile',
                            'location': 4,
                        }
                        response = requests.post(
                            'https://i.instagram.com/api/v1/reports/get_frx_prompt/', headers=self.headers, cookies=cki, data=data1)
                        if response.status_code != 200:
                            continue
                        reporter_id = response.json(
                        )['response']['report_info']['reporter_id']

                        responsible_id = response.json(
                        )['response']['report_info']['responsible_id']
                        aaaaa = json.loads(response.json()['response']['context'])
                        jj = json.loads(aaaaa['ixt_context_from_www'])
                        cc = json.loads(jj['session'])
                        mapp = cc['extra_data']['sentry_feature_map']

                        if self.reptp == 'ig_spam_v3':
                            data = 'selected_tag_types=%5B%22ig_spam_v3%22%5D&_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22e278d97f-506f-4a71-9dac-c2c9dafa209a%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22c4e232a3-8952-4b1e-82f9-bdada4c8cc93%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2'

                        elif self.reptp == 'ig_self_injury_v3':

                            data = '_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_self_injury_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22fc586124-f132-4430-9ef2-e6662d466856%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_self_injury_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%229b3d4617-9dca-45f6-8b5a-8456b95e29de%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'
                        elif 'hate' in self.reptp:
                            data = '_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_hate_speech_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2220c9417e-877c-4aa3-b831-a0298fa29a95%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_hate_speech_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%222'+mapp + \
                                '%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22b2a02742-97f5-4292-a190-07a58c2ce2af%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif self.reptp == 'ig_hate_speech_v3':
                            data = 'selected_tag_types=%5B%22ig_product_scam_fraud_v2%22%5D&_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%221267fd84-35e1-46ec-977a-f6c6ec08149c%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22240acebe-4c1d-4dd2-b353-e001e516fc54%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2'
                        elif 'ig_false_news' in self.reptp:
                            data = '_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&selected_tag_type=ig_misinformation_social_issue&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_false_news%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2219f09f1b-8e26-4e63-bc6d-0accf849945d%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_false_news%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22361d40ea-1e87-4938-a489-30190c165e16%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D'
                        elif 'ig_violence_threat' in self.reptp:
                            data = 'selected_tag_types=%5B%22ig_violence_threat%22%5D&_csrftoken=9NC5I9yI8PonLhQFCjMI4wefqaw4YgJ1&_uuid=bc19975f-7663-4346-a758-4d6025eb301a&context=%7B%22tags%22%3A%5B%22ig_violence_parent%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%229513cfa1-84d8-44ee-8f31-22ec3e7fff10%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjQWhu6HjQwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22ef1c4aa8-7574-4dc1-8344-21d1e3b78c6a%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif 'ig_drugs_v3' in self.reptp:
                            data = 'selected_tag_types=%5B%22ig_drugs_v3%22%5D&_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_sale_of_illegal_or_regulated_goods_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2247976d4c-298f-4c38-8bec-3011bee31691%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_sale_of_illegal_or_regulated_goods_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%223298e155-4028-4ae1-b0f6-8cd309aff4bc%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif 'ig_bullying_or_harassment_comment_v3' in self.reptp:
                            data = '_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_bullying_or_harassment_comment_v3%22%2C%22ig_bullying_or_harassment_me_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22a82f08cd-9e58-465d-98f9-adeda2f243cc%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_bullying_or_harassment_comment_v3%5C%5C%5C%22%2C%5C%5C%5C%22ig_bullying_or_harassment_me_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2252e74737-2218-4608-a9a9-63d7a2b56ce8%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif 'ig_nudity_or_pornography_v3' in self.reptp:
                            data = 'selected_tag_types=%5B%22ig_nudity_or_pornography_v3%22%5D&_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_nudity_v2%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%228390b963-bac6-4dac-825c-5d14c2603e38%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_nudity_v2%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22d3b2a1bd-12e0-46ee-814d-c96dc4e48f0f%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'
                        elif 'ig_firearms_v3' in self.reptp:
                            data = 'selected_tag_types=%5B%22ig_firearms_v3%22%5D&_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_sale_of_illegal_or_regulated_goods_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2247976d4c-298f-4c38-8bec-3011bee31691%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_sale_of_illegal_or_regulated_goods_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%223298e155-4028-4ae1-b0f6-8cd309aff4bc%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'
                        elif 'ig_animal_abuse' in self.reptp:
                            data = 'selected_tag_types=%5B%22ig_animal_abuse%22%5D&_csrftoken=zwWpxdimxgli492MR4eYJ6xwRobkgSXI&_uuid=ed0e63e9-1663-4c54-b150-40d726c30a87&context=%7B%22tags%22%3A%5B%22ig_violence_parent%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%229379e13c-a1b1-4c6e-aca8-d7ce561d0933%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+idd+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                                '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                '%2Bvulpp70tj8YQGExN2JjZGRjMDI1MTY0ZmYxNGY5MzY1NzhkMzQ1ZmU2ZDdhYTUxNWIxOTRlYzQ4ODY1OTNlM2UzZTNkODI5ZWIAHBUAABIAFv7lvKD9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFjoWpLb7jAwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_highlight_profile%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2237b05adb-a063-469b-8fe3-e4f762167e26%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        response = self.r.post(
                            'https://i.instagram.com/api/v1/reports/get_frx_prompt/', data=data, headers=self.headers, cookies=cki)

                        if '"status":"ok"' in response.text:
                            self.done += 1
                        else:
                            self.error += 1
                        self.dnlab.setText(f'DONE : {self.done}')
                        self.erlab.setText(f"ERROR : {self.error}")
                        time.sleep(1)
        except:
            autopy.alert.alert("Action Blocked","Error")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyApp()
    MyApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
