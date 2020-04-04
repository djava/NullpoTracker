import os
import datetime
import timezones
import globalVars


def modTime(path: str, *includeReplayPath: bool) -> datetime.datetime:
    ''' Returns the last modified time of a file

        Path is the path of the file to modTime

        Set includeReplayPath to True to just add the replay
        path to the arg to shorten function calls
    '''

    if includeReplayPath:
        return datetime.datetime.fromtimestamp(
            os.path.getmtime(globalVars.REPLAY_PATH + path), tz=timezones.UTC)
    else:
        return datetime.datetime.fromtimestamp(
            os.path.getmtime(path), tz=timezones.UTC)