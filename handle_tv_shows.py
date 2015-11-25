#!/usr/bin/env python
import re, glob, shutil,sys, os

# tv list file as input NUMER 1 . MANDATORY
# destination device as input NUMBER 2. MANDATORY

if len(sys.argv) != 3:
    print("Usage: %s <series.list> </path/to/dst>" % sys.argv[0])
    sys.exit(0)
else:
    input_file = sys.argv[1]
    dst_folder = sys.argv[2]

    print("* Checking input file...")

    if os.path.isfile(input_file):
        print("\t** %s found! Ok" % input_file)
    else:
        print("\t** %s not found! Exiting" % input_file)
        sys.exit(0)

    print("* Checking destination folder...")
   
    if os.path.isdir(dst_folder):
        print("\t** %s found! Ok" % dst_folder)
    else:
        print("\t** %s not found! Exiting" % dst_folder)
        sys.exit(0)

	  
def check_destination(serie,season):
    check_path = dst_folder + "/" + serie + "/Season " + season
    if not os.path.isdir(check_path):
        print("- E - " + check_path + " does not exist... Exiting")
        sys.exit(0)
    return True


def copy_episodes(serie):
    for episode in glob.glob(serie.rstrip() + "*/*.mp4"):
        m = re.match("("+serie.rstrip()+").S(\d+)E(\d+).*/(.*.mp4)",episode)

        if m:
            tmp_serie = m.group(1).replace(".", " ")
            tmp_season = str(m.group(2)).lstrip("0") 
            tmp_ep_name = m.group(4)

            check_destination(tmp_serie,tmp_season)

            #Remote folder path: /path/to/dst/<Serie Name>/Season <X>/
            if not os.path.isfile(dst_folder+"/"+tmp_serie+"/Season "+tmp_season+"/"+tmp_ep_name):
                print("\t*** Copying %s to %s/%s/Season %s" % (tmp_ep_name,dst_folder,tmp_serie,tmp_season)) 
                shutil.copy2(episode,dst_folder+"/"+tmp_serie+"/Season "+tmp_season+"/" )       
            else:
                print("\t*** %s already in destination... Skipping" % (tmp_ep_name)) 

        else:
            print("- E - Cannot identify season/episode in: %s" % episode)


def main():
    myseries = open(input_file,"r")
    print("\n* Starting\n")
    for tvserie in myseries:
        print("** Show: %s" % tvserie.rstrip()) 
        copy_episodes(tvserie)


if __name__ == "__main__":
    main()

