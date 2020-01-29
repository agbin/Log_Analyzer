import datetime
import sys


requests = 0
d = {}
sizes_of_2xx = 0
num_of_sizes_of_2xx = 0


if len(sys.argv) == 6:
    file = sys.argv[5]
if len(sys.argv) == 4:
    file = sys.argv[3]
if len(sys.argv) == 2:
    file = sys.argv[1]



try:
    with open(file) as f:

        first_line = f.readline()                                           # to ignore first line

# default start_date from first line
        default_start = first_line.split()[5] + "_" + first_line.split()[6]
        default_start_dt = datetime.datetime.strptime(default_start, "%Y-%m-%d_%H:%M:%S")
# default end_date from first line
        default_end = first_line.split()[11] + "_" + first_line.split()[12]
        default_end_dt = datetime.datetime.strptime(default_end, "%Y-%m-%d_%H:%M:%S")



 # --from, date, --to, date, logfile.log (all argvs are given)


        start = default_start_dt
        end = default_end_dt

        # print("ok start as default_start_dt:", start)
        # print("ok end as default_end_dt", end)
        if (sys.argv[1]) == "--from":
            print("1. ok --from as first argv", sys.argv[2])
            if len(sys.argv[2]) == 19:
                start = datetime.datetime.strptime(sys.argv[2], "%d-%m-%Y_%H-%M-%S")
            elif len(sys.argv[2]) == 16:
                r = sys.argv[2] +"-00"
                start = datetime.datetime.strptime(r, "%d-%m-%Y_%H-%M-00")
            elif len(sys.argv[2]) != 19 and len(sys.argv[2]) != 16:
                print("2. WPISZ POPRAWNY FORMAT DATY: --from %d-%m-%Y_%H-%M-%S, np. --from 01-12-2019_11-33-00")
        if (sys.argv[1]) == "--to":
            print("3.. ok --to as first argv", sys.argv[2])
            # print(sys.argv[1])
            if len(sys.argv[2]) == 19:
                end = datetime.datetime.strptime(sys.argv[2], "%d-%m-%Y_%H-%M-%S")
            elif len(sys.argv[2]) == 16:
                r = sys.argv[2] + "-00"
                end = datetime.datetime.strptime(r, "%d-%m-%Y_%H-%M-00")
            elif len(sys.argv[2]) != 19 and len(sys.argv[2]) != 16:
                print("4. WPISZ POPRAWNY FORMAT DATY: --from %d-%m-%Y_%H-%M-%S, np. --from 01-12-2019_11-33-00")

        if len(sys.argv) >= 3:
            if (sys.argv[3]) == "--to":

                if len(sys.argv[4]) == 19:
                    print("5. ok --to as 3. argv as end", sys.argv[4])
                    end = datetime.datetime.strptime(sys.argv[4], "%d-%m-%Y_%H-%M-%S")
                elif len(sys.argv[4]) == 16:
                    print("6. ok --to as 3. argv")
                    r = sys.argv[4] +"-00"
                    end = datetime.datetime.strptime(r, "%d-%m-%Y_%H-%M-00")
                else:
                # elif len(sys.argv[4]) != 19 and len(sys.argv[4]) != 16:
                #     sys.exit("WPISZ POPRAWNY FORMAT DATY '--TO': --to %d-%m-%Y_%H-%M-%S, np. --to 01-12-2019_11-33-00")
                    print("7. NIEPOPRAWNY FORMAT DATY '--TO': ZOSTANĄ UŻYTA DOMYŚLNA DATA KOŃCOWA")


        print("")
        print("start:", start)
        print("end:", end)
        print("")

        for line in f:
            data0 = line.split()[8]
            data = data0[1:]
            # print(data)

            ts = datetime.datetime.strptime(data, '%d/%b/%Y:%H:%M:%S')
            if ts > start and ts < end:

#requests:
                if "requests" in line:
                    requests += 1

#responses:

                response = line.split()[13]
                if response in d:
                    d[response] = d[response] + 1
                else:
                    d[response] = 1

#avg size of 2xx responses:
                size = line.split()[14]  # type str
                for i in response:
                    # print(response[0])
                    if response[0] == "2":
                        # print("yeah")
                        # print(size)
                        sizes_of_2xx += int(size)
                        num_of_sizes_of_2xx += 1

# requests/sec
        def date_diff_in_Seconds(dt2, dt1):
            timedelta = dt2 - dt1
            return timedelta.days * 24 * 3600 + timedelta.seconds



        timedelta_in_sec = date_diff_in_Seconds(end, start)
        requests_sec = requests / timedelta_in_sec



except IOError:
    print('''TAKI LOG FILE NIE ISTNIEJE, WPISZ np.: logfile.log /n
          PRZYKŁADOWE WYWOŁANIA:
          python3 parser.py --from 01-12-2019_11-23-11 --to 01-12-2019_00-33 logfile.log''')



print("requests:", requests)
print("requests/sec:", requests_sec)

# for key in list(d.keys()):
#     print("responses:", key, ":", d[key])
#
# print("responses:", tuple(d.items()))


print("responses:", d)




avg_size_of_2xx = sizes_of_2xx / num_of_sizes_of_2xx        # in bytes
avg_size_of_2xx_Mb = (avg_size_of_2xx * 8) / 1048576
print("avg size of 2xx responses:", avg_size_of_2xx, "bytes")
print("avg size of 2xx responses:", avg_size_of_2xx_Mb, "Mb")




