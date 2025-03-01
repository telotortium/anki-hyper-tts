import sys
import requests
import base64
import logging
import time

voice = __import__('voice', globals(), locals(), [], sys._addon_import_level_services)
service = __import__('service', globals(), locals(), [], sys._addon_import_level_services)
errors = __import__('errors', globals(), locals(), [], sys._addon_import_level_services)
constants = __import__('constants', globals(), locals(), [], sys._addon_import_level_services)

class Google(service.ServiceBase):
    CONFIG_API_KEY = 'api_key'
    CONFIG_EXPLORER_API_KEY = 'explorer_api_key'
    CONFIG_THROTTLE_SECONDS = 'throttle_seconds'

    def __init__(self):
        service.ServiceBase.__init__(self)

    def cloudlanguagetools_enabled(self):
        return True

    @property
    def service_type(self) -> constants.ServiceType:
        return constants.ServiceType.tts

    @property
    def service_fee(self) -> constants.ServiceFee:
        return constants.ServiceFee.Premium

    def configuration_options(self):
        return {
            self.CONFIG_API_KEY: str,
            self.CONFIG_EXPLORER_API_KEY: bool,
            self.CONFIG_THROTTLE_SECONDS: float
        }

    def voice_list(self):
        return self.basic_voice_list()

    def get_tts_audio(self, source_text, voice: voice.VoiceBase, options):
        # configuration options
        api_key = self.get_configuration_value_mandatory(self.CONFIG_API_KEY)
        is_explorer_api_key = self.get_configuration_value_optional(self.CONFIG_EXPLORER_API_KEY, False)
        throttle_seconds = self.get_configuration_value_optional(self.CONFIG_THROTTLE_SECONDS, 0)

        if throttle_seconds > 0:
            time.sleep(throttle_seconds)

        payload = {
            "audioConfig": {
                "audioEncoding": "MP3",
                "pitch": options.get('pitch', voice.options['pitch']['default']),
                "speakingRate": options.get('speaking_rate', voice.options['speaking_rate']['default']),
            },
            "input": {
                "ssml": f"<speak>{source_text}</speak>"
            },
            "voice": {
                "languageCode": voice.voice_key['language_code'],
                "name": voice.voice_key['name'],
            }
        }

        logging.debug(f'requesting audio with payload {payload}')

        headers = {}
        if is_explorer_api_key:
            headers['x-origin'] = 'https://explorer.apis.google.com'
        response = requests.post(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}", json=payload, headers=headers,
            timeout=constants.RequestTimeout)
        
        if response.status_code != 200:
            data = response.json()
            error_message = data.get('error', {}).get('message', str(data))
            logging.error(error_message)
            raise errors.RequestError(source_text, voice, error_message)

        data = response.json()
        encoded = data['audioContent']
        audio_content = base64.b64decode(encoded)

        return audio_content