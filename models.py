import typing
from fields import AnswerBaseField


class QuestionProcess:
    """
    Processor for QuestionBaseModel
    """
    def __init__(self, _class):
        self._class = _class
        self.question = self.question(_class)

    @staticmethod
    def find_question(question_id: typing.Any):
        """
        Function to find a specific question by question_id

        ex: QuestionBaseModel.process.find_question(question_id='example_id')
        """
        question = None
        for subclass in QuestionBaseModel.__subclasses__():
            if subclass.question_id == question_id:
                question = subclass
                break
        return question

    class question:
        def __init__(self, _class):
            self._class = _class

        def get(self, label: typing.Any):
            """
            Function to retrieve a specific answer in a question

            :param label: Answer label
            :return: Subclass of QuestionBaseModel
            """
            question = None
            if label:
                for attr in dir(self._class):
                    attr = getattr(self._class, attr)
                    if issubclass(type(attr), AnswerBaseField) and attr.label == label:
                        question = attr
                        break
            return question


class QuestionConstants:
    """
    Class for defining survey constants
    """
    # General answers
    YES = 'Yes'
    NOT_YET = 'Not yet'
    NOT_WILLING_TO_ANSWER = "I don't want to answer"

    # Plot lines
    SPECIAL_CASE_1 = 'Special Case 1'  # Special case that will consider previous answers
    ANY_ANSWER = 'Any answer'  # Any answer will lead to a specific plot
    THE_END = 'End of survey'


class QuestionBaseModel:
    """
    Base question class
    question_id - String with any content for question identification
    title - String with any content for defining question title
    many - Boolean value to determine choosing one or multiple answers
    choices - List of strings with answer choices
    plot - Dictionary for defining question plots. Format:
           {
                tuple('Answer_1'): Question class(QuestionBaseModel) referenced by 'Answer_1',
                tuple('Answer_2'): Question class(QuestionBaseModel) referenced by 'Answer_2',
           }
    """

    def __init_subclass__(cls, **kwargs):
        # Assign answer choices to the question
        answers = []
        for _attr in dir(cls):
            attr = getattr(cls, _attr)
            if issubclass(type(attr), AnswerBaseField):
                answers.append(attr.get_question())
        cls.answers = answers
        cls.process = QuestionProcess(cls)  # Processor for the inherited class

    question_id = ""  # Question identifier
    title = ""  # Question title
    many = False  # Choose one or multiple questions
    answers = []  # Answer choices
    plot = {}  # Question plots
    process = QuestionProcess  # Processor for the base class

    @classmethod
    def question_data(cls):
        """
        Returns complete question data defined in the subclass
        """
        data = {
            'question_id': cls.question_id,
            'title': cls.title,
            'many': cls.many,
            'answers': cls.answers,
        }
        return data


class QuestionPlotBaseModel:
    """
    Base plot model
    """
    question = QuestionBaseModel
    plot = {}

    @classmethod
    def activate(cls, _class):
        """
        Assigns the plot defined in the subclass to the parent class QuestionBaseModel
        """
        if _class.question is not cls.question:
            _class.question.plot = _class.plot
        return
