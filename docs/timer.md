The Timer class is used to manage a queue of functions and execute them at regular intervals. It provides methods to add and remove functions from the queue, as well as starting and restarting the execution of the functions.

### Constructor

#### \_\_init__(self, gap:int=28800, queue:list[Callable]=[])

The constructor initializes a Timer object with the following parameters:

- `gap` (optional): The time gap in seconds between each execution of the functions in the queue. The default value is 28800 seconds (8 hours).
- `queue` (optional): A list of Callable objects representing the functions that will be executed at regular intervals. The default value is an empty list.

### Methods

#### add_to_queue(self, func:Callable=None) -> None

This method adds a Callable object to the queue. It takes the following parameter:

- `func`: The function to be added to the queue. It should be a Callable object.

If `func` is None, the method will raise an Exception with the message "Function is not callable".

#### remove_from_queue(self, index:int=None) -> None

This method removes a function from the queue based on its index. It takes the following parameter:

- `index` (optional): The index of the function to be removed from the queue. If not specified, it will raise a ValueError.

#### \_start(self) -> None

This method starts the execution of the functions in the queue. It is meant to be used internally and should not be called directly. It creates a separate process for each function in the queue and starts them.

#### \_restart(self) -> None

This method restarts the execution of the functions in the queue. It first stops the currently executing functions using the `_stop()` method and then starts them again using the `_start()` method.

#### start_job(self) -> bool

This method starts the execution of the functions in the queue. It returns a boolean value indicating whether the job was successfully started or not.

**Note:** The actual code implementation of the functions and the internals of the Timer class are not included in this documentation, as per the request to not touch the function code