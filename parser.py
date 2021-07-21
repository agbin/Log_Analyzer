import datetime
import sys

# a) Number of requests. Find if "request" is  in logline. If yes add 1 to num_req (number of requests)

def requests_in_loggs(logline, num_req):
    if "requests" in logline:
        num_req += 1
    return num_req

# c) Number of individual server response codes. Find status of 'response' in log, if response is already in d (dict)
# add 1 to it, if not add response to d dict, for example {200: 1}.

def responses_in_loggs(logline, d):
    response = logline.split()[13]
    if response in d:
        d[response] = d[response] + 1
    else:
        d[response] = 1
    return d

# d) Average size of the generated response. Read 'size of request' from logline. If status of 'response' of this log
# begin at 2::.Aadd size of it to 'sizes_of_2xx' and add 1 to num_of_sizes_of_2xx

def avgsize(logline, d, sizes_of_2xx, num_of_sizes_of_2xx):
    size = logline.split()[14]  # type str
    for key in d:
        if key[0] == '2':
            sizes_of_2xx += int(size)
            num_of_sizes_of_2xx += 1
    return sizes_of_2xx, num_of_sizes_of_2xx

# calculate how many seconds there are between the dates - the beginning and the end of the log range

def date_diff_in_Seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds

# b) count how many requests were send on 1 second (divide the number of requests by the time (in seconds))

def req_on_sec(start, end, requests):
    timedelta_in_sec = date_diff_in_Seconds(end, start)
    return ("%.4f" %(requests / timedelta_in_sec))

# default start date = first date from first line of logfile

def default_start(first_line):
    default_start = first_line.split()[5] + "_" + first_line.split()[6]
    default_start_dt = datetime.datetime.strptime(default_start, "%Y-%m-%d_%H:%M:%S")
    return default_start_dt

# default end date = last date from first line of logfile

def default_end(first_line):
    default_end = first_line.split()[11] + "_" + first_line.split()[12]
    default_end_dt = datetime.datetime.strptime(default_end, "%Y-%m-%d_%H:%M:%S")
    return default_end_dt

# considering sys.argv and default start and default end, specify start and end

def start_end(first_logline):
    start = 0
    end = 0
    # if dates are not given, default dates are start, end
    if len(sys.argv) > 1:
        if (sys.argv[1]) == "--from" and len(sys.argv) > 2:
            # if '--from', 'date' is given, set start
            if len(sys.argv[2]) == 19:
                start = datetime.datetime.strptime(sys.argv[2], "%d-%m-%Y_%H-%M-%S")
            elif len(sys.argv[2]) == 16:
                r = sys.argv[2] + "-00"
                start = datetime.datetime.strptime(r, "%d-%m-%Y_%H-%M-00")
            # if --from date is given and it has wrong format set default start
            elif len(sys.argv[2]) != 19 and len(sys.argv[2]) != 16:
                print("2. NIEPOPRAWNY FORMAT DATY '--FROM': ZOSTANIE UZYTA DOMYSLNA DATA POCZATKU:", default_start(first_logline))
        # if --to date is given and --from date is not given, set end
        if (sys.argv[1]) == "--to" and len(sys.argv) > 2:
            # print("3.. ok --to as first argv", sys.argv[2])
            # print(sys.argv[1])
            if len(sys.argv[2]) == 19:
                end = datetime.datetime.strptime(sys.argv[2], "%d-%m-%Y_%H-%M-%S")
            elif len(sys.argv[2]) == 16:
                r = sys.argv[2] + "-00"
                end = datetime.datetime.strptime(r, "%d-%m-%Y_%H-%M-00")
            # if --from date is given and it has wrong format, set default start
            elif len(sys.argv[2]) != 19 and len(sys.argv[2]) != 16:
                print("4. NIEPOPRAWNY FORMAT DATY '--FROM': ZOSTANIE UZYTA DOMYSLNA DATA POCZATKU:", default_start(first_logline))
        # if there are 1) --from date, 2) --to date, 3) logfile_name given
        if len(sys.argv) >= 4:
            if (sys.argv[3]) == "--to" and len(sys.argv) > 4:
                if len(sys.argv[4]) == 19:
                    # print("5. ok --to as 3. argv as end", sys.argv[4])
                    end = datetime.datetime.strptime(sys.argv[4], "%d-%m-%Y_%H-%M-%S")
                elif len(sys.argv[4]) == 16:
                    # print("6. ok --to as 3. argv")
                    r = sys.argv[4] + "-00"
                    end = datetime.datetime.strptime(r, "%d-%m-%Y_%H-%M-00")
        if start == 0:
            print("ZOSTANIE UZYTA DOMYSLNA DATA POCZATKOWA, --FROM:", default_start(first_logline), ", gdyż wystąpił jeden z przypadków: "
                  "1) NIEPOPRAWNY FORMAT SŁOWA '--from' "
                  "2) BRAK SŁOWA '--from' "
                  "3) NIEPOOPRAWNY FORMAT DATY POCZATKOWEJ"
                  "3) DATA POCZATKOWA NIE ZOSTALA PODANA ")
            start = default_start(first_logline)
        if end == 0:
            print("ZOSTANIE UZYTA DOMYSLNA DATA KONCOWA, --to:", default_end(first_logline), ", gdyż wystąpił jeden z przypadków: "
                  "1) NIEPOPRAWNY FORMAT SŁOWA '--to' "
                  "2) BRAK SŁOWA '--to' "
                  "3) NIEPOOPRAWNY FORMAT DATY KONCOWEJ "
                  "3) DATA KONCOWA NIE ZOSTALA PODANA ")
            end = default_end(first_logline)
    return start, end


