from typing import Optional
import traceback


# #
# Base

class DomainError(Exception):
    def __init__(self, msg: str, code: int) -> None:
        self.msg = msg
        self.code = code

    def __str__(self) -> str:
        return self.msg
    
    def __trace_back__(self) -> str:
        return ''.join(traceback.format_exception(type(self), self, self.__traceback__))


# #
# DomainError

class InvalidTypeError(DomainError):
    def __init__(self, target, valid_type: type):
        super().__init__(msg=f"\n\t{target}, 유효하지 않은 자료형입니다. 유효한 자료형({valid_type})", code=400)
    
    @classmethod
    def from_pydantic(cls, e):
        error = next((err for err in e.errors() if err['type'] == 'dataclass_type'), None)
        if not error:
            raise ValueError("is not 'dataclass_type'.")

        target = " > ".join(map(str, error.get('loc', [])))
        valid_type = error.get('ctx', {}).get('class_name', 'Unknown')

        return cls(target=target, valid_type=valid_type)
    
class InvalidFormatError(DomainError):
    def __init__(self, target: str, valid_example: str):
        super().__init__(msg=f"\n\t {target}, 유효하지 않은 형식입니다. 유효한 형식의 예({valid_example})", code=400)

class InvalidLengthError(DomainError):
    def __init__(self, target: str, min_len: Optional[int] = 0, max_len: Optional[int] = None):
        if max_len is None:
            super().__init__(msg=f"\n\t {target}, 유효하지 않은 길이입니다. 유효한 길이({min_len}~)", code=400)

        elif min_len == max_len:
            super().__init__(msg=f"\n\t {target}, 유효하지 않은 길이입니다. 유효한 길이({min_len})", code=400)

        else:
            super().__init__(msg=f"\n\t {target}, 유효하지 않은 길이입니다. 유효한 길이({min_len}~{max_len})", code=400)

class DisallowedValueError(DomainError):
    def __init__(self, target: str, allowed_list: list):
        super().__init__(msg=f"\n\t {target}, 허용되지 않은 값입니다. 허용된 값({allowed_list})", code=400)

class EmptyValueError(DomainError):
    def __init__(self, target: str):
        super().__init__(msg=f"\n\t {target}, 비어있을 수 없는 값입니다.", code=400)

class FrozenAttributeError(DomainError):
    def __init__(self, target: str):
        super().__init__(msg=f"\n\t{target}, 유효하지 않은 동작입니다. frozen 상태의 속성은 수정할 수 없습니다.", code=403)


# #
# DatabaseError

class DatabaseError(DomainError):
    pass


class NotInsertedError(DatabaseError):
    def __init__(self, target: str, exception: Optional[Exception]) -> None:
        super().__init__(f"{target} 생성에 실패했습니다. Details: {exception}", code=400)

class NotEditedError(DatabaseError):
    def __init__(self, target: str, exception: Optional[Exception]) -> None:
        super().__init__(f"{target} 수정에 실패했습니다. Details: {exception}", code=400)

class NotFoundError(DatabaseError):
    def __init__(self, target: str, exception: Optional[Exception]) -> None:
        super().__init__(f"{target} 조회에 실패했습니다. Details: {exception}", code=404)
