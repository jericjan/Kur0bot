from typing import Any, Protocol
import inspect 
import functools

class UnboundedMsgHandlerType(Protocol):
    def __call__(_, self: Any, msg: str, *args: Any, **kwargs: Any) -> None:  # pyright: ignore[reportSelfClsParameterName]
        pass
    
class BoundedMsgHandlerType(Protocol):
    def __call__(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass

def msg_contains(keyword: str):
    def decorator(func: UnboundedMsgHandlerType):        
        @functools.wraps(func)      
        def wrapper(self: Any, msg: str, *args: Any, **kwargs: Any):
            if keyword in msg:
                func(self, msg, *args, **kwargs)
        setattr(wrapper, "_msg_handler", True)
        return wrapper    
    return decorator

class Test:
    def __init__(self):
        self.handlers: list[BoundedMsgHandlerType] = []
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
                    if hasattr(method, '_msg_handler'):
                         print(f"Appending function `{name}`")
                         self.handlers.append(method)

    def start(self, msg: str):
        for handler in self.handlers:
             handler(msg, 'a')

    @msg_contains("balls")
    def thing(self, msg: str, more: str):
        print(f"BALLS???")        

a = Test()
a.start("i like balls")
