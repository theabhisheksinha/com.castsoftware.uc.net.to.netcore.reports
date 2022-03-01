class NetCoreProperty:

    def __init__(self, aip_property: str, title: str, description: str):
        """
        Initialize the property
        :param aip_property: Property to retrieve in CAST AIP
        :param title: Name of the property
        :param description: Description of it to be formatted
        """
        self._property = aip_property
        self._title = title
        self._description = description
        self._value = None

    def copy(self):
        """
        Get a copy of the object
        :return:
        """
        return NetCoreProperty(self._property,
                               self._title,
                               self._description)

    def set_value(self, value) -> None:
        """
        Set a value to the property
        :param value: Value to set
        :return:  None
        """
        self._value = value

    def get_value(self):
        """
        Get the value of the property
        This field needs to be populated first
        :return:
        """
        return self._value

    def format_description(self, **values) -> str:
        """
        Format the description of the property
        :param values: Values to apply
        :return: The new description
        """
        self._description = self._description.format(values)
        return self._description

    def format_title(self, **values) -> str:
        """
        Format the title of the property
        :param values: Values to apply
        :return: The new title
        """
        self._title = self._title.format(values)
        return self._title

    def get_title(self) -> str:
        """
        Getter on the title
        :return: Title
        """
        return self._title

    def get_description(self) -> str:
        """
        Getter on the description
        :return: Description
        """
        return self._description

    def get_property(self) -> str:
        """
        Getter on the property
        :return: AIP Property
        """
        return self._property
