import PyQt5
import logging
import component_batch_preview
import config_models
import servicemanager
import testing_utils
import hypertts
import constants
import component_voiceselection
import component_source
import component_target
import component_batch

class EmptyDialog(PyQt5.QtWidgets.QDialog):
    def __init__(self):
        super(PyQt5.QtWidgets.QDialog, self).__init__()

    def setupUi(self):
        self.main_layout = PyQt5.QtWidgets.QVBoxLayout(self)

    def getLayout(self):
        return self.main_layout

    def setLayout(self, layout):
        self.main_layout = layout

    def addChildLayout(self, layout):
        self.main_layout.addLayout(layout)

class MockModelChangeCallback():
    def __init__(self):
        self.model = None

    def model_updated(self, model):
        self.model = model

def get_hypertts_instance():
    # return hypertts_instance    
    config_gen = testing_utils.TestConfigGenerator()
    return config_gen.build_hypertts_instance_test_servicemanager('default')


def test_voice_selection_defaults_single(qtbot):
    hypertts_instance = get_hypertts_instance()

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    # voiceselection.voices_combobox.setCurrentIndex(1) # pick second voice
    expected_output = {
        'voice_selection_mode': 'single',
        'voice': {
            'voice': {
                'gender': 'Male', 
                'language': 'fr_FR',
                'name': 'voice_a_1', 
                'service': 'ServiceA',
                'voice_key': {'name': 'voice_1'}
            },
            'options': {
            }
        }        
    }

    assert voiceselection.serialize() == expected_output

    # dialog.exec_()
    
def test_voice_selection_single_1(qtbot):
    hypertts_instance = get_hypertts_instance()

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    voiceselection.voices_combobox.setCurrentIndex(1) # pick second voice

    # dialog.exec_()

    expected_output = {
        'voice_selection_mode': 'single',
        'voice': {
            'voice': {
                'gender': 'Female', 
                'language': 'en_US',
                'name': 'voice_a_2', 
                'service': 'ServiceA',
                'voice_key': {'name': 'voice_2'}
            },
            'options': {
            }
        }        
    }
    assert voiceselection.serialize() == expected_output    

    # change options
    speaking_rate_widget = dialog.findChild(PyQt5.QtWidgets.QDoubleSpinBox, "voice_option_speaking_rate")
    speaking_rate_widget.setValue(0.25)

    expected_output = {
        'voice_selection_mode': 'single',
        'voice': {
            'voice': {
                'gender': 'Female', 
                'language': 'en_US',
                'name': 'voice_a_2', 
                'service': 'ServiceA',
                'voice_key': {'name': 'voice_2'}
            },
            'options': {
                'speaking_rate': 0.25
            }
        }        
    }
    assert voiceselection.serialize() == expected_output        

def test_voice_selection_random_1(qtbot):
    hypertts_instance = get_hypertts_instance()

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    # choose random mode
    # qtbot.mouseClick(voiceselection.radio_button_random, PyQt5.QtCore.Qt.LeftButton)
    voiceselection.radio_button_random.setChecked(True)

    # pick second voice and add it
    voiceselection.voices_combobox.setCurrentIndex(1) # pick second voice
    qtbot.mouseClick(voiceselection.add_voice_button, PyQt5.QtCore.Qt.LeftButton)

    # pick third voice and add it
    voiceselection.voices_combobox.setCurrentIndex(2) # pick second voice
    qtbot.mouseClick(voiceselection.add_voice_button, PyQt5.QtCore.Qt.LeftButton)    

    expected_output = {
        'voice_selection_mode': 'random',
        'voice_list': [
            {
                'voice': {
                    'gender': 'Female', 
                    'language': 'en_US',
                    'name': 'voice_a_2', 
                    'service': 'ServiceA',
                    'voice_key': {'name': 'voice_2'}
                },
                'options': {
                },
                'weight': 1
            },
            {
                'voice': {
                    'gender': 'Female', 
                    'language': 'ja_JP',
                    'name': 'voice_a_3', 
                    'service': 'ServiceA',
                    'voice_key': {'name': 'voice_3'}
                },
                'options': {
                },
                'weight': 1
            }            
        ]
    }
    assert voiceselection.serialize() == expected_output    

