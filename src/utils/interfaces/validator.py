from abc import abstractmethod


class Validator:
    @abstractmethod
    def validate(self, value: any):
        pass
