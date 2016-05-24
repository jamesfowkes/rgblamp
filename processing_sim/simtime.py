import datetime

sim_time = datetime.datetime.now()

old_millis = 0
    
def set(new_time):
    global sim_time
    sim_time = datetime.datetime.combine(sim_time.date(), new_time)
 
def tick():
    global old_millis
    global sim_time
    if millis() - old_millis >= 500:
        old_millis = millis()
        sim_time += datetime.timedelta(minutes=1)
        
    return sim_time