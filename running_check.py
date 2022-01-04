
import subprocess
import time


# coms = ['ps', '-aef']
# process = subprocess.Popen(coms)


# stdout, stderr = process.communicate()

# print(stdout.splitlines())
def check(start_time, proc_id):
    print(f"{(time.time() - start_time):.2f}s - Checking for dupe processes...")
    num = 0
    coms = ["ps", "-aef", "ww"]
    out = subprocess.Popen(coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = out.communicate()
    # file_object = open('sample.txt', 'a')
    # file_object.write(stdout.decode('utf-8')+"\n\n")
    # file_object.close()
    final = stdout.decode("utf-8").splitlines()
    for line in final:
        if line.startswith("runner"):
            words = line.split(" ")
            for word in words:
                if word == "main.py":

                    raw_word_list = line.split(" ")
                    word_list = []
                    for i in raw_word_list:

                        if i != "":
                            word_list.append(i)

                    id = word_list[1]
                    name = word_list[-1]
                    if int(id) != proc_id:
                        num = num + 1
                        #   print(f"{id}: {name}")
                        print(f"Killing {id}:{name}...")
                        coms = ["kill", "-9", str(id)]
                        out = subprocess.Popen(
                            coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                        )
                        stdout, stderr = out.communicate()
                    #  print(f"{id}{name} killed!")
    if num > 0:
        print(
            f"{(time.time() - start_time):.2f}s - {num} main.py processes were found and killed."
        )
    elif num == 0:
        print(
            f"{(time.time() - start_time):.2f}s - No duplicate main.py process found :)"
        )

    # for i in final:
    #   if any(word in i for word in ['main.py']):
    #       print(i)
    #   print(i)
