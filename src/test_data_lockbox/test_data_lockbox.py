TEST_DATA_LOCKBOX_HAS_DISPLAYED_HELP_MESSAGE = False


class LockboxAccessViolation(Exception):
    """An error raised when the user attempts to access their training data without unlocking the lockbox first."""
    pass


class TestDataLockbox(object):
    _has_been_unlocked = False
    _stored_vars = []

    def __init__(self, suppress_help_message=True):
        global TEST_DATA_LOCKBOX_HAS_DISPLAYED_HELP_MESSAGE
        # only show the help message one time, and only if the user wants us to.
        if suppress_help_message and not TEST_DATA_LOCKBOX_HAS_DISPLAYED_HELP_MESSAGE:
            self.help()
            TEST_DATA_LOCKBOX_HAS_DISPLAYED_HELP_MESSAGE = True

    def __setattr__(self, item, value):
        if not self._has_been_unlocked:
            self._stored_vars.append(item)
        object.__setattr__(self, item, value)
        #self.__dict__[item] = value

    def __getattribute__(self, item):
        if item not in ['_has_been_unlocked', '_stored_vars'] and item in self._stored_vars and not self._has_been_unlocked:
            raise LockboxAccessViolation('Lockbox is locked to prevent evaluation bias. If you are completely done developing your model, call .unlock() to gain access to this variable.')
        else:
            return object.__getattribute__(self, item)

    def unlock(self):
        self._has_been_unlocked = True

    def help(self):
        """
        Display a message introducing the user to the library.
        """
        print('Thanks for using TestDataLockbox!')
        print('Evaluation bias is a huge problem because it can cause you to underestimate your model\'s true test error.')
        print('TestDataLockbox is an educational library that will help you avoid this issue by preventing data access until you are done building your model.')
        print('When you create a TestDataLockbox, it is write-only until you call .unlock(), meaning any attributes you add to it will be protected from access until you are ready for them.')
        print()
        print('Tips for avoiding evaluation bias using this library:')
        print(' - Always pull test data directly from the source into your TestDataLockbox without performing any encoding or analysis.')
        print(' - Once you have unlocked your TestDataLockbox, avoid altering your model in any way.')
        print(' - If you want to tune hyper-parameters, use a separate validation set to estimate model accuracy.')
        print('   For more information about validation sets, check out this website: https://machinelearningmastery.com/difference-test-validation-datasets/')
        print()