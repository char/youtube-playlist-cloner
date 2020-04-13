# youtube-playlist-cloner

A simple script to copy the contents of a YouTube playlist to another.

## Motivation

On YouTube, you cannot set your 'Liked videos' playlist to 'Unlisted', only 'Public' or 'Private'.

We can work around this by cloning the Liked videos playlist to another playlist, and setting *that* one to 'Unlisted'.

## Requirements

- [Pipenv](https://pipenv.pypa.io/)
- If not Pipenv, then install the dependencies listed in the Pipfile manually.

## Usage

1. Create an [API key for the YouTube Data API](https://developers.google.com/youtube/v3/quickstart/python#step_1_set_up_your_project_and_credentials)
2. Create a [Google OAuth keypair](https://console.developers.google.com/apis/credentials) through the Google API console.
3. Download the OAuth client JSON from the Google panel and save it as `./oauth.json`

```
$ git clone $THIS_REPO
$ cd youtube-playlist-cloner/
$ cp settings.example.json settings.json
$ $EDITOR settings.json
[set up the API key]
$ # download the OAuth client JSON
$ mv ~/Downloads/[the OAuth JSON] ./oauth.json
$ pipenv --three shell
[pipenv] $ pipenv install # Install the dependencies from the Pipfile
[pipenv] $ python3 youtube_playlist_cloner.py [playlist ID]
```
