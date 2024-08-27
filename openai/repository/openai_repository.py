from abc import abstractmethod, ABC


class OpenAIRepository(ABC):
    @abstractmethod
    def generateText(self, userSendMessage):
        pass