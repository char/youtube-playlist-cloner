#!/usr/bin/env python3

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import json
import sys
import os


def get_youtube_service(settings):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "oauth.json", ["https://www.googleapis.com/auth/youtube"])

    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials, developerKey=settings["API_KEY"])

    return youtube


def get_playlist_title(youtube, playlist_id):
    playlists = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    ).execute()

    return playlists["items"][0]["snippet"]["title"]


def get_videos_in_playlist(youtube, playlist_id):
    # Since the API only gives us 5 playlist entries per call,
    # we have to navigate the pagination

    page_token = None
    while True:
        playlist_resource = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            pageToken=page_token
        ).execute()

        for item in playlist_resource["items"]:
            yield item["contentDetails"]["videoId"]
        
        if "nextPageToken" not in playlist_resource:
            break
        else:
            page_token = playlist_resource["nextPageToken"]


def create_playlist(youtube, playlist_title):
    created_playlist = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_title,
                "description": "Cloned playlist"
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        }
    ).execute()

    return created_playlist["id"]


def populate_playlist(youtube, playlist_id, videos):
    # Oof, we have to do this one-by-one.

    for video in videos:
        playlist_item = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video
                    }
                }
            }
        ).execute()

        yield playlist_item["snippet"]["title"]


def main(playlist_id):
    with open("settings.json") as f:
        settings = json.load(f)
        youtube = get_youtube_service(settings)

        playlist_title = get_playlist_title(youtube, playlist_id)
        print("Cloning playlist:", playlist_title)
        videos = list(get_videos_in_playlist(youtube, playlist_id))
        print("Found", len(videos), "videos")

        # TODO: For a next-day run (with a renewed quota),
        # we can set videos = videos[SOME_AMOUNT_ALREADY_WRITTEN:]

        new_playlist_id = create_playlist(youtube, "Copy of " + playlist_title)
        print("Created a new playlist:", new_playlist_id)

        print("\nAdding videos in sequence:")
        for added_title in populate_playlist(youtube, new_playlist_id, videos):
            print("+ " + added_title)


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]))