def test_voice_selection_random_2(qtbot):
    hypertts_instance = get_hypertts_instance()

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    # choose random mode
    voiceselection.radio_button_random.setChecked(True)

    # add the first voice twice, but with different options
    voiceselection.voices_combobox.setCurrentIndex(0)
    qtbot.mouseClick(voiceselection.add_voice_button, PyQt5.QtCore.Qt.LeftButton)

    # change options
    speaking_rate_widget = dialog.findChild(PyQt5.QtWidgets.QDoubleSpinBox, "voice_option_speaking_rate")
    speaking_rate_widget.setValue(0.25)    

    # add again
    qtbot.mouseClick(voiceselection.add_voice_button, PyQt5.QtCore.Qt.LeftButton)

    # build expected voice selection model
    expected_model = config_models.VoiceSelectionRandom()
    voice = [x for x in hypertts_instance.service_manager.full_voice_list() if x.service.name == 'ServiceA' and x.name == 'voice_a_1'][0]

    expected_model.add_voice(config_models.VoiceWithOptionsRandom(voice, {}))
    expected_model.add_voice(config_models.VoiceWithOptionsRandom(voice, {'speaking_rate': 0.25}))    

    assert voiceselection.voice_selection_model.serialize() == expected_model.serialize()


def test_voice_selection_priority_1(qtbot):
    hypertts_instance = get_hypertts_instance()

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    # choose random mode
    # qtbot.mouseClick(voiceselection.radio_button_random, PyQt5.QtCore.Qt.LeftButton)
    voiceselection.radio_button_priority.setChecked(True)

    # dialog.exec_()

    # pick second voice and add it
    voiceselection.voices_combobox.setCurrentIndex(1) # pick second voice
    qtbot.mouseClick(voiceselection.add_voice_button, PyQt5.QtCore.Qt.LeftButton)

    # pick third voice and add it
    voiceselection.voices_combobox.setCurrentIndex(2) # pick second voice
    qtbot.mouseClick(voiceselection.add_voice_button, PyQt5.QtCore.Qt.LeftButton)    

    expected_model = config_models.VoiceSelectionPriority()
    voice_2 = [x for x in hypertts_instance.service_manager.full_voice_list() if x.service.name == 'ServiceA' and x.name == 'voice_a_2'][0]
    voice_3 = [x for x in hypertts_instance.service_manager.full_voice_list() if x.service.name == 'ServiceA' and x.name == 'voice_a_3'][0]

    expected_model.add_voice(config_models.VoiceWithOptionsPriority(voice_2, {}))
    expected_model.add_voice(config_models.VoiceWithOptionsPriority(voice_3, {}))

    assert voiceselection.voice_selection_model.serialize() == expected_model.serialize()

    # dialog.exec_()


