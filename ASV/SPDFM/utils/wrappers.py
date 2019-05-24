import os 


def check_path_existence(func):
    """ Decorator for a function wich prototype is:
    
        func(features, outputFileName)
        
        This decorator gets the path included in 'outputFileName' if any 
        and check if this path exists; if not the path is created.
        :param func: function to decorate
    """
    def wrapper(*args, **kwargs):

        dir_name = os.path.dirname(args[1])  # get the path
        # Create the directory if it dosn't exist
        if not os.path.exists(dir_name) and (dir_name is not ''):
            os.makedirs(dir_name)            
        # Do the job
        func(*args, **kwargs)
    return wrapper