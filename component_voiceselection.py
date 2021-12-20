import PyQt5
import logging
import constants
import voice

class SelectedVoiceOptionBase():
    def __init__(self, voice_with_options):
        self.voice_with_options = voice_with_options
    
class SelectedVoiceOptionRandom(SelectedVoiceOptionBase):
    def draw(self, grid_layout, row):
        grid_layout.addWidget(PyQt5.QtWidgets.QLabel(str(self.voice_with_options)), row, 0, 1, 1)

class SelectedVoiceOptionPriority(SelectedVoiceOptionBase):
    def draw(self, grid_layout, row):
        pass


class ComponentVoiceListBase():
    def __init__(self):
        self.voice_with_option_list = []

class ComponentRandomVoiceList(ComponentVoiceListBase):
    def __init__(self):
        ComponentVoiceListBase.__init__(self)
        self.widget = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QVBoxLayout(self.widget)
        self.layout.addWidget(PyQt5.QtWidgets.QLabel('Voice List (Random)'))

    def draw(self, layout):
        
        # buttons

        self.voice_list_grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.layout.addLayout(self.voice_list_grid_layout)

        # add ourselves to the parent
        layout.addWidget(self.widget)
        self.widget.setVisible(False)

    def add_voice_with_options(self, voice_with_options):
        logging.info('add_voice_with_options')
        row = len(self.voice_with_option_list)
        self.voice_with_option_list.append(voice_with_options)
        self.voice_list_grid_layout.addWidget(PyQt5.QtWidgets.QLabel(str(voice_with_options)), row, 0, 1, 1)

    def clear_voices(self):
        logging.info('clear_voices')
        # remove everything from layout self.voice_mode_random_voice_list
        for i in reversed(range(self.voice_list_grid_layout.count())): 
            self.voice_list_grid_layout.itemAt(i).widget().setParent(None)
        self.selected_random_voice_list = []
        self.selected_priority_voice_list = []

    def setVisible(self, visible):
        self.widget.setVisible(visible)

