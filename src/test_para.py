import time
import multiprocessing


def x_square(x,send_end):
    time.sleep(1)
    result = x*x
    send_end.send(result)

def x_cube(x,send_end):
    time.sleep(2)
    result = x*x*x
    send_end.send(result)

if __name__ == '__main__':
    
    start = time.perf_counter()
    x = 7
    pipe_list = []
    
    [recv_end,send_end] = multiprocessing.Pipe(False)
    p1 = multiprocessing.Process(target=x_square, args=(x,send_end))
    pipe_list.append(recv_end)
    p1.start()

    [recv_end,send_end] = multiprocessing.Pipe(False)
    p2 = multiprocessing.Process(target=x_cube, args=(x,send_end))
    pipe_list.append(recv_end)
    p2.start()
    
    p1.join()
    p2.join()

    result_list = [x.recv() for x in pipe_list]
    
    finish = time.perf_counter()
    print(finish - start)
    print(result_list)
