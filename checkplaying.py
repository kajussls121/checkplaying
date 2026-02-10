import time
import sys
import platform

SYSTEM = platform.system()

# ---------------- LINUX (MPRIS) ----------------
if SYSTEM == "Linux":
    try:
        import pydbus
    except ImportError:
        print("pydbus not found. Install with: pip install pydbus")
        sys.exit(1)

    bus = pydbus.SessionBus()
    dbus = bus.get("org.freedesktop.DBus", "/org/freedesktop/DBus")

    def is_media_playing():
        try:
            names = dbus.ListNames()
        except Exception as e:
            print(f"Error getting names: {e}")
            return False
        for name in names:
            if not name.startswith("org.mpris.MediaPlayer2."):
                continue
            try:
                player = bus.get(name, "/org/mpris/MediaPlayer2")
                if player.PlaybackStatus == "Playing":
                    return True
            except Exception:
                pass
    def get_media_info():
        try:
            names = dbus.ListNames()
        except Exception as e:
            print(f"Error getting names: {e}")
            return False
        for name in names:
            if not name.startswith("org.mpris.MediaPlayer2."):
                continue
            try:
                player = bus.get(name, "/org/mpris/MediaPlayer2")
            except Exception:
                pass
            #return player.Metadata
            #{'mpris:trackid': '/org/mpris/MediaPlayer2/firefox', 
            # 'xesam:title': 'Dancing With A Stranger (with Normani) • Sam Smith, Normani', 'xesam:album': '',
            #  'xesam:artist': [''],
            #  'xesam:url': 'https://open.spotify.com/playlist/5dqxr7GU7MEb6bTgYgbwbq',
            #  'mpris:length': 171000000}

            return {
                "title": player.Metadata['xesam:title'],
                "trackid": player.Metadata['mpris:trackid'],
                "artist": player.Metadata['xesam:artist'],
                "url": player.Metadata['xesam:url'],
                "status": player.PlaybackStatus,
                "duration": player.Metadata['mpris:length'] if 'mpris:length' in player.Metadata else None,
                "album": player.Metadata['xesam:album'] if 'xesam:album' in player.Metadata else None,
                "position": player.Metadata['mpris:position'] if 'mpris:position' in player.Metadata else None,
            }


# ---------------- WINDOWS (WinRT) ----------------
elif SYSTEM == "Windows":
    import asyncio
    try:
        from winrt.windows.media.control import (
            GlobalSystemMediaTransportControlsSessionManager
        )
    except ImportError:
        print("winrt not found. Install with: pip install winrt-runtime winrt-windows-media")
        sys.exit(1)

    async def _is_media_playing_async():
        manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        session = manager.get_current_session()
        if not session:
            return False

        info = session.get_playback_info()
        return info.playback_status.name == "PLAYING"

    def is_media_playing():
        return asyncio.run(_is_media_playing_async())

    def get_media_info():
        raise NotImplementedError("TODO: Windows get_media_info()")
        return {
            "title": info.metadata.title,
            "artist": info.metadata.artist,
            "album": info.metadata.album,
            "duration": info.metadata.duration,
            "position": info.metadata.position,
            "status": info.playback_status.name
        }


# ---------------- UNSUPPORTED ----------------
else:
    print(f"Unsupported OS: {SYSTEM}")
    sys.exit(1)


# ---------------- MAIN LOOP ----------------
def main():
    last_state = False

    while True:
        playing = is_media_playing()

        if playing and not last_state:
            # TODO: your code here
            print("Something started playing")
            try:
                minfo=get_media_info()#Temporary
            except Exception as e:
                print(f"Error getting media info: {e}")
                continue
            if minfo:
                #"title": player.Metadata['xesam:title'],
                #"trackid": player.Metadata['mpris:trackid'],
                #"artist": player.Metadata['xesam:artist'],
                #"url": player.Metadata['xesam:url'],
                #"status": player.PlaybackStatus,
                #"duration": player.Metadata['mpris:length'] if 'mpris:length' in player.Metadata else None,
                #"album": player.Metadata['xesam:album'] if 'xesam:album' in player.Metadata else None,
                #"position": player.Metadata['mpris:position'] if 'mpris:position' in player.Metadata else None,
                print("title: "+minfo["title"])
                print(f"trackid: {minfo["trackid"]}")
                print(f"artist: {minfo["artist"]}")
                print(f"url: {minfo["url"]}")
                print(f"status: {minfo["status"]}")
                print(f"duration: {minfo["duration"]}")
                print(f"album: {minfo["album"]}")
                print(f"position: {minfo["position"]}")
            else:
                print("minfo empty, restarting")
        elif not playing and last_state:
            print("Playback stopped")

        last_state = playing
        time.sleep(1)


if __name__ == "__main__":
    main()
