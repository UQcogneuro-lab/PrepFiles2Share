# %% General setup %%
# import libraries
import os
from pathlib import Path
import shutil
# setting paths - depends on YOUR path
os.chdir('/Volumes/CBradleyQBI/TMS-EEG-Visual/data')
ROOTPATH = Path().cwd()

# %% Define functions %% #
def bvfiles_rename_move(extension, ROOTPATH):  # can be '.vhdr' or '.vmrk'

    # %% Filtering files of interest %%
    # finding header files
    ext = '**/*' + extension
    bvFiles = sorted(list(ROOTPATH.glob(ext)))
    # filtering header files in BIDS folders
    bvFiles = [path for path in bvFiles if '/data/sub-' not in str(path)]
    bvFiles = [path for path in bvFiles if '/data/derivatives' not in str(path)]

    # For each header file, apply the following procedure
    for num, file in enumerate(bvFiles):
        print('Processing file ' + str(num+1) + ' out of ' + str(len(bvFiles)))

        # open the file
        with open(file, 'r', encoding='utf-8') as f:
            tmplines = f.readlines()
        # select the lines (and their contents) that contain the prefix 'DataFile' or 'MarkerFile', as these contain the name of the .eeg and .vmrk files that link to vhdr
        sslines = [[idx, line] for idx, line in enumerate(tmplines) if 'DataFile' in line or 'MarkerFile' in line]

        for i, ssline in enumerate(sslines):
            idx = ssline[0]  # extract line number
            line = ssline[1]  # extract line contents
            prefix, fname = line.split('=')  # get the line prefix in vhdr/vmrk header, i.e. 'DataFile' or 'MarkerFile'
            stem, ftype = fname.split('.')  # get the components of the filename (name and file type)
            subnum, subname, ses, block = stem.split('_')  # get the individual name sub-components. This is determined by how YOU named your files.
            subnum = subnum[1]+subnum[2]  # get rid of the 's' prefix to only retain the subject number. Again, this is determined by how YOU named your files.
            newstem = 'sub-' + subnum + '_task-TMSRDK_run-' + block + '_eeg' # create new name following BIDS convention
            newfname = '.'.join([newstem, ftype])  # add the file type
            newline = '='.join([prefix, newfname])  # add the line name
            tmplines[idx] = newline  # overwrite the old line in the vhdr/vmrk header

        # Set things up to save the new file
        newsubfolder = 'sub-' + subnum
        newfilename = newstem + extension
        newfilepath = ROOTPATH / newsubfolder / 'eeg' / newfilename
        newdirectory = os.path.dirname(newfilepath)
        if not os.path.exists(newdirectory):
            os.makedirs(newdirectory)
        with open(newfilepath, 'w', encoding='utf-8') as f:
            f.writelines(tmplines)

def rename_move(extension, ROOTPATH):  # can be '.eeg', '.EDF', or 'timestamps.csv', 'timestamps.txt' or 'trial_list.csv'

    # %% Filtering files of interest %%
    ext = '**/*' + extension
    listFiles = sorted(list(ROOTPATH.glob(ext)))
    # filtering header files in BIDS folders
    listFiles = [path for path in listFiles if '/data/sub-' not in str(path)]
    listFiles = [path for path in listFiles if '/data/derivatives' not in str(path)]

    # For each header file, apply the following procedure
    for num, file in enumerate(listFiles):
        print('Processing file ' + str(num+1) + ' out of ' + str(len(listFiles)))
        oldFileName = file.stem

        if '.eeg' in extension:
            subnum, subname, ses, block = oldFileName.split('_')  # get the individual name sub-components. This is determined by how YOU named your files.
            subnum = subnum[1]+subnum[2]  # get rid of the 's' prefix to only retain the subject number. Again, this is determined by how YOU named your files.
            newstem = 'sub-' + subnum + '_task-TMSRDK_run-' + block + '_eeg' # create new name following BIDS convention
        elif '.EDF' in extension:
            subnum = oldFileName[-5] + oldFileName[-4]
            newstem = 'sub-' + subnum + '_task-TMSRDK' + '_physio'
        elif 'timestamps.csv' or 'timestamps.txt' in extension:
            subnum = oldFileName[0]+oldFileName[1]
            newstem = 'sub-' + subnum + '_task-TMSRDK' + '_timestamps_beh'
        elif 'trial_list.csv' in extension:
            subnum = oldFileName[0]+oldFileName[1]
            newstem = 'sub-' + subnum + '_task-TMSRDK' + '_triallist_beh'

        newFileName = newstem + file.suffix  # add the file type

        # Set things up to save the new file
        newsubfolder = 'sub-' + subnum
        if '.eeg' in extension:
            newfilepath = ROOTPATH / newsubfolder / 'eeg' / newFileName
        elif '.EDF' in extension:
            newfilepath = ROOTPATH / newsubfolder / 'beh' / newFileName
        elif 'timestamps.csv' or 'timestamps.txt' in extension:
            newfilepath = ROOTPATH / newsubfolder / 'beh' / newFileName
        elif 'trial_list.csv' in extension:
            newfilepath = ROOTPATH / newsubfolder / 'beh' / newFileName

        newdirectory = os.path.dirname(newfilepath)
        if not os.path.exists(newdirectory):
            os.makedirs(newdirectory)
        shutil.copy(str(file), str(newfilepath))
    return listFiles

# %% Run functions %% #

bvfiles_rename_move('.vhdr', ROOTPATH)
print('Renaming .vhdr files; Done!')

bvfiles_rename_move('.vmrk', ROOTPATH)
print('Renaming .vmrk files; Done!')

listFiles = rename_move('.eeg', ROOTPATH)  # need to add .json files, etc...
rename_move('.EDF', ROOTPATH)  # actually, this probably needs to be converted to fully comply with BIDS...ah well...
rename_move('timestamps.csv', ROOTPATH)  # this also needs to be converted in .tsv, plus .json file...
rename_move('timestamps.txt', ROOTPATH)
rename_move('trial_list.csv', ROOTPATH)

# %% If you've messed up a few things, clean up %% #
# get rid of ._ files (what are they?)
# get rid of ..files
filelist = sorted(list(ROOTPATH.glob('**/*..EDF')))
for filepath in filelist:
    try:
        os.remove(filepath)
    except:
        print("Error while deleting file : ", filepath)

# rename the ..eeg files
filelist = sorted(list(ROOTPATH.glob('**/*..eeg')))
for filepath in filelist:
    os.rename(filepath, filepath.parent / (filepath.stem + 'eeg'))