def test_voice_selection_filters(qtbot):
    manager = servicemanager.ServiceManager(testing_utils.get_test_services_dir(), 'test_services')
    manager.init_services()
    manager.get_service('ServiceA').set_enabled(True)
    manager.get_service('ServiceB').set_enabled(True)
    anki_utils = testing_utils.MockAnkiUtils({})

    hypertts_instance = hypertts.HyperTTS(anki_utils, manager)

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    # ensure filters are set to All by default
    assert voiceselection.audio_languages_combobox.currentText() == constants.LABEL_FILTER_ALL
    assert voiceselection.languages_combobox.currentText() == constants.LABEL_FILTER_ALL
    assert voiceselection.services_combobox.currentText() == constants.LABEL_FILTER_ALL
    assert voiceselection.genders_combobox.currentText() == constants.LABEL_FILTER_ALL

    # filter language to Japanese
    voiceselection.languages_combobox.setCurrentText('Japanese')

    # ensure japanese filter is enabled
    assert len(voiceselection.filtered_voice_list) < len(voiceselection.voice_list)
    assert len(voiceselection.filtered_voice_list) == voiceselection.voices_combobox.count()
    for voice in voiceselection.filtered_voice_list:
        assert voice.language.lang == constants.Language.ja

    # reset filters
    qtbot.mouseClick(voiceselection.reset_filters_button, PyQt5.QtCore.Qt.LeftButton)

    # ensure all voices are available now
    assert len(voiceselection.filtered_voice_list) == len(voiceselection.voice_list)

    # filter gender to male
    voiceselection.genders_combobox.setCurrentText('Male')

    # ensure only male voices appear
    assert len(voiceselection.filtered_voice_list) < len(voiceselection.voice_list)
    assert len(voiceselection.filtered_voice_list) == voiceselection.voices_combobox.count()
    for voice in voiceselection.filtered_voice_list:
        assert voice.gender == constants.Gender.Male

    # reset filters again
    qtbot.mouseClick(voiceselection.reset_filters_button, PyQt5.QtCore.Qt.LeftButton)
    # ensure all voices are available now
    assert len(voiceselection.filtered_voice_list) == len(voiceselection.voice_list)
    
    # filter with two different conditions
    voiceselection.languages_combobox.setCurrentText('Japanese')
    voiceselection.genders_combobox.setCurrentText('Female')

    # ensure only female japanese voices are present
    assert len(voiceselection.filtered_voice_list) < len(voiceselection.voice_list)
    assert len(voiceselection.filtered_voice_list) == voiceselection.voices_combobox.count()
    for voice in voiceselection.filtered_voice_list:
        assert voice.gender == constants.Gender.Female
        assert voice.language.lang == constants.Language.ja

    # reset filters again
    qtbot.mouseClick(voiceselection.reset_filters_button, PyQt5.QtCore.Qt.LeftButton)    

    # select random mode and add some voices
    # ======================================


    # dialog.exec_()

def test_voice_selection_samples(qtbot):
    hypertts_instance = get_hypertts_instance()

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    # simulate selection from the preview grid
    voiceselection.sample_text_selected('Bonjour')

    qtbot.mouseClick(voiceselection.play_sample_button, PyQt5.QtCore.Qt.LeftButton)

    assert hypertts_instance.anki_utils.played_sound == {
        'source_text': 'Bonjour',
        'voice': {
            'gender': 'Male', 
            'language': 'fr_FR', 
            'name': 'voice_a_1', 
            'service': 'ServiceA',
            'voice_key': {'name': 'voice_1'}
        },
        'options': {}
    }

    # dialog.exec_()

def test_voice_selection_load_model(qtbot):
    hypertts_instance = get_hypertts_instance()

    dialog = EmptyDialog()
    dialog.setupUi()

    model_change_callback = MockModelChangeCallback()
    voiceselection = component_voiceselection.VoiceSelection(hypertts_instance, model_change_callback.model_updated)
    dialog.addChildLayout(voiceselection.draw())

    voice_list = hypertts_instance.service_manager.full_voice_list()
    voice_a_2 = [x for x in voice_list if x.name == 'voice_a_2'][0]
    voice_a_3 = [x for x in voice_list if x.name == 'voice_a_3'][0]

    # single voice
    # ============

    model = config_models.VoiceSelectionSingle()
    model.voice = config_models.VoiceWithOptions(voice_a_2, {'speaking_rate': 3.5})

    voiceselection.load_model(model)

    assert voiceselection.radio_button_single.isChecked()
    assert voiceselection.voices_combobox.currentText() == str(voice_a_2)


    speaking_rate_widget = voiceselection.voice_options_widgets['voice_option_speaking_rate']
    assert speaking_rate_widget != None
    assert speaking_rate_widget.value() == 3.5

    # random
    # =======

    model = config_models.VoiceSelectionRandom()
    model.add_voice(config_models.VoiceWithOptionsRandom(voice_a_2, {'speaking_rate': 2.5}))
    model.add_voice(config_models.VoiceWithOptionsRandom(voice_a_3, {}))

    voiceselection.load_model(model)
    
    assert voiceselection.radio_button_random.isChecked()

    assert voiceselection.voice_list_grid_layout.itemAt(0).widget().text() == str(voice_a_2) + ' (speaking_rate: 2.5)'
    assert voiceselection.voice_list_grid_layout.itemAt(3).widget().text() == str(voice_a_3)

    # priority
    # ========

    model = config_models.VoiceSelectionPriority()
    model.add_voice(config_models.VoiceWithOptionsPriority(voice_a_2, {'speaking_rate': 2.5}))
    model.add_voice(config_models.VoiceWithOptionsPriority(voice_a_3, {}))

    voiceselection.load_model(model)
    
    assert voiceselection.radio_button_priority.isChecked()

    assert voiceselection.voice_list_grid_layout.itemAt(0).widget().text() == str(voice_a_2) + ' (speaking_rate: 2.5)'
    assert voiceselection.voice_list_grid_layout.itemAt(4).widget().text() == str(voice_a_3)    

    # dialog.exec_()





