class TestModule(object):

    def tests(self):
        return {
            'boolean': self.is_boolean,
        }

    def is_boolean(self, value):
        """Test if a value is of type boolean.

        Jinja2 >= 2.11 comes a built-in boolean test, but most systems will ship
        an older version. Until Ansible adopts the new Jinja2 version, this test
        can be used as an alternative.

        Args:
            value: A value, that shall be type tested

        Returns:
            bool: True, if value is of type boolean, False otherwise.
        """
        return isinstance(value, bool)
