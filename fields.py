import typing


class AnswerTypesField:
    """
    Answer types
    """
    BASE_FIELD = 'base_field'
    CHOICE_FIELD = 'choice_field'
    CUSTOM_TEXT_FIELD = 'custom_text_field'
    DATE_FIELD = 'date_field'


class AnswerBaseField:
    """
    Base answer model
    """
    def __init__(self, label: str, value: typing.Any = None):
        self.type = AnswerTypesField.BASE_FIELD
        self.label = label  # Answer label
        self.value = value  # Answer value

    def get_question(self) -> dict:
        """
        Function to get a dictionary of answer data
        :return: Dictionary containing answer data
        """
        return self.__dict__


class AnswerChoiceField(AnswerBaseField):
    """
    Choice answer field
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = AnswerTypesField.CHOICE_FIELD


class AnswerCustomTextField(AnswerBaseField):
    """
    Custom text input field
    """
    def __init__(self, max_length: int = 255, **kwargs):
        super().__init__(**kwargs)
        self.type = AnswerTypesField.CUSTOM_TEXT_FIELD
        self.max_length = max_length


class AnswerDateField(AnswerBaseField):
    """
    Date selection field for a question
    """
    def __init__(self, date: bool = True, time: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.type = AnswerTypesField.DATE_FIELD
        self.date = date  # Does the answer require a date
        self.time = time  # Does the answer require a time
