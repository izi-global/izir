"""This is an example of a izi "sink", these enable all request URLs that start with the one defined to be captured

To try this out, run this api with izi -f sink_example.py and hit any URL after localhost:8000/all/
(for example: localhost:8000/all/the/things/) and it will return the path sans the base URL. 
"""
import izi


@izi.sink('/all')
def my_sink(request):
    return request.path.replace('/all', '')