class VoiceSelection():
    def __init__(self, hypertts):
        self.hypertts = hypertts

    def get_voices(self):
        self.voice_list = self.hypertts.service_manager.full_voice_list()

        languages = set()
        audio_languages = set()
        services = set()
        genders = set()

        for voice in self.voice_list:
            audio_languages.add(voice.language)
            languages.add(voice.language.lang)
            services.add(voice.service.name)
            genders.add(voice.gender)

        self.audio_languages = list(audio_languages)
        self.languages = list(languages)
        self.services = list(services)
        self.genders = list(genders)

        self.component_random_voice_list = ComponentRandomVoiceList()

    def populate_combobox(self, combobox, items):
        combobox.addItem(constants.LABEL_FILTER_ALL)
        combobox.insertSeparator(1)
        combobox.addItems(items)

    def draw(self, layout):
        # filters:
        # - language
        # - locale
        # - service
        # - gender

        # 1. get full voice list
        # 2. iterate over the list, gather attributes
        # 3. populate filters
        # 4. draw all voices


        self.get_voices()

        self.voices_layout = PyQt5.QtWidgets.QVBoxLayout()
        layout.addLayout(self.voices_layout)

        self.audio_languages_combobox = PyQt5.QtWidgets.QComboBox()
        self.languages_combobox = PyQt5.QtWidgets.QComboBox()
        self.services_combobox = PyQt5.QtWidgets.QComboBox()
        self.genders_combobox = PyQt5.QtWidgets.QComboBox()
        self.voices_combobox = PyQt5.QtWidgets.QComboBox()

        self.reset_filters_button = PyQt5.QtWidgets.QPushButton('Reset Filters')

        self.populate_combobox(self.audio_languages_combobox, [audio_lang.audio_lang_name for audio_lang in self.audio_languages])
        self.populate_combobox(self.languages_combobox, [language.lang_name for language in self.languages])
        self.populate_combobox(self.services_combobox, self.services)
        self.populate_combobox(self.genders_combobox, [gender.name for gender in self.genders])

        self.voices_layout.addWidget(self.audio_languages_combobox)
        self.voices_layout.addWidget(self.languages_combobox)
        self.voices_layout.addWidget(self.services_combobox)
        self.voices_layout.addWidget(self.genders_combobox)
        self.voices_layout.addWidget(self.reset_filters_button)
        self.voices_layout.addWidget(self.voices_combobox)

        self.voice_options_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.voices_layout.addLayout(self.voice_options_layout)


        # voice selection mode
        # ====================
        mode_group = PyQt5.QtWidgets.QButtonGroup()
        self.radio_button_single = PyQt5.QtWidgets.QRadioButton('Single')
        self.radio_button_random = PyQt5.QtWidgets.QRadioButton('Random')
        self.radio_button_priority = PyQt5.QtWidgets.QRadioButton('Priority')
        mode_group.addButton(self.radio_button_single)
        mode_group.addButton(self.radio_button_random)
        mode_group.addButton(self.radio_button_priority)
        #self.voices_layout.addWidget(mode_group)
        self.voices_layout.addWidget(self.radio_button_single)
        self.voices_layout.addWidget(self.radio_button_random)
        self.voices_layout.addWidget(self.radio_button_priority)


        # buttons
        # =======

        self.add_voice_button = PyQt5.QtWidgets.QPushButton('Add Voice')
        self.clear_voices_button = PyQt5.QtWidgets.QPushButton('Remove all Voices')

        self.voices_layout.addWidget(self.add_voice_button)
        self.voices_layout.addWidget(self.clear_voices_button)

        # additional layouts screens for the various modes
        # ================================================

        self.component_random_voice_list.draw(self.voices_layout)

        # # random selection mode
        # # ---------------------

        # self.voice_mode_random_widget = PyQt5.QtWidgets.QWidget()
        # self.voice_mode_random_layout = PyQt5.QtWidgets.QVBoxLayout(self.voice_mode_random_widget)
        # self.voice_mode_random_layout.addWidget(PyQt5.QtWidgets.QLabel('Voice List (Random)'))
        
        # # buttons
        # self.voice_mode_random_add_button = PyQt5.QtWidgets.QPushButton('Add Voice')
        # self.voice_mode_random_layout.addWidget(self.voice_mode_random_add_button)
        # self.voice_mode_random_clear_button = PyQt5.QtWidgets.QPushButton('Remove all Voices')
        # self.voice_mode_random_layout.addWidget(self.voice_mode_random_clear_button)
        # self.voice_mode_random_add_button.pressed.connect(self.add_voice_random)
        # self.voice_mode_random_clear_button.pressed.connect(self.clear_voices)

        # self.voice_mode_random_voice_list = PyQt5.QtWidgets.QGridLayout()
        # self.voice_mode_random_layout.addLayout(self.voice_mode_random_voice_list)

        # self.voices_layout.addWidget(self.voice_mode_random_widget)
        # self.voice_mode_random_widget.setVisible(False)

        # # priority selection mode
        # # -----------------------

        # self.voice_mode_priority_widget = PyQt5.QtWidgets.QWidget()
        # self.voice_mode_priority_layout = PyQt5.QtWidgets.QVBoxLayout(self.voice_mode_priority_widget)
        # self.voice_mode_priority_layout.addWidget(PyQt5.QtWidgets.QLabel('Voice List (Priority)'))

        # self.voice_mode_priority_add_button = PyQt5.QtWidgets.QPushButton('Add Voice')
        # self.voice_mode_priority_layout.addWidget(self.voice_mode_priority_add_button)

        # self.voices_layout.addWidget(self.voice_mode_priority_widget)
        # self.voice_mode_priority_widget.setVisible(False)
        
        # wire all events
        # ===============

        self.audio_languages_combobox.currentIndexChanged.connect(self.filter_and_draw_voices)
        self.languages_combobox.currentIndexChanged.connect(self.filter_and_draw_voices)
        self.services_combobox.currentIndexChanged.connect(self.filter_and_draw_voices)
        self.genders_combobox.currentIndexChanged.connect(self.filter_and_draw_voices)

        self.voices_combobox.currentIndexChanged.connect(self.voice_selected)

        self.reset_filters_button.pressed.connect(self.reset_filters)

        self.radio_button_single.toggled.connect(self.voice_selection_mode_change)
        self.radio_button_random.toggled.connect(self.voice_selection_mode_change)
        self.radio_button_priority.toggled.connect(self.voice_selection_mode_change)

        self.add_voice_button.pressed.connect(self.add_voice)
        self.clear_voices_button.pressed.connect(self.clear_voices)

        self.filter_and_draw_voices(0)

    def voice_selection_mode_change(self):
        if self.radio_button_single.isChecked():
            self.component_random_voice_list.setVisible(False)
            self.voice_mode_priority_widget.setVisible(False)
        elif self.radio_button_random.isChecked():
            self.component_random_voice_list.setVisible(True)
            self.voice_mode_priority_widget.setVisible(False)
        elif self.radio_button_priority.isChecked():
            self.component_random_voice_list.setVisible(False)
            self.voice_mode_priority_widget.setVisible(True)

    def reset_filters(self):
        self.audio_languages_combobox.setCurrentIndex(0)
        self.languages_combobox.setCurrentIndex(0)
        self.services_combobox.setCurrentIndex(0)
        self.genders_combobox.setCurrentIndex(0)


    def add_voice(self):
        selected_voice = self.filtered_voice_list[self.voices_combobox.currentIndex()]
        options = self.current_voice_options
        voice_with_options = voice.VoiceWithOptions(selected_voice, options)

        self.component_random_voice_list.add_voice_with_options(voice_with_options)


    def clear_voices(self):
        self.component_random_voice_list.clear_voices()

    def add_voice_random(self):

        self.component_random_voice_list.add_voice_with_options(voice_with_options)

        self.selected_random_voice_list.append(SelectedVoiceOptionRandom(voice_with_options))

        # draw the last item
        self.selected_random_voice_list[-1].draw(self.voice_mode_random_voice_list, len(self.selected_random_voice_list))

    def voice_selected(self, current_index):
        voice = self.filtered_voice_list[current_index]
        logging.info(f'voice_selected: {voice} options: {voice.options}')

        # clear the options layout
        for i in reversed(range(self.voice_options_layout.count())): 
            self.voice_options_layout.itemAt(i).widget().setParent(None)

        # clear the current voice options
        self.current_voice_options = {}

        def get_set_option_lambda(key):
            def set_value(value):
                self.current_voice_options[key] = value
                logging.info(f'set option {key} to {value}')
            return set_value

        # populate voice options layout
        for key, value in voice.options.items():
            widget_name = f'voice_option_{key}'
            option_type = constants.VoiceOptionTypes[value['type']]
            if option_type == constants.VoiceOptionTypes.number:
                # create a spinner
                widget = PyQt5.QtWidgets.QDoubleSpinBox()
                widget.setObjectName(widget_name)
                widget.setRange(value['min'], value['max'])
                widget.setValue(value['default'])
                widget.valueChanged.connect(get_set_option_lambda(key))
                self.voice_options_layout.addWidget(widget)
            else:
                raise Exception(f"voice option type not supported: {value['type']}")

        
    def filter_and_draw_voices(self, current_index):
        logging.info('filter_and_draw_voices')
        voice_list = self.voice_list
        # check filtering by audio language
        if self.audio_languages_combobox.currentIndex() != 0:
            audio_language = self.audio_languages[self.audio_languages_combobox.currentIndex() - 2]
            voice_list = [voice for voice in voice_list if voice.language == audio_language]
        # check filtering by language
        if self.languages_combobox.currentIndex() != 0:
            language = self.languages[self.languages_combobox.currentIndex() - 2]
            voice_list = [voice for voice in voice_list if voice.language.lang == language]
        # check filtering by service
        if self.services_combobox.currentIndex() != 0:
            service = self.services[self.services_combobox.currentIndex() - 2]
            voice_list = [voice for voice in voice_list if voice.service.name == service] 
        # check filtering by gender
        if self.genders_combobox.currentIndex() != 0:
            gender = self.genders[self.genders_combobox.currentIndex() - 2]
            voice_list = [voice for voice in voice_list if voice.gender == gender]
        self.filtered_voice_list = voice_list
        self.draw_all_voices(self.filtered_voice_list)

    def draw_all_voices(self, voice_list):
        self.voices_combobox.clear()
        self.voices_combobox.addItems([str(voice) for voice in voice_list])
