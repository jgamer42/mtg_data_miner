import datetime


def check_execution_time(method):
    """
    Decorator used to check how much time tooks the execution from a function
    """
    def decorator(*args,**kwargs):
        start:datetime.datetime = datetime.datetime.now()
        method_name:str = str(method).split(" ")[1]
        output =  method(*args,**kwargs)
        end:str = str(datetime.datetime.now() - start)
        return output
    return decorator