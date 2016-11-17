import requests
import sys
import time
from concurrent.futures import as_completed, ThreadPoolExecutor
import argparse

#based on: http://stackoverflow.com/questions/20801034/how-to-measure-download-speed-and-progress-using-requests

def get_url(url, n_requests) :
    kbps_l = []
    total_kb = 0
    passed_time = 0
    good_requests = 0

    for i in xrange(n_requests):
        dl = 0
        start = time.time()
        
        try:
            r = requests.get(url, stream=True, verify=False, timeout=(2, 2))
            if r.status_code != 200:
                continue

            good_requests += 1

            for chunk in r.iter_content(chunk_size=1024):
                dl += len(chunk)

            passed_time += (time.time() - start)

            total_kb += dl / float(1024)
            
            kbps = total_kb
            if dl > 0:
                kbps = (1 / float(passed_time)) * total_kb

            kbps_l.append(kbps)
            if i % 50 == 0:
                print 'Request {}/{}'.format(i, n_requests)
        except Exception as e:
            print '[ERROR] Exception: {}'.format(e)


    return passed_time, sum(kbps_l) / float(len(kbps_l)), total_kb, good_requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost')
    parser.add_argument('--threads', default=30)
    parser.add_argument('--requests', default=300)
    parser.add_argument('--debug', dest='debug', action='store_true')
    args = parser.parse_args()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:

        print '[INFO]', 'Loading workers...'

        waits = {
            executor.submit(get_url, args.url, args.requests): i for i in xrange(args.threads)
        }

        print '[INFO]', 'Working...'

        kbps_l = []
        total_kb_l = []
        total_passed_requests = 0
        total_requests = args.requests * args.threads

        for future in as_completed(waits):
            node = waits[future]
            try:
                time_elapsed, kbps, total_kb, good_requests = future.result()
            except Exception as e:
                print '{} generated an exception: {}'.format(node, e)
            else:
                kbps_l.append(kbps)
                total_kb_l.append(total_kb)
                total_passed_requests += good_requests
                print '{}: Time Elapsed: {}s, Kbps:{}, total kb:{}, Passed requests:{}'.format(node, time_elapsed, kbps, total_kb, good_requests)

        print '\n=== RESULT ==='
        print '\tMean Throughput:{:.3f}Kbps, Approx total Throughput:{:.3f}Kbps, Total downloaded:{:.2f}Kb, Good requests:{:.3f}%\n'.format(sum(kbps_l) / float(len(kbps_l)), sum(kbps_l), sum(total_kb_l), (total_passed_requests * 100) / float(total_requests)) 
  