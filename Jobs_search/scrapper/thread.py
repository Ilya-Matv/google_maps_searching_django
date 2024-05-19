import multiprocessing
from pickle import FALSE
import threading
from .models import BusinessList, Business
from .scrap_function import start_scrap
from django.utils import timezone
import time
from .Global_Variable_Manager import GlobalVariable


prog = GlobalVariable()

class CreateBusinessesThread(threading.Thread):
    def __init__(self, request, city, profession, number, name="scrap_and_ProgressVariable"):
        self.request = request
        self.city = city
        self.profession = profession
        self.number = number
        global prog
        threading.Thread.__init__(self)


    def run(self):
        try:
            print('Thread execution started')
            queue = multiprocessing.Queue()
            global prog
            
            process = multiprocessing.Process(target=start_scrap, args=(queue,[f"{self.city} {self.profession}"], self.number))
            process.start()
            condition = self.number
            if condition == 'all':
                while process.is_alive():
                    data = queue.get()  # Get data from the queue
                    prog.set_value(value = data)
                prog.set_value(value = -1) 
            else:
                while process.is_alive():
                    data = queue.get()  # Get data from the queue
                    prog.set_value(value = (round(data/self.number, 1)*100))
                    if prog.get_value() == 100:
                        break    
            
            list = queue.get()
            business_list = BusinessList.objects.create(user = self.request.user, name = f'{self.city} {self.profession}', count_num = len(list),date = timezone.now())
            for i in list:
                bus = Business.objects.create(name=i['name'], address=i['address'], website=i['website'], phone_number=i['phone_number'])
                business_list.businesses.add(bus)
                business_list.save()
        except Exception as e:
            print(e)

    

