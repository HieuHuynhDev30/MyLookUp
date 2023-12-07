import requests
from django import forms


class WordForm(forms.Form):
    word = forms.CharField(label='Your word', max_length=50)

    def search(self):
        result = {}
        searched_word = self.cleaned_data['word']
        if searched_word.isalpha():
            api_key = '57f42480-9178-4af8-9398-2f75f536fc08'
            api_url = f'''https://www.dictionaryapi.com/api/v3/references/learners/json/{searched_word}?key={api_key}'''
            response = requests.get(api_url)
            if response.status_code == 200:
                response = response.json()
                if response:
                    response_str = str(response)
                    if 'meta' in response_str:
                        response_object = response[0]
                        meta = response_object['meta']
                        stems = meta['stems']
                        exact_word = stems[0]
                        result['exact_word'] = exact_word.capitalize()
                        result['type'] = meta['app-shortdef']['fl'].casefold()
                        ipa = response_object['hwi']['prs'][0]['ipa']
                        result['ipa'] = f'/{ipa}/'
                        audio = response_object['hwi']['prs'][0]['sound']['audio']
                        subdirectory = audio[0]
                        prefixes = ['bix', 'gg', *tuple(list('0123456789'))]
                        for prefix in prefixes:
                            if audio.startswith(prefix, 0):
                                subdirectory = prefix
                        formats = ['mp3', 'wav', 'ogg']
                        audio_srcs = []
                        for ext in formats:
                            audio_srcs.append({'src': f'''https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdirectory}/{audio}.{ext}''', 'type': ext})
                        result['audio_srcs'] = audio_srcs
                        result['phrases'] = []
                        for phrase in stems[1:]:
                            result['phrases'].append(phrase.capitalize())
                        result['meanings'] = []
                        for meaning in response_object['shortdef']:
                            if not meaning[0].isalpha():
                                meaning = meaning[1:]
                            result['meanings'].append(meaning.capitalize())
                    else:
                        result['phrases'] = response
                else:
                    result['message'] = f'No results for "{searched_word}"'
            elif response.status_code == 500:
                result['message'] = 'Word not found'
            else:
                result['message'] = 'API not working'
        else:
            result['message'] = 'Invalid typing'
        return result
