import utils
import globalVars


def checkAndHandleIgnores():
    ''' Removes the values for each file and mode in the ignore files.
        Also sets the ignored values in those files to true in the DB.
    '''

    with open('ignoreReps.txt') as ignoreReps:
        IGNORE_REPS = ignoreReps.readlines()
    with open('ignoreModes.txt') as ignoreModes:
        IGNORE_MODES = ignoreModes.readlines()

    LAST_TIME_OPENED = globalVars.LAST_TIME_OPENED
    # modIgnoreReps is True if ignoreReps was changes
    # since the last time NullpoTracker was run, to know
    # if it has to update the db for new reps to ignore
    modIgnoreReps = utils.modTime('ignoreReps.txt') > LAST_TIME_OPENED
    pass