# Main function is like the entry point of a program. It takes all given args and have global parameteters to conect
#with other functions.

def main(*args):
    global requests
    requests = 0
    global  requests_sec
    requests_sec = 0
    d = {}
    global sizes_of_2xx
    sizes_of_2xx = 0
    global num_of_sizes_of_2xx
    num_of_sizes_of_2xx = 0
    global avg_size_of_2xx_Mb
    avg_size_of_2xx_Mb = 0
    file = sys.argv[-1]
    if len(sys.argv) == 1:
        file = "blad"
    try:
        with open(file) as f:
            first_line = f.readline()
            start, end = start_end(first_line)
            # results can be shown if start date is smaller than end date
            if start < end:
                print("from:", start, "to:", end, '\n')
                for line in f:
                    # date of the individual log (changed on format: datetime)
                    data0 = line.split()[8]
                    data = data0[1:]
                    ts = datetime.datetime.strptime(data, '%d/%b/%Y:%H:%M:%S')
                    # count on these logfile which dates are between start date end end date
                    if ts > start and ts < end:
                        requests = requests_in_loggs(line, requests)
                        d = responses_in_loggs(line, d)
                        sizes_of_2xx, num_of_sizes_of_2xx = avgsize(line, d, sizes_of_2xx, num_of_sizes_of_2xx)
                requests_sec = req_on_sec(start, end, requests)
            else:
                print("DATA --FROM MUSI BYC DATA MNIEJSZA OD DATY --TO")
            # print requests, requests/sec, responses, avg size of 2xx responses (if start date were smaller than end date)
            if start < end:
                print("requests:", requests)
                print("requests/sec:", requests_sec)
                print("responses:", d)
                if num_of_sizes_of_2xx == 0:
                    avg_size_of_2xx = 0
                else:
                    avg_size_of_2xx = sizes_of_2xx / num_of_sizes_of_2xx  # in bytes
                avg_size_of_2xx_Mb = (avg_size_of_2xx * 8) / 1048576
                print("avg size of 2xx responses:", avg_size_of_2xx_Mb, "Mb")
    # if name of log does not exist:
    except IOError:
        print('''TAKI LOG FILE NIE ISTNIEJE, WPISZ np.: logfile.log  PRZYKLADOWE WYWOLANIE: 
              python3 parser.py --from 01-12-2019_11-23-11 --to 01-12-2019_00-33 logfile.log''')
    return requests, requests_sec, d, avg_size_of_2xx_Mb

main()

