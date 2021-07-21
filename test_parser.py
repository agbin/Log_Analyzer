import pytest
import parser
import sys
import datetime

@pytest.mark.parametrize('logline, number, result',
                         [
                             ('Dec 01 11:06:07 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:07 +0100] "GET /internal/user/5fe5aeac-261d-4e2f-9811-c054edda14fa/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 92048', 0, 1),
                             ('Dec 01 11:05:45 app3-test-vm1 gunicorn[53253]: 172.16.3.5 - - [01/Dec/2019:11:05:45 +0100] "GET /.well-known/assetlinks.json HTTP/1.0" 404 0 "-" "GoogleAssociationService" 288488', 0, 0)
                         ]
                         )

def test_requests_in_loggs(logline, number, result):
    assert parser.requests_in_loggs(logline, number) == result


@pytest.mark.parametrize('logline, d, result',
                         [
                             ('Dec 01 11:06:07 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:07 +0100] "GET /internal/user/5fe5aeac-261d-4e2f-9811-c054edda14fa/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 92048', {}, {'200': 1}),
                             ('Nov 30 23:04:03 actify3-test-vm1 gunicorn[53253]: 172.16.3.5 - - [30/Nov/2019:23:04:03 +0100] "GET /.well-known/assetlinks.json HTTP/1.0" 404 0 "-" "GoogleAssociationService" 286953', {}, {'404': 1}),
                         ]
                         )

def test_responses_in_loggs(logline, d, result):
    assert parser.responses_in_loggs(logline, d) == result


@pytest.mark.parametrize('logline, d, sizes_of_2xx, num_of_sizes_of_2xx, result',
                         [
                             ('Dec 01 11:06:07 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:07 +0100] "GET /internal/user/5fe5aeac-261d-4e2f-9811-c054edda14fa/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 92048', {'200': 1}, 720, 1,  (1440, 2)),
                             ('Dec 01 11:06:07 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:07 +0100] "GET /internal/user/5fe5aeac-261d-4e2f-9811-c054edda14fa/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 92048', {'404': 2, '200': 2}, 1440, 2,  (2160, 3))

                         ]
                         )

def test_avgsize(logline, d, sizes_of_2xx, num_of_sizes_of_2xx, result):
    assert parser.avgsize(logline, d, sizes_of_2xx, num_of_sizes_of_2xx) == result

def test_date_diff_in_Seconds():
    result = parser.date_diff_in_Seconds(datetime.datetime(2019, 9, 6, 8, 39, 19), datetime.datetime(2019, 9, 6, 8, 39, 16))
    assert result == 3

def test_req_on_sec():
    result = parser.req_on_sec(datetime.datetime(2019, 10, 1, 0, 0, 0), datetime.datetime(2019, 12, 1, 0, 1, 1), 54516)
    assert result == ("%.4f" %(0.010343687203073887))

def test_default_start():
    result = parser.default_start('-- Logs begin at Fri 2019-09-06 08:39:18 CEST, end at Wed 2020-01-08 14:04:44 CET. --')
    assert result == datetime.datetime(2019, 9, 6, 8, 39, 18)

def test_default_end():
    result = parser.default_end('-- Logs begin at Fri 2019-09-06 08:39:18 CEST, end at Wed 2020-01-08 14:04:44 CET. --')
    assert result == datetime.datetime(2020, 1, 8, 14, 4, 44)