def test_batch_source_1(qtbot):
    config_gen = testing_utils.TestConfigGenerator()
    hypertts_instance = config_gen.build_hypertts_instance_test_servicemanager('default')    

    dialog = EmptyDialog()
    dialog.setupUi()

    note_id_list = [config_gen.note_id_1, config_gen.note_id_2]

    model_change_callback = MockModelChangeCallback()
    field_list = hypertts_instance.get_all_fields_from_notes(note_id_list)
    batch_source = component_source.BatchSource(hypertts_instance, field_list, model_change_callback.model_updated)
    dialog.addChildLayout(batch_source.draw())

    # the field selected should be "Chinese"
    expected_source_model = config_models.BatchSource()
    expected_source_model.mode = constants.BatchMode.simple
    expected_source_model.source_field = 'Chinese'

    assert batch_source.batch_source_model.serialize() == expected_source_model.serialize()

    # select another field, 'English'
    batch_source.source_field_combobox.setCurrentText('English')
    expected_source_model.source_field = 'English'

    assert batch_source.batch_source_model.serialize() == expected_source_model.serialize()

    # select template mode
    batch_source.batch_mode_combobox.setCurrentText('template')

    # enter template format
    qtbot.keyClicks(batch_source.simple_template_input, '{Chinese}')

    expected_source_model = config_models.BatchSource()
    expected_source_model.mode = constants.BatchMode.template
    expected_source_model.source_template = '{Chinese}'
    expected_source_model.template_format_version = constants.TemplateFormatVersion.v1

    assert batch_source.batch_source_model.serialize() == expected_source_model.serialize()

    # load model tests
    # ================
    # the field selected should be "Chinese"
    model = config_models.BatchSource()
    model.mode = constants.BatchMode.simple
    model.source_field = 'English'

    batch_source.load_model(model)

    assert batch_source.batch_mode_combobox.currentText() == 'simple'
    assert batch_source.source_field_combobox.currentText() == 'English'

    model.source_field = 'Chinese'

    batch_source.load_model(model)

    assert batch_source.batch_mode_combobox.currentText() == 'simple'
    assert batch_source.source_field_combobox.currentText() == 'Chinese'

    model.mode = constants.BatchMode.template
    model.source_template = '{English}'
    model.template_format_version = constants.TemplateFormatVersion.v1

    batch_source.load_model(model)

    assert batch_source.batch_mode_combobox.currentText() == 'template'
    assert batch_source.simple_template_input.text() == '{English}'

    # dialog.exec_()

def test_target(qtbot):
    config_gen = testing_utils.TestConfigGenerator()
    hypertts_instance = config_gen.build_hypertts_instance_test_servicemanager('default')    

    dialog = EmptyDialog()
    dialog.setupUi()

    note_id_list = [config_gen.note_id_1, config_gen.note_id_2]

    batch_target = component_target.BatchTarget(hypertts_instance, note_id_list)
    batch_target.draw(dialog.getLayout())

    # pick the Sound field
    batch_target.target_field_combobox.setCurrentText('Sound')

    assert batch_target.batch_target_model.target_field == 'Sound'
    assert batch_target.batch_target_model.text_and_sound_tag == False
    assert batch_target.batch_target_model.remove_sound_tag == True

    # change some options
    batch_target.radio_button_text_sound.setChecked(True)
    assert batch_target.batch_target_model.text_and_sound_tag == True

    batch_target.radio_button_keep_sound.setChecked(True)
    assert batch_target.batch_target_model.remove_sound_tag == False

    # load model tests
    # ================

    model = config_models.BatchTarget('Chinese', False, True)
    batch_target.load_model(model)

    assert batch_target.target_field_combobox.currentText() == 'Chinese'
    assert batch_target.radio_button_sound_only.isChecked() == True
    assert batch_target.radio_button_remove_sound.isChecked() == True

    model = config_models.BatchTarget('Pinyin', True, True)
    batch_target.load_model(model)

    assert batch_target.target_field_combobox.currentText() == 'Pinyin'
    assert batch_target.radio_button_sound_only.isChecked() == False
    assert batch_target.radio_button_remove_sound.isChecked() == True

def test_batch_preview(qtbot):

    config_gen = testing_utils.TestConfigGenerator()
    hypertts_instance = config_gen.build_hypertts_instance_test_servicemanager('default')

    # configure delay on service A
    # hypertts_instance.service_manager.get_service('ServiceA').configure({'delay': 1.0})

    dialog = EmptyDialog()
    dialog.setupUi()

    note_id_list = [config_gen.note_id_1, config_gen.note_id_2]    

    voice_list = hypertts_instance.service_manager.full_voice_list()

    voice_a_1 = [x for x in voice_list if x.name == 'voice_a_1'][0]
    voice_selection = config_models.VoiceSelectionSingle()
    voice_selection.set_voice(config_models.VoiceWithOptions(voice_a_1, {}))

    batch_config = config_models.BatchConfig()
    source = config_models.BatchSourceSimple('Chinese')
    target = config_models.BatchTarget('Sound', False, True)

    batch_config.set_source(source)
    batch_config.set_target(target)
    batch_config.set_voice_selection(voice_selection)    

    batch_preview = component_batch_preview.BatchPreview(hypertts_instance, batch_config, note_id_list)
    batch_preview.draw(dialog.getLayout())

    # dialog.exec_()

    # play sound preview
    # ==================

    # select second row
    index_second_row = batch_preview.batch_preview_table_model.createIndex(1, 0)
    batch_preview.table_view.selectionModel().select(index_second_row, PyQt5.QtCore.QItemSelectionModel.Select)
    # press preview button
    qtbot.mouseClick(batch_preview.preview_audio_button, PyQt5.QtCore.Qt.LeftButton)

    assert hypertts_instance.anki_utils.played_sound == {
        'source_text': '你好',
        'voice': {
            'gender': 'Male', 
            'language': 'fr_FR', 
            'name': 'voice_a_1', 
            'service': 'ServiceA',
            'voice_key': {'name': 'voice_1'}
        },
        'options': {}
    }    

    # load audio
    # ==========

    qtbot.mouseClick(batch_preview.load_audio_button, PyQt5.QtCore.Qt.LeftButton)

    # make sure notes were updated
    note_1 = hypertts_instance.anki_utils.get_note_by_id(config_gen.note_id_1)
    assert 'Sound' in note_1.set_values 

    sound_tag = note_1.set_values['Sound']
    audio_full_path = hypertts_instance.anki_utils.extract_sound_tag_audio_full_path(sound_tag)
    audio_data = hypertts_instance.anki_utils.extract_mock_tts_audio(audio_full_path)

    assert audio_data['source_text'] == '老人家'

    note_2 = hypertts_instance.anki_utils.get_note_by_id(config_gen.note_id_2)
    assert 'Sound' in note_2.set_values 

    sound_tag = note_2.set_values['Sound']
    audio_full_path = hypertts_instance.anki_utils.extract_sound_tag_audio_full_path(sound_tag)
    audio_data = hypertts_instance.anki_utils.extract_mock_tts_audio(audio_full_path)

    assert audio_data['source_text'] == '你好'        


def test_batch_dialog(qtbot):
    config_gen = testing_utils.TestConfigGenerator()
    hypertts_instance = config_gen.build_hypertts_instance_test_servicemanager('default')

    dialog = EmptyDialog()
    dialog.setupUi()

    note_id_list = [config_gen.note_id_1, config_gen.note_id_2]    

    batch = component_batch.ComponentBatch(hypertts_instance, note_id_list)
    batch.draw(dialog.getLayout())
    # dialog.setLayout(batch.draw())
    # batch.draw(dialog.getLayout())

    dialog.exec_()