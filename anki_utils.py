import sys
import os
import aqt
import anki.template
import anki.sound
import anki.collection
import logging
import aqt.qt
from . import constants    

if hasattr(sys, '_sentry_crash_reporting'):
    import sentry_sdk

class AnkiUtils():
    def __init__(self):
        pass

    def get_config(self):
        return aqt.mw.addonManager.getConfig(__name__)

    def write_config(self, config):
        aqt.mw.addonManager.writeConfig(__name__, config)

    def night_mode_enabled(self):
        night_mode = aqt.mw.pm.night_mode()
        return night_mode

    def get_green_stylesheet(self):
        night_mode = self.night_mode_enabled()
        if night_mode:
            return constants.GREEN_STYLESHEET_NIGHTMODE
        return constants.GREEN_STYLESHEET

    def get_red_stylesheet(self):
        night_mode = self.night_mode_enabled()
        if night_mode:
            return constants.RED_STYLESHEET_NIGHTMODE
        return constants.RED_STYLESHEET

    def get_user_files_dir(self):
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        user_files_dir = os.path.join(addon_dir, 'user_files')
        return user_files_dir        

    def play_anki_sound_tag(self, text):
        out = aqt.mw.col.backend.extract_av_tags(text=text, question_side=True)
        file_list = [
            x.filename
            for x in anki.template.av_tags_to_native(out.av_tags)
            if isinstance(x, anki.sound.SoundOrVideoTag)
        ]   
        if len(file_list) >= 1:
            filename = file_list[0]
            aqt.sound.av_player.play_file(filename)

    def get_note_by_id(self, note_id):
        note = aqt.mw.col.getNote(note_id)
        return note

    def get_model(self, model_id):
        return aqt.mw.col.models.get(model_id)

    def get_deck(self, deck_id):
        return aqt.mw.col.decks.get(deck_id)

    def get_model_id(self, model_name):
        return aqt.mw.col.models.id_for_name(model_name)

    def get_deck_id(self, deck_name):
        return aqt.mw.col.decks.id_for_name(deck_name)

    def media_add_file(self, filename):
        full_filename = aqt.mw.col.media.addFile(filename)
        return full_filename

    def undo_start(self):
        return aqt.mw.col.add_custom_undo_entry(constants.UNDO_ENTRY_NAME)

    def undo_end(self, undo_id):
        aqt.mw.col.merge_undo_entries(undo_id)
        aqt.mw.update_undo_actions()
        aqt.mw.autosave()

    def update_note(self, note):
        aqt.mw.col.update_note(note)

    def create_card_from_note(self, note, card_ord, model, template):
        return note.ephemeral_card(
            card_ord,
            custom_note_type=model,
            custom_template=template
        )

    def extract_tts_tags(self, av_tags):
        tts_tags = [x for x in av_tags if isinstance(x, anki.sound.TTSTag)]
        return tts_tags

    def save_note_type_update(self, note_model):
        logging.info(f"""updating note type: {note_model['name']}""")
        aqt.mw.col.models.update_dict(note_model)

    def run_in_background(self, task_fn, task_done_fn):
        aqt.mw.taskman.run_in_background(task_fn, task_done_fn)

    def run_on_main(self, task_fn):
        aqt.mw.taskman.run_on_main(task_fn)

    def wire_typing_timer(self, text_input, text_input_changed):
        typing_timer = aqt.qt.QTimer()
        typing_timer.setSingleShot(True)
        typing_timer.timeout.connect(text_input_changed)
        text_input.textChanged.connect(lambda: typing_timer.start(1000))
        return typing_timer


    def call_on_timer_expire(self, timer, task):
        if timer.timer_obj != None:
            # stop it first
            timer.timer_obj.stop()
        timer.timer_obj = aqt.qt.QTimer()
        timer.timer_obj.setSingleShot(True)
        timer.timer_obj.timeout.connect(task)
        timer.timer_obj.start(timer.delay_ms)

    def info_message(self, message, parent):
        aqt.utils.showInfo(message, title=constants.ADDON_NAME, textFormat='rich', parent=parent)

    def critical_message(self, message, parent):
        aqt.utils.showCritical(message, title=constants.ADDON_NAME, parent=parent)

    def ask_user(self, message, parent):
        result = aqt.utils.askUser(message, parent=parent)
        return result

    def play_sound(self, filename):
        aqt.sound.av_player.play_file(filename)

    def show_progress_bar(self, message):
        aqt.mw.progress.start(immediate=True, label=f'{constants.MENU_PREFIX} {message}')

    def stop_progress_bar(self):
        aqt.mw.progress.finish()

    def editor_set_field_value(self, editor, field_index, text):
        if field_index >= len(editor.note.fields):
            raise Exception(f'there are {len(editor.note.fields)} fields in this note, field index {field_index} not found')
        # set the field value on the note
        editor.note.fields[field_index] = text
        # update the webview
        js_command = f"""set_field_value({field_index}, "{text}")"""
        editor.web.eval(js_command)

    def show_loading_indicator(self, editor: aqt.editor.Editor, field_index):
        js_command = f"show_loading_indicator({field_index})"
        if editor != None and editor.web != None:
            editor.web.eval(js_command)

    def hide_loading_indicator(self, editor: aqt.editor.Editor, field_index, original_field_value):
        js_command = f"""hide_loading_indicator({field_index}, "{original_field_value}")"""
        if editor != None and editor.web != None:
            editor.web.eval(js_command)

    def checkpoint(self, action_str):
        aqt.mw.checkpoint(action_str)

    def display_dialog(self, dialog):
        return dialog.exec_()

    def report_known_exception_interactive(self, exception, action):
        error_message = f'Encountered an error while {action}: {str(exception)}'
        self.critical_message(error_message, None)

    def report_unknown_exception_interactive(self, exception, action):
        error_message = f'Encountered an unknown error while {action}: {str(exception)}'
        if hasattr(sys, '_sentry_crash_reporting'):
            sentry_sdk.capture_exception(exception)
        else:
            logging.critical(exception, exc_info=True)
        self.critical_message(error_message, None)

    def report_unknown_exception_background(self, exception):
        if hasattr(sys, '_sentry_crash_reporting'):
            sentry_sdk.capture_exception(exception)
        else:
            logging.critical(exception, exc_info=True)
