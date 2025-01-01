import sys
from datetime import datetime, timedelta


def parse_interval(interval_str):
    # example input: '01:39:36,239 --> 01:39:41,182'
    start, end = interval_str.strip().split(" --> ")
    return start, end


def read_srt(srt_file="input.srt"):
    print(f"\nreading {srt_file}... ", end="")
    subfile = open(srt_file, "r", encoding="latin1")
    lines = subfile.readlines()
    lpos = 0
    items = []

    while lpos < len(lines):
        try:
            sub_nr = int(lines[lpos])
            lpos += 1
            if sub_nr < 1:
                continue
        except ValueError:
            lpos += 1
            continue

        sub_interval = lines[lpos].strip()
        lpos += 1

        sub_line = lines[lpos].strip()
        sub_text = ""
        while len(sub_line) > 0 and lpos < len(lines):
            sub_text += sub_line + "\n"
            lpos += 1
            if lpos < len(lines):
                sub_line = lines[lpos].strip()

        start_time, end_time = parse_interval(sub_interval)
        item = {
            'nr': sub_nr,
            'start_time': start_time,
            'end_time': end_time,
            'text': sub_text.strip()
        }

        items.append(item)

    print("done.")
    return items



def delay_time(time_str, delay_minutes=0, delay_seconds=0):
    # Parse the time string into a datetime object
    time_format = "%H:%M:%S,%f"
    time_obj = datetime.strptime(time_str, time_format)
    
    # Create a timedelta for the delay
    delay = timedelta(minutes=delay_minutes, seconds=delay_seconds)
    
    # Add the delay to the original time
    new_time_obj = time_obj + delay
    
    # Format the new time back to the desired string format
    # new_time_str = new_time_obj.strftime(time_format)
    new_time = new_time_obj.strftime("%H:%M:%S")
    new_time_ms = f"{new_time_obj.microsecond // 1000:03d}"

    return f"{new_time},{new_time_ms}"


def delay_lines(sublines, minutes=0, seconds=0):
    delay_items = []
    for sl in sublines:
        sl['start_time'] = delay_time(sl['start_time'], minutes, seconds)
        sl['end_time'] = delay_time(sl['end_time'], minutes, seconds)
        delay_items.append(sl)

    return delay_items


def time_difference(time_str1, time_str2):
    # Define the time format
    time_format = "%H:%M:%S,%f"
    
    # Parse the time strings into datetime objects
    time_obj1 = datetime.strptime(time_str1, time_format)
    time_obj2 = datetime.strptime(time_str2, time_format)
    
    # Calculate the difference
    difference = abs((time_obj2 - time_obj1).total_seconds())
    
    # Convert the difference to minutes and seconds
    minutes = int(difference // 60)
    seconds = int(difference % 60)
    
    return minutes, seconds


def write_srt(output_file, sublines):
    print(f"writing {output_file}... ", end="")
    out = open(output_file, "w")

    for sl in sublines:
        out.write(f"{sl['nr']}\n")
        out.write(sl['start_time']+ ' --> '+ sl['end_time'] + '\n')
        out.write(sl['text'] + '\n\n')

    out.close()
    print("done.\n")

def print_usage(cmd):
    print(f"USAGE: python {cmd} MM:SS input.srt output.srt")
    print("\nExample: ")
    print(f"  python {cmd} 01:53 in.srt out.srt")
    print("  This delays all subtitle lines by 1 minutes and 53 seconds.")
    print("  The result is written to out.srt\n")

if __name__ == "__main__":
    try:
        if len(sys.argv) < 4:
            print_usage(sys.argv[0]) 
            exit(1)

        delays = sys.argv[1].split(':')
        del_min = int(delays[0])
        del_sec = int(delays[1])

        sublines = read_srt(sys.argv[2])
        print(f"Delaying each line by {del_min} minutes and {del_sec} seconds... ", end="")
        sublines = delay_lines(sublines, del_min, del_sec)
        print("done.")
        write_srt(sys.argv[3], sublines)

    except ValueError:
        print_usage(sys.argv[0])
        exit(1)